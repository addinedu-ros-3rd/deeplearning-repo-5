# 필요 라이브러리
# !pip install boto3 pyqt5 pymysql

# 필요 인증파일
# ~/.aws/credentials

# AWS S3 클라이언트 설정
# s3_client = boto3.client('s3', region_name='ap-northeast-2')
# bucket_name = 'prj-wildlife'

import sys
import pymysql
import boto3
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QFrame, QProgressBar, QSizePolicy
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QRect, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtWidgets import QLabel, QComboBox, QMessageBox, QAbstractItemView

import logging

# 로깅 설정
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# AWS S3 클라이언트 설정
s3_client = boto3.client('s3', region_name='ap-northeast-2')
bucket_name = 'prj-wildlife'

class TimelineWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.eventPositions = [10, 30, 50]
        self.setMinimumHeight(20)  # 최소 높이 설정
    
    def setEventPositions(self, positions):
        self.eventPositions = positions
        self.update()  # 타임라인 위젯 업데이트
        
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        # Draw the timeline
        painter.setPen(QColor(0, 0, 0))
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())

        # Draw event markers
        for position in self.eventPositions:
            x = int(rect.width() * position / 100)  # x 좌표를 정수로 변환
            painter.drawLine(x, rect.bottom(), x, rect.bottom() - 10)  # Adjust marker size as needed


class WildlifeUserGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.videoFiles = [
        ]

        self.setWindowTitle("Wildlife User GUI")
        self.setGeometry(200, 100, 1200, 1200)

        # Create a widget for window contents
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # Create the main vertical layout
        self.mainVerticalLayout = QVBoxLayout(self.centralWidget)
        
        self.mainLayout = QHBoxLayout()
        self.playlistLayout = QVBoxLayout()
        
        self.playLayout = QVBoxLayout()
        self.recentLayout = QHBoxLayout()
        self.videoLayout = QVBoxLayout()


        # Create the top label
        top_label = QLabel("Animal Detecting System", self)
        top_label.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20, QFont.Bold)
        top_label.setFont(font)
        top_label.setStyleSheet("background-color: rgb(0, 0, 102); color: rgb(255, 255, 255); border: 10px solid black;")
        self.mainVerticalLayout.addWidget(top_label)

        # Create the main horizontal layout for playlist and video
        self.playlist = QListWidget()
        self.playlist.setSelectionMode(QAbstractItemView.SingleSelection)
        self.playlist.itemSelectionChanged.connect(self.onItemSelected)


        self.playlistspaceLabel = QLabel(" ")
        # 카메라 장치 레이블과 콤보박스 생성
        self.cameraLabel = QLabel("카메라 장치")
        font = QFont("Arial", 10, QFont.Bold)  # Arial 글꼴, 20pt 크기, 굵은 글씨
        self.cameraLabel.setFont(font)
        self.cameraComboBox = QComboBox()
        self.cameraComboBox.addItems(["1", "2"])  # 콤보박스에 장치 번호 추가

        # 카메라 장치 레이블과 콤보박스를 레이아웃에 추가
        self.playlistLayout.addWidget(self.playlistspaceLabel)
        self.playlistLayout.addWidget(self.cameraLabel)
        self.playlistLayout.addWidget(self.cameraComboBox)
        self.playlistspaceLabel = QLabel(" ")
        self.playlistLayout.addWidget(self.playlistspaceLabel)
        # 기존의 playlistLabel을 레이아웃에 추가
        self.playlistLabel = QLabel("야생동물 출현 기록")
        self.playlistLabel.setFont(font)
        self.playlistLayout.addWidget(self.playlistLabel)


        # 이미지 레이블 생성 및 설정
        self.recentImage = QLabel()
        
        # recentVideo에 대한 미디어 플레이어 생성 및 설정
        self.recentVideo = QVideoWidget()
        self.recentMediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.recentMediaPlayer.setVideoOutput(self.recentVideo)
        
        # self.recentLayout에 이미지 레이블 추가
        self.recentLayout.addWidget(self.recentImage, 5)
        self.recentLayout.addWidget(self.recentVideo, 5)
        
        self.recentFrame = QFrame()
        self.recentFrame.setLayout(self.recentLayout)
        self.recentFrame.setFrameStyle(QFrame.StyledPanel)

        # Create video widget, player, and buttons
        self.videoWidget = QVideoWidget()
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.positionChanged.connect(self.updateProgressBar)
        self.player.mediaStatusChanged.connect(self.onMediaStatusChanged)
        self.playButton = QPushButton("Play")

        # Create the timeline widget and add it to the layout
        self.timelineWidget = TimelineWidget()
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)  # 진행율 텍스트 숨기기
        self.totalDuration = 0
        self.totalPosition = 0
        
        self.videoLayout.addWidget(self.playButton)
        self.videoLayout.addWidget(self.videoWidget)
        self.videoLayout.addWidget(self.timelineWidget)
        self.videoLayout.addWidget(self.progressBar)

        # Set size policy for timeline widget and progress bar
        self.timelineWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.progressBar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
                
        # Create a frame around the video widget and controls
        self.videoFrame = QFrame()
        self.videoFrame.setLayout(self.videoLayout)
        self.videoFrame.setFrameStyle(QFrame.StyledPanel)
        
        self.playspaceLabel1 = QLabel(" ")
        self.recentLabel = QLabel("실시간 최근 상황")
        self.recentLabel.setFont(font)

        self.playspaceLabel2 = QLabel(" ")
        self.playLayout.addWidget(self.playspaceLabel1)
        self.videoLabel = QLabel("출현 기록 비디오 재생")
        self.videoLabel.setFont(font)
        
        self.playLayout.addWidget(self.recentLabel)
        self.playLayout.addWidget(self.recentFrame, 3)
        self.playLayout.addWidget(self.playspaceLabel2)
        self.playLayout.addWidget(self.videoLabel)
        self.playLayout.addWidget(self.videoFrame, 7)
        
        # Add playlist and its label to the playlist layout
        self.playlistLayout.addWidget(self.playlist)
        self.mainLayout.addLayout(self.playlistLayout, 2)
        self.mainLayout.addLayout(self.playLayout, 7)

        # Add the main horizontal layout to the main vertical layout
        self.mainVerticalLayout.addLayout(self.mainLayout)

        # Connect the player to the video widget and the button
        self.player.setVideoOutput(self.videoWidget)
        self.playButton.clicked.connect(self.click_play)

        # Populate the playlist (for demo purposes, using placeholder items)
        #self.populate_playlist()
        
        logging.debug("GUI Initialized")

        self.lastImage = ""
        self.lastVideo = ""

        # 타이머 초기화 및 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetchLatestData)  # 타이머 시그널을 슬롯에 연결
        self.timer.start(1000)  # 1초(1000밀리초)마다 타이머 실행
        
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.updateList)  # 타이머 시그널을 슬롯에 연결
        self.timer2.start(11000)  # 1초(1000밀리초)마다 타이머 실행
        
        self.updateList()

    def onItemSelected(self):
        # 선택된 아이템들 가져오기
        selected_items = self.playlist.selectedItems()

        # 선택된 아이템들이 있다면
        if selected_items:
            selected_item = selected_items[0]  # 첫 번째 선택된 아이템
            # print(selected_item.text())        # 아이템의 텍스트 출력
            try:
                self.connectDB()
                with self.connection.cursor() as cursor:
                    # 쿼리 실행
                    query = f"""SELECT MIN(time) as earliest_time, link_video
                            FROM detect_log
                            WHERE time >= CONCAT(DATE_FORMAT('{selected_item.text()}', '%Y-%m-%d %H:'), LPAD(FLOOR(MINUTE('{selected_item.text()}') / 10) * 10, 2, '0'), ':00')
                            AND time < CONCAT(DATE_FORMAT('{selected_item.text()}' + INTERVAL 10 MINUTE, '%Y-%m-%d %H:'), LPAD(FLOOR(MINUTE('{selected_item.text()}' + INTERVAL 10 MINUTE) / 10) * 10, 2, '0'), ':00')
                            GROUP BY link_video
                            ORDER BY earliest_time;"""
                    # print(query)
                    cursor.execute(query)
                    list_data = cursor.fetchall()
                    logging.debug(f"video list data: {list_data}")
                self.disconnectDB()
            except Exception as e:
                logging.error(f"video list query failed: {e}")

            # 결과 처리
            if list_data != None:
                self.videoFiles = []
                for row in list_data:
                    self.videoFiles.append(row[1])
                print(self.videoFiles)

    def updateList(self):
        try:
            self.connectDB()
            with self.connection.cursor() as cursor:
                # 쿼리 실행
                query = """SELECT 
                                MIN(time) as earliest_time,
                                CONCAT(DATE_FORMAT(time, '%Y-%m-%d %H:'), LPAD(FLOOR(MINUTE(time) / 10) * 10, 2, '0')) as rounded_time,
                                COUNT(*)
                            FROM 
                                detect_log
                            GROUP BY 
                                CONCAT(DATE_FORMAT(time, '%Y-%m-%d %H:'), LPAD(FLOOR(MINUTE(time) / 10) * 10, 2, '0'))
                            ORDER BY
                                earliest_time DESC;"""
                cursor.execute(query)
                list_data = cursor.fetchall()
                # logging.debug(f"list data: {list_data}")
            self.disconnectDB()
        except Exception as e:
            logging.error(f"updateList query failed: {e}")
        
        # 결과 처리
        if list_data != None:
            self.playlist.clear()
            for row in list_data:
                # print(row)
                self.playlist.addItem(row[0].strftime("%Y-%m-%d %H:%M:%S"))


    def fetchLatestData(self):
        # 데이터베이스에서 최신 데이터를 가져오는 메서드
        try:
            self.connectDB()
            with self.connection.cursor() as cursor:
                # 쿼리 실행
                query = """SELECT 
                            MIN(time) as earliest_time,
                            link_picture,
                            link_video
                            FROM detect_log
                            WHERE CONVERT_TZ(time, 'Asia/Seoul', 'UTC') > NOW() - INTERVAL 10 MINUTE
                            GROUP BY link_video
                            ORDER BY earliest_time DESC
                            LIMIT 2;"""
                cursor.execute(query)

                # 결과 처리
                latest_data = cursor.fetchall()
                # logging.debug(f"Latest data: {latest_data}")
            self.disconnectDB()
        except Exception as e:
            logging.error(f"fetchLatestData query failed: {e}")
                
        if len(latest_data) < 2:
            self.recentImage.setPixmap(QPixmap())
            self.recentMediaPlayer.stop()
            self.recentMediaPlayer.setMedia(QMediaContent())
        else:
            print(latest_data[0])
            print(latest_data[1])
            if self.lastImage != latest_data[0][1]:
                self.lastImage = latest_data[0][1]
                # S3 버킷에서 파일의 임시 URL 생성
                url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': self.lastImage}, ExpiresIn=3600)
                print("image: ", url)
                response = requests.get(url)
                if response.status_code == 200:
                    pixmap = QPixmap()
                    success = pixmap.loadFromData(response.content)
                    if success:
                        scaled_pixmap = pixmap.scaled(self.recentImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # recentImage 크기에 맞게 조정
                        self.recentImage.setPixmap(scaled_pixmap)
                        self.recentImage.setScaledContents(True)  # 이미지 크기 자동 조절  
                    else:
                        print("Pixmap 로딩 실패")
                else:
                    print("URL 접근 실패:", response.status_code)
                
            if self.lastVideo != latest_data[1][2]:
                self.lastVideo = latest_data[1][2]
                # S3 버킷에서 파일의 임시 URL 생성
                url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': self.lastVideo}, ExpiresIn=3600)
                print("video: ", url)
                # 동영상 파일 재생
                self.recentMediaPlayer.setMedia(QMediaContent(QUrl(url)))
                self.recentMediaPlayer.play()

    def connectDB(self):
        # 데이터베이스 연결 설정
        self.connection = pymysql.connect(  host='database-1.ciifx43v3wkq.ap-northeast-2.rds.amazonaws.com', 
                                            user='root', password='qaz51133', db='Project_ML', charset='utf8mb4')

    def disconnectDB(self):
        self.connection.close()

    def closeEvent(self, event):
        # 종료 전에 실행할 코드
        self.disconnectDB()
        
    def updateProgressBar(self, position):
        logging.debug(f"Updating progress bar: {position}")
        self.progressBar.setValue(int((self.totalPosition + position) / 1000))  # 밀리초를 초로 변환

    def click_play(self):
        # self.videoFiles = [
        #     "./gui_user/23_12_14_16_33_31.avi",
        #     "./gui_user/23_12_14_16_34_04.avi",
        #     "./gui_user/23_12_14_16_34_34.avi",
        #     "./gui_user/23_12_14_16_35_05.avi"
        # ]
        self.timelineWidget.setEventPositions([30, 60, 90])  # 이벤트 위치 설정
        self.currentVideoIndex = 0
        self.totalDuration = len(self.videoFiles) * 30 * 1000
        logging.debug(f"click play: total duration {self.totalDuration} ms")
        self.totalPosition = 0
        self.play_video()
        self.progressBar.setStyleSheet("")  # 기본 스타일로 재설정
        
        # pixmap = QPixmap("./gui_user/231214214313.jpg")  # 이미지 경로 설정
        # scaled_pixmap = pixmap.scaled(self.recentImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)  # recentImage 크기에 맞게 조정
        # self.recentImage.setPixmap(scaled_pixmap)
        # self.recentImage.setScaledContents(True)  # 이미지 크기 자동 조절  
        
        # # 재생할 동영상 파일 지정
        # self.recentVideoFile = "./gui_user/23_12_14_16_36_43.avi"  # 동영상 파일 경로 설정

        # # 동영상 파일 재생
        # self.recentMediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.recentVideoFile)))
        # self.recentMediaPlayer.play()
        
    def play_video(self):
        logging.debug(f"Playing video {self.currentVideoIndex + 1}/{len(self.videoFiles)}")  
        if self.currentVideoIndex < len(self.videoFiles):
            # S3 버킷에서 파일의 임시 URL 생성
            url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': self.videoFiles[self.currentVideoIndex]}, ExpiresIn=3600)
            print("video: ", url)
            # 동영상 파일 재생
            self.player.setMedia(QMediaContent(QUrl(url)))
            #self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.videoFiles[self.currentVideoIndex])))
            self.player.play()
        else:
            self.progressBar.setValue(int(self.totalDuration / 1000))  # 밀리초를 초로 변환
            # 재생이 끝났을 때 프로그래스바 스타일 변경
            self.progressBar.setStyleSheet("""
                QProgressBar {
                    border: 2px solid grey;
                    border-radius: 5px;
                    background-color: #FFFFFF;
                }

                QProgressBar::chunk {
                    background-color: #37A2DA;  # 재생 완료 후 색상
                    width: 20px;
                }
            """)

    def onMediaStatusChanged(self, status):
        logging.debug(f"Media status changed: {status}")
        if status == QMediaPlayer.EndOfMedia:
            logging.debug("EndOfMedia")
            self.totalPosition = self.totalPosition + self.player.duration()
            self.currentVideoIndex += 1
            self.play_video()
        elif status == QMediaPlayer.BufferedMedia:
            logging.debug("BufferedMedia")
            self.totalDuration = self.totalDuration + (self.player.duration() - (30 * 1000))
            logging.debug(f"duration {self.player.duration()}, total duration {self.totalDuration} ms")
            self.progressBar.setMaximum(int(self.totalDuration / 1000))  # 밀리초를 초로 변환

    def populate_playlist(self):
        # Add time range items to the playlist
        self.playlist.addItem("Video 1: 00:00 - 00:30")
        self.playlist.addItem("Video 2: 00:30 - 01:00")
        # and so on...

# Run the application
app = QApplication(sys.argv)
gui = WildlifeUserGUI()
gui.show()
sys.exit(app.exec_())

