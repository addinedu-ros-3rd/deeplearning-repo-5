import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
import cv2, imutils
import time, datetime
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.7  # 최소 정확도
# 경계박스 색깔
GREEN = (0, 255, 0)  # 사람의 경우 초록색
RED = (0, 0 , 255)  # 타겟의 경우(사슴, 멧돼지) 빨간색
WHITE = (255, 255, 255) # 경계박스 글씨 색 하얀색

class_list = ['None', 'Deer', 'Human', 'wild boar']
model = YOLO('best.pt')

class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec = 0, parent = None):
        super().__init__()
        self.main = parent
        self.running = True

    def run(self):
        while self.running == True:
            self.update.emit()
            time.sleep(0.1)
    
    def stop(self):
        self.running = False

from_class = uic.loadUiType("myui.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.isCameraOn = False
        self.isRecStart = False

        self.pixmap = QPixmap()

        self.camera = Camera(self)
        self.camera.daemon = True

        self.record = Camera(self)
        self.record.daemon = True
        
        self.camera.start()
        self.video = cv2.VideoCapture(-1)
        # self.cameraStart()
        self.btnOpen.clicked.connect(self.openFile)
        # self.btnCamera.clicked.connect(self.clickCamera)
        self.camera.update.connect(self.updateCamera)
        self.btnRecord.clicked.connect(self.clickRecord)
        self.record.update.connect(self.updateRecording)

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

    def updateCamera(self):
        retval, self.image = self.video.read()
        if retval:
            image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            h,w,c = image.shape
            qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
            
            detection = model(image)[0]

            for data in detection.boxes.data.tolist():
                confidence = float(data[4])

                if confidence < CONFIDENCE_THRESHOLD:
                    continue  

                xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])  # 경계박스의 너비, 높이 좌표
                label = int(data[5])  # 인식한 객체의 라벨(이름)

                if label == 2:
                    self.record_status.setText('check!')
                else:
                    self.record_status.setText('No')
            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.display.width(), self.display.height())
            
            self.display.setPixmap(self.pixmap)

    def clickCamera(self):
        if self.isCameraOn == False:
            self.btnCamera.setText("Camera off")
            self.isCameraOn = True

            self.cameraStart()
        else:
            self.btnCamera.setText("Camera on")
            self.isCameraOn = False
            self.cameraStop()


    # def cameraStart(self):
    #     self.camera.running = True
    #     self.camera.start()
    #     self.video = cv2.VideoCapture(-1)

    # def cameraStop(self):
    #     self.camera.running = False
    #     self.video.release()

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