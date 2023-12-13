# 라이브러리
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
import cv2, imutils
import time, datetime
from ultralytics import YOLO

# 경계박스관련 변수
CONFIDENCE_THRESHOLD = 0.5
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

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

# UI 소환
from_class = uic.loadUiType("/home/wintercamo/dev_ws/Project_ML/src/myui.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("유해조수 판별 모델 및 추적모델")

        # 식별 모델
        self.model = YOLO('/home/wintercamo/dev_ws/Project_ML/src/runs/detect/train3/weights/best.pt')

        # 실시간 영상 화면
        self.image = None
        self.video = cv2.VideoCapture(-1)
        self.camera = Camera()
        self.realtime_display = QPixmap()
        self.camera.start()
        self.camera.update.connect(self.updateCamera)
        
        self.record = Camera(self)

        # 객체 검출 정보
        self.previous_status = None
        self.current_status = None
        self.fisrtEncount = False
        self.info_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.row = self.info_table.rowCount()
        self.detect_end = None

    def detect_target(self):
        detection = self.model(self.image)[0]
        
        if len(detection.boxes) == 0:
            self.current_status = None

        else:
            for data in detection.boxes.data.tolist():
                confidence = float(data[4])

                if confidence >= CONFIDENCE_THRESHOLD:
                    xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
                    label = int(data[-1])

                    if label == 1: box_color = GREEN
                    else: box_color = RED

                    cv2.rectangle(self.image, (xmin, ymin), (xmax, ymax), box_color, 2)
                    cv2.putText(self.image, class_list[label]+' '+str(round(confidence, 2)) + '%', (xmin, ymin), cv2.FONT_ITALIC, 1, WHITE, 2)
                    self.current_status = class_list[label]
            
         

        if self.current_status in class_list:
            if self.previous_status is None or self.previous_status != self.current_status:
                self.start_db_record(label)

        if self.previous_status in class_list and self.current_status is None:
            self.end_db_record()
        
        elif self.previous_status and self.previous_status != self.current_status:
            self.end_db_record()
                
    def start_db_record(self,label):
        self.recordingStart()
        self.row = self.info_table.rowCount()
        self.info_table.insertRow(self.row)
        self.info_table.setItem(self.row, 0, QTableWidgetItem(class_list[label]))
        timing = datetime.datetime.now().strftime('%y%m%d_%H:%M:%S')
        self.info_table.setItem(self.row, 1, QTableWidgetItem(str(timing)))

    def end_db_record(self):
        self.fisrtEncount = False
        timing = datetime.datetime.now().strftime('%y/%m/%d_%H:%M:%S')
        self.info_table.setItem(self.row, 2, QTableWidgetItem(timing))
        self.recordingStop()

    def recordingStart(self):
        self.record.start()
        
        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now + '.avi'
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    
        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
        self.writer = cv2.VideoWriter(filename, self.fourcc, 20.0, (w, h))

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

    # def closeEvent(self, event):  # gui를 닫는 즉시 실행되는 함수
    #     self.recordingStop()
    
    def updateRecording(self):
        self.writer.write(self.image)
    
    def recordingStop(self):
        self.writer.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())
