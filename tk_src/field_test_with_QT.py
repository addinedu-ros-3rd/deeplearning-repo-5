# 라이브러리
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
import cv2, imutils
import time, datetime
from ultralytics import YOLO
import mysql.connector
import boto3
from botocore.exceptions import NoCredentialsError
import pygame

# S3 클라이언트 초기화
def initialize_s3_client():
    try:
        s3_client = boto3.client('s3')
        return s3_client
    except NoCredentialsError:
        print("Credentials not available")
        return None

# S3 버킷에 파일 업로드
def upload_file_to_s3(file_name, bucket, object_name=None):
    s3_client = initialize_s3_client()
    if s3_client is None:
        return False

    if object_name is None:
        object_name = file_name

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}")
        return True
    except NoCredentialsError:
        print("Error in uploading file")
        return False

# S3 버킷에서 파일 다운로드
def download_file_from_s3(bucket, object_name, file_name):
    s3_client = initialize_s3_client()
    if s3_client is None:
        return False

    try:
        s3_client.download_file(bucket, object_name, file_name)
        print(f"File {file_name} downloaded from {bucket}/{object_name}")
        return True
    except NoCredentialsError:
        print("Error in downloading file")
        return False

# aws RDS 연결
aws_DB = mysql.connector.connect(
    host = "database-1.ciifx43v3wkq.ap-northeast-2.rds.amazonaws.com",
    port = 3306,
    user = "root",
    password = "qaz51133"
)

# 데이터베이스 생성
my_db_name = 'Project_ML'  # create하려는 데이터베이스 이름
sql_query = 'CREATE DATABASE ' + my_db_name

my_cursor = aws_DB.cursor()  # 커서 생성

my_cursor.execute(f"SHOW DATABASES LIKE '{my_db_name}'")  # create하려는 데이터베이스가 이미 있는지 파악을 하기 위함.

# 없으면 생성한다.
if my_cursor.fetchone() is None:
    my_cursor.execute(sql_query)
    aws_DB.commit()
    print(f"데이터베이스 '{my_db_name}'를 생성했습니다.")

# 있으면 스킵한다.
else:  
    print(f"데이터베이스 '{my_db_name}'가 이미 존재합니다. 생성을 스킵합니다.")

my_cursor.execute(f"USE {my_db_name}")  # 해당 데이터베이스로 들어간다.

# 테이블 생성
my_table_name  = "detect_log"
sql_query = f'''CREATE TABLE {my_table_name} (
                time DATETIME,
                class VARCHAR(16),
                X_min float,
                X_max float,
                y_min float,
                y_max float,
                link_picture VARCHAR(255),
                link_video VARCHAR(255)
            )'''

my_cursor.execute(f"SHOW TABLES LIKE %s", (my_table_name,))  # 만드려는 테이블명이 중복인지 아닌지 확인

# 테이블 없으면 생성
if my_cursor.fetchone() is None:
    my_cursor.execute(sql_query)
    aws_DB.commit()
    print(f"테이블 '{my_table_name}'를 생성했습니다.")

# 있으면 스킵
else:
    print(f"테이블 '{my_table_name}'가 이미 존재합니다. 생성을 스킵합니다.")

