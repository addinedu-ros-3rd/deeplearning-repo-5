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
CONFIDENCE_THRESHOLD = 0.6
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

# 식별 모델 정의
from_class = uic.loadUiType("/home/wintercamo/dev_ws/Project_ML/src/myui.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("유해조수 판별 모델 및 추적모델")

        # 식별 모델
        self.model = YOLO('/home/wintercamo/dev_ws/Project_ML/src/runs/detect/train3/weights/best.pt')

        # 실시간 영상 화면
        self.video = cv2.VideoCapture(-1)
        self.camera = Camera()
        self.realtime_display = QPixmap()
        self.camera.start()
        self.camera.update.connect(self.updateCamera)

        # 객체 검출 정보
        self.info_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.isdetect = False
        self.detect_end = None
        self.sequence = []

        self.isRecStart = False
        self.record = Camera(self)
        self.record.daemon = True
        self.record_string = False
        
    
        self.btnOpen.clicked.connect(self.openFile)
        self.btnRecord.clicked.connect(self.clickRecord)
        self.record.update.connect(self.updateRecording)

    def detect_target(self):
        detection = self.model(self.image)[0]
        
        for data in detection.boxes.data.tolist():
            confidence = float(data[4])

            if confidence < CONFIDENCE_THRESHOLD:
                continue

            else:
                xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
                label = int(data[-1])

                if label == 1:
                    box_color = GREEN
                else:
                    box_color = RED

                cv2.rectangle(self.image, (xmin, ymin), (xmax, ymax), box_color, 2)
                cv2.putText(self.image, class_list[label]+' '+str(round(confidence, 2)) + '%', (xmin, ymin), cv2.FONT_ITALIC, 1, WHITE, 2)
        
        try:
            self.isSignal.setText("")
            self.sequence.append(label)
            self.sequence = self.sequence[-3:]
        except:
            if len(self.sequence) != 0:
                self.sequence.pop(-1)
        try:
            if self.sequence[0] == self.sequence[-1]:
                self.isdetect = True
                self.recordingStart()
        except:
            self.isdetect = False
            self.isSignal.setText("No Target")
            self.isSignal.setStyleSheet("color: white")
        # if label is not None:
        #     print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBbb")
        # else:
        #     print("--------------")
                #     self.record_string = True
                #     self.recordingStart()
                # else:
                #     self.record_string = False
                #     self.recordingStop()
   
    def updateCamera(self):
        retval, self.image = self.video.read()
        if retval:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.detect_target()

            h,w,c = self.image.shape
            qimage = QImage(self.image.data, w, h, w*c, QImage.Format_RGB888)

            self.realtime_display = self.realtime_display.fromImage(qimage)
            self.realtime_display = self.realtime_display.scaled(self.display.width(), self.display.height())
            
            self.display.setPixmap(self.realtime_display)

    def updateRecording(self):
        self.writer.write(self.image)
    
    def clickRecord(self):
        if self.isRecStart == False:
            self.btnRecord.setText("Rec Stop")
            self.isRecStart = True

            self.recordingStart()
        else:
            self.btnRecord.setText("Rec Start")
            self.isRecStart = False

            self.recordingStop()

    def recordingStart(self):

        if self.record_string == True:
            row = self.info_table.rowCount()
            self.info_table.insertRow(row)
            self.info_table.setItem(row, 0, QTableWidgetItem(class_list[self.sequence[1]]))
            confidence = str(int(confidence*100)) + "%"
            self.info_table.setItem(row, 1, QTableWidgetItem(confidence))
            self.record_string = False
            
            # self.info_table.setItem(row, 2, QTableWidgetItem((str(xmin), str(ymin), str(xmax), str(ymax))))
        #     self.info_table.setItem(row, 3, QTableWidgetItem(시작))
            
        # self.info_table.setItem(row, 4, QTableWidgetItem(끝))
        self.record.running = True
        self.record.start()
        
        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now + '.avi'
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    
        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
        self.writer = cv2.VideoWriter(filename, self.fourcc, 20.0, (w, h))
    
    def recordingStop(self):
        self.record.running = False
    
        if self.isRecStart:
            self.writer.release()        


    

    def openFile(self):
        file = QFileDialog.getOpenFileName(filter='Image (*.*)')

        image = cv2.imread(file[0])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h,w,c = image.shape
        qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.display.width(), self.display.height())

        self.display.setPixmap(self.pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())
    