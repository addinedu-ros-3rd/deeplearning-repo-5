import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
import cv2, imutils
import time, datetime
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.6

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

        self.clear_timer = QTimer(self)
        self.clear_timer.start(300)
        self.clear_timer.timeout.connect(self.clear_box)

        self.record = Camera(self)
        self.record.daemon = True
        
        self.pixmap2 = QPixmap(self.boxzone.width(), self.boxzone.height())
        self.pixmap2.fill(Qt.transparent)
        self.boxzone.setPixmap(self.pixmap2)

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

    def clear_box(self):
        self.pixmap2 = QPixmap(self.boxzone.width(), self.boxzone.height())
        self.pixmap2.fill(Qt.transparent)
        self.boxzone.setPixmap(self.pixmap2)

    def draw_box(self, color, xmin, ymin, xmax, ymax):
        painter = QPainter(self.boxzone.pixmap())
        painter.setPen(QPen(color, 5, Qt.SolidLine))
        painter.drawRect(xmin, ymin, (xmax - xmin), (ymax-ymin))
        painter.end()
    
    def target_detect(self, image):
        detection = model(image)[0]

        for data in detection.boxes.data.tolist():
            confidence = float(data[4])

            if confidence < CONFIDENCE_THRESHOLD:
                continue

            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            # label = int(data[5])
            label = int(data[4])
            self.draw_box(Qt.red, xmin, ymin, xmax, ymax)
            # self.draw_box(Qt.transparent, xmin, ymin, xmax, ymax)
            # if label == 2:
            #     self.draw_box(xmin, ymin, xmax, ymax)
            # else:
            #     print("None")

    def updateCamera(self):
        retval, self.image = self.video.read()
        if retval:
            image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)    

            h,w,c = image.shape
            qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)

            self.target_detect(image)

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