# INSERT 쿼리 불러오기
sql_query = f'''INSERT INTO {my_table_name} (time, class, x_min, y_min, x_max, y_max, link_picture, link_video)
                                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''

# 경계박스관련 변수
CONFIDENCE_THRESHOLD = 0.8
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 식별 모델
model = YOLO('/home/wintercamo/dev_ws/Project_ML/src/best.pt')

# 감지 객체 명칭
mycoco = open('/home/wintercamo/dev_ws/Project_ML/src/mycoco.txt', 'r')
data = mycoco.read()
class_list = data.split('\n')
mycoco.close()

# 카메라 클래스
class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec = 0):
        super().__init__()

    def run(self):
        while True:
            self.update.emit()
            time.sleep(0.1)

# mp3 플레이어 클래스
class Mp3Player(QThread):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        # Pygame 초기화
        pygame.init()
        pygame.mixer.init()

        # MP3 파일 로드 및 재생
        pygame.mixer.music.load(self.file_path)
        pygame.mixer.music.play()

        # 음악 재생 상태 체크
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def stop(self):
        # 음악 종료
        pygame.mixer.music.stop()
        self.terminate()

# UI 불러오기
from_class = uic.loadUiType("/home/wintercamo/dev_ws/Project_ML/src/myui.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("유해조수 판별 모델 및 추적모델") 

        # 실시간 영상 화면
        self.image = None
        # self.video = cv2.VideoCapture('/home/wintercamo/dev_ws/Project_ML/data/samples/Bear.mp4')  # 웹캠 or 로컬 영상 파일
        self.video = cv2.VideoCapture(0)
        self.camera = Camera()
        self.realtime_display = QPixmap()
        self.camera.start()
        self.camera.update.connect(self.updateCamera)
        
        # 객체 검출 정보 및 DB 저장
        self.record = Camera(self)
        self.info_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.row = self.info_table.rowCount()
        self.record.update.connect(self.updateRecording)

        self.record_flag = False
        self.record_stop_timer = QTimer(self)
        self.record_stop_timer.timeout.connect(self.recordingStop)
        
        self.capture_flag = 0

        self.mp3Player = Mp3Player("/home/wintercamo/dev_ws/Project_ML/data/samples/EAS.mp3")

        
#     def openFile(self):
#         file = QFileDialog.getOpenFileName(filter='Image (*.*)')

#         image = cv2.imread(file[0])
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         h,w,c = image.shape
#         qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
#         self.pixmap = self.pixmap.fromImage(qimage)
#         self.pixmap = self.pixmap.scaled(self.display.width(), self.display.height())
#         self.display.setPixmap(self.pixmap)

    def record_on_DB(self, detected_class, xmin, ymin, xmax, ymax):
        self.row = self.info_table.rowCount()
        self.info_table.insertRow(self.row)

        self.info_table.setItem(self.row, 0, QTableWidgetItem(str(self.now)))
        self.info_table.setItem(self.row, 1, QTableWidgetItem(detected_class))

        self.info_table.setItem(self.row, 2, QTableWidgetItem(str(xmin)))
        self.info_table.setItem(self.row, 3, QTableWidgetItem(str(ymin)))
        self.info_table.setItem(self.row, 4, QTableWidgetItem(str(xmax)))
        self.info_table.setItem(self.row, 5, QTableWidgetItem(str(ymax)))

        self.info_table.setItem(self.row, 6, QTableWidgetItem(str(self.image_full_path_s3)))
        self.info_table.setItem(self.row, 7, QTableWidgetItem(str(self.video_full_path_s3)))
    
        my_cursor.execute(sql_query, (str(self.now), detected_class, str(xmin), str(ymin), str(xmax),str(ymax),
                                      str(self.image_full_path_s3), str(self.video_full_path_s3)))
        aws_DB.commit()
    
    def captureImage(self):
        timing = self.now
        filename = timing.replace(' ', '').replace('/','').replace(':','').replace('_','')
        link = "images/" + filename[:6]

        filename = filename + ".jpg"
        self.image_full_path_s3 = os.path.join(link, filename)
        self.image_full_path_local = os.path.join("/home/wintercamo/dev_ws/Project_ML/data/images", filename)
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(self.image_full_path_local, image)
        upload_file_to_s3(self.image_full_path_local, 'prj-wildlife', self.image_full_path_s3)
        # self.upload_stack_images.append((self.image_full_path_local, self.image_full_path_s3))
        
    def updateRecording(self):
        self.writer.write(cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))

    def recordingStop(self):
        if self.record_flag == True:
            self.record_flag = False
            self.mp3Player.stop()
            self.writer.release()
            upload_file_to_s3(self.video_full_path_local, 'prj-wildlife', self.video_full_path_s3)
            # self.upload_stack_video.append((self.video_full_path_local, self.video_full_path_s3))

    def recordingStart(self):
        self.record.start()
        self.mp3Player.start()
        timing = self.now
        filename = timing.replace(' ', '').replace('/','').replace(':','').replace('_','')
        link = "videos/" + filename[:6]
        
        filename = filename + '.avi'
        self.video_full_path_s3 = os.path.join(link, filename)
        self.video_full_path_local = os.path.join("/home/wintercamo/dev_ws/Project_ML/data/videos", filename)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
        self.writer = cv2.VideoWriter(self.video_full_path_local, self.fourcc, 20.0, (w, h))
        self.record_stop_timer.start(10000)  # 30초: 30000

    def detect_target(self):
        detection = model(self.image)[0]

        for data in detection.boxes.data.tolist():
            confidence = float(data[4])

            if confidence < CONFIDENCE_THRESHOLD:
                continue

            if self.record_flag == False:
                self.recordingStart()
                self.record_flag = True            

            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            label = int(data[-1])
            
            cv2.rectangle(self.image, (xmin, ymin), (xmax, ymax), RED, 2)
            cv2.putText(self.image, class_list[label] + ' '+str(round(confidence, 2)), (xmin, ymin), cv2.FONT_ITALIC, 1, WHITE, 2)
            
            self.current_second = time.time()

            if (self.current_second - self.capture_flag) >= 2:
                self.captureImage()
                self.record_on_DB(class_list[label], xmin, ymin, xmax, ymax)
                self.capture_flag = self.current_second

    def updateCamera(self):
        retval, self.image = self.video.read()
        if retval:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.now = datetime.datetime.now().strftime('%y/%m/%d _ %H:%M:%S')
            cv2.putText(self.image, self.now, (30, 30), cv2.FONT_ITALIC, 1, WHITE, 2)

            self.detect_target()

            h,w,c = self.image.shape
            qimage = QImage(self.image.data, w, h, w*c, QImage.Format_RGB888)

            self.realtime_display = self.realtime_display.fromImage(qimage)
            self.realtime_display = self.realtime_display.scaled(self.display.width(), self.display.height())
            
            self.display.setPixmap(self.realtime_display)

    def closeEvent(self, event):  # gui를 닫는 즉시 실행되는 함수
        if self.record_flag:
            self.recordingStop()
        aws_DB.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())