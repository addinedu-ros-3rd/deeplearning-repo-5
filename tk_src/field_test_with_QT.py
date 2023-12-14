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
                box_num int,
                link VARCHAR(255)
            )'''

my_cursor.execute(f"SHOW TABLES LIKE %s", (my_table_name,))  # 만드려는 테이블명이 중복인지 아닌지 확인

if my_cursor.fetchone() is None:
    my_cursor.execute(sql_query)
    aws_DB.commit()
    print(f"테이블 '{my_table_name}'를 생성했습니다.")
else:
    print(f"테이블 '{my_table_name}'가 이미 존재합니다. 생성을 스킵합니다.")

# INSERT 쿼리 불러오기
sql_query = f'''INSERT INTO {my_table_name} (time, class, x_min, y_min, x_max, y_max, link)
                                     VALUES (%s, %s, %s, %s, %s, %s, %s)'''

# 경계박스관련 변수
CONFIDENCE_THRESHOLD = 0.8
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# 식별 모델
# model = YOLO('/home/wintercamo/dev_ws/Project_ML/src/runs/detect/train3/weights/best.pt')
model = YOLO('/home/wintercamo/dev_ws/Project_ML/src/best.pt')

# 감지 객체 명칭
mycoco = open('/home/wintercamo/dev_ws/Project_ML/src/mycoco.txt', 'r')
data = mycoco.read()
class_list = data.split('\n')
mycoco.close()

# 파일 경로
video_path = "/home/wintercamo/dev_ws/Project_ML/data/videos"
image_path = "/home/wintercamo/dev_ws/Project_ML/data/images"

# 카메라 클래스
class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec = 0):
        super().__init__()

    def run(self):
        while True:
            self.update.emit()
            time.sleep(0.1)

class RecordViewer(QThread):
    pass

# UI 소환
from_class = uic.loadUiType("/home/wintercamo/dev_ws/Project_ML/src/myui.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("유해조수 판별 모델 및 추적모델")

        # 실시간 영상 화면
        self.image = None
        self.video = cv2.VideoCapture('/home/wintercamo/dev_ws/Project_ML/data/samples/wild_boars.mp4')
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

        self.past_second = datetime.datetime.now().second
        self.current_second = datetime.datetime.now().second

    def captureImage(self):        
        timing = datetime.datetime.now().strftime('%y_%m_%d_%H_%M_%S')
        filename = timing + '.jpg'

        full_path = os.path.join(image_path, filename)
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(full_path, image)

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
            cv2.putText(self.image, class_list[label]+' '+str(round(confidence, 2)), (xmin, ymin), cv2.FONT_ITALIC, 1, WHITE, 2)
            
            if (self.current_second - self.past_second) >= 2:
                self.captureImage()
            else:
                self.past_second = self.current_second

            self.record_on_DB(class_list[label], xmin, ymin, xmax, ymax)

        self.current_second = datetime.datetime.now().second

    def record_on_DB(self, detected_class, xmin, ymin, xmax, ymax):
        self.row = self.info_table.rowCount()
        self.info_table.insertRow(self.row)

        timing = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.info_table.setItem(self.row, 0, QTableWidgetItem(str(timing)))
        self.info_table.setItem(self.row, 1, QTableWidgetItem(detected_class))

        self.info_table.setItem(self.row, 2, QTableWidgetItem(str(xmin)))
        self.info_table.setItem(self.row, 3, QTableWidgetItem(str(ymin)))
        self.info_table.setItem(self.row, 4, QTableWidgetItem(str(xmax)))
        self.info_table.setItem(self.row, 5, QTableWidgetItem(str(ymax)))
        
        filename = timing[2:]
        filename = filename.replace(' ', '_').replace('-','_').replace(':','_')
        filename = video_path + '/' +filename + '.avi'
        self.info_table.setItem(self.row, 6, QTableWidgetItem(str(filename)))
    
        my_cursor.execute(sql_query, (str(timing), detected_class, str(xmin), str(ymin), str(xmax), str(ymax), str(filename)))
        aws_DB.commit()
    
    def recordingStop(self):
        if self.record_flag == True:
            self.record_flag = False
            self.writer.release()

    def recordingStart(self):
        self.record.start()

        timing = datetime.datetime.now().strftime('%y_%m_%d_%H_%M_%S')
        filename = timing + '.avi'
        full_path = os.path.join(video_path, filename)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
        self.writer = cv2.VideoWriter(full_path, self.fourcc, 20.0, (w, h))
        self.record_stop_timer.start(30000)  # 30초: 30000

    def openFile(self):
        file = QFileDialog.getOpenFileName(filter='Image (*.*)')

        image = cv2.imread(file[0])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h,w,c = image.shape
        qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.display.width(), self.display.height())
        self.display.setPixmap(self.pixmap)

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
    
    def updateRecording(self):
        self.writer.write(cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())