# 필요 라이브러리
# !pip install boto3 pyqt5

# 필요 인증파일
# ~/.aws/credentials

# AWS S3 클라이언트 설정
# s3_client = boto3.client('s3', region_name='ap-northeast-2')
# bucket_name = 'prj-wildlife'


import sys
import cv2
import boto3
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QDesktopWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QUrl, QTimer, Qt  # Qt를 추가로 임포트
import os

# AWS S3 클라이언트 설정
s3_client = boto3.client('s3', region_name='ap-northeast-2')
bucket_name = 'prj-wildlife'

# PyQt 윈도우 클래스
class S3Viewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 현재 화면의 해상도 얻기
        screen = QDesktopWidget().screenGeometry()

        # 창의 크기를 화면 해상도의 특정 비율로 설정
        window_width = int(screen.width() * 0.8)  # 화면 너비의 80%
        window_height = int(screen.height() * 0.8)  # 화면 높이의 80%
        self.setFixedSize(window_width, window_height)

        h_layout = QHBoxLayout(self)

        # 파일 목록의 너비를 창 너비의 일정 비율로 설정
        file_list_width = int(window_width * 0.2)  # 전체 너비의 20%
        self.file_list = QListWidget(self)
        self.file_list.setFixedWidth(file_list_width)
        self.file_list.clicked.connect(self.onFileClicked)
        h_layout.addWidget(self.file_list, 1)

        v_layout = QVBoxLayout()
        self.image_label = QLabel(self)
        self.video_label = QLabel(self)
        v_layout.addWidget(self.image_label)
        v_layout.addWidget(self.video_label)
        h_layout.addLayout(v_layout, 3)

        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextFrame)

        self.populateFileList()

    def handleStateChanged(self, state):
        print("Player State Changed: ", state)

    def handleError(self):
        print("Player Error: ", self.video_player.errorString())

    def populateFileList(self):
        # S3 버킷에서 파일 목록 가져오기
        response = s3_client.list_objects(Bucket=bucket_name)
        if 'Contents' in response:
            for file in response['Contents']:
                self.file_list.addItem(file['Key'])

    def onFileClicked(self, index):
        file_name = self.file_list.item(index.row()).text()
        print(file_name)
        # S3 버킷에서 파일의 임시 URL 생성
        url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_name}, ExpiresIn=3600)

        # 파일 타입에 따라 재생
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            self.timer.stop()  # 비디오 재생 중지
            self.video_label.hide()
            self.showImage(url)
            self.image_label.show()
        elif file_name.lower().endswith(('.mp4', '.avi', '.mkv', '.flv')):
            self.image_label.hide()
            self.cap = cv2.VideoCapture(url)
            self.timer.start(int(1000/30))  # 30fps로 설정
            self.video_label.show()

    def showImage(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            pixmap = QPixmap()
            success = pixmap.loadFromData(response.content)
            if success:
                scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.show()
            else:
                print("Pixmap 로딩 실패")
        else:
            print("URL 접근 실패:", response.status_code)

    def nextFrame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.video_label.setPixmap(scaled_pixmap)
        else:
            self.timer.stop()

# PyQt 애플리케이션 실행
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = S3Viewer()
    ex.show()
    sys.exit(app.exec_())
