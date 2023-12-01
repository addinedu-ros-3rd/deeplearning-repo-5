import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
import cv2, imutils
import time, datetime
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.6
RED = (255, 0, 0)
GREEN = (0, 255, 0)

mycoco = open('/home/wintercamo/dev_ws/Project_ML/src/mycoco.txt', 'r')
data = mycoco.read()
class_list = data.split('\n')
mycoco.close()
print(class_list)

model = YOLO('/home/wintercamo/dev_ws/Project_ML/src/runs/detect/train3/weights/best.pt')

class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec = 0, parent = None):
        super().__init__()
        self.main = parent

    def run(self):
        while True:
            self.update.emit()
            time.sleep(0.1)

from_class = uic.loadUiType("/home/wintercamo/dev_ws/Project_ML/src/myui.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.isRecStart = False

        self.video = cv2.VideoCapture(-1)
        self.camera = Camera(self)
        self.realtime_display = QPixmap()
        self.camera.start()
        self.camera.update.connect(self.updateCamera)

        self.record = Camera(self)
        self.record.daemon = True
        
        # self.pixmap2 = QPixmap(self.boxzone.width(), self.boxzone.height())
        # self.pixmap2.fill(Qt.transparent)
        # self.boxzone.setPixmap(self.pixmap2)

        self.btnOpen.clicked.connect(self.openFile)
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

    def detect_target(self):
        detection = model(self.image)[0]
        
        for data in detection.boxes.data.tolist():
            confidence = float(data[4])

            if confidence < CONFIDENCE_THRESHOLD:
                continue
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            label = int(data[-1])

            if label == 1:
                cv2.rectangle(self.image, (xmin, ymin), (xmax, ymax), GREEN, 2)
            else:
                cv2.rectangle(self.image, (xmin, ymin), (xmax, ymax), RED, 2)
            
            cv2.putText(self.image, class_list[label]+' '+str(round(confidence, 2)) + '%', (xmin, ymin), cv2.FONT_ITALIC, 1, (255,255,255), 2)

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