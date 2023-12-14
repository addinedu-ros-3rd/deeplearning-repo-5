# 필요 라이브러리
# !pip install boto3 pyqt5 pymysql

# 필요 인증파일
# ~/.aws/credentials

# AWS S3 클라이언트 설정
# s3_client = boto3.client('s3', region_name='ap-northeast-2')
# bucket_name = 'prj-wildlife'

import sys
import pymysql

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QTreeWidget, QSplitter, QVBoxLayout, QLabel, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDateTime

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 메인 윈도우 설정
        self.setWindowTitle("Animal Detecting System")
        #self.showMaximized()
        self.resize(1600, 1000)  # 윈도우 크기를 800x800으로 설정


        # 중앙 위젯과 레이아웃 설정
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 상단 레이블
        top_label = QLabel("Animal Detecting System", self)
        top_label.setAlignment(Qt.AlignCenter)
        
        # 글꼴 및 크기 설정
        font = QFont("Arial", 20, QFont.Bold)  # Arial 글꼴, 20pt 크기, 굵은 글씨
        top_label.setFont(font)
        
        # 스타일 시트 설정 (옵션)
        top_label.setStyleSheet("background-color: rgb(0, 0, 102);color: rgb(255, 255, 255);border: 10px solid black;")
        main_layout.addWidget(top_label)

        # 전체 스플리터 (상단 및 하단)
        main_splitter = QSplitter(Qt.Vertical)

        # 중앙 스플리터 (이미지 및 비디오 뷰)
        center_splitter = QSplitter(Qt.Horizontal)

        image_view = QLabel("Image View")
        font = QFont("Arial", 10, QFont.Bold) 
        image_view.setFont(font)
        image_view.setAlignment(Qt.AlignCenter)
        image_view.setStyleSheet("background-color: lightgreen; border: 2px solid black;")
        video_view = QLabel("Video View")
        font = QFont("Arial", 10, QFont.Bold) 
        video_view.setFont(font)
        video_view.setAlignment(Qt.AlignCenter)
        video_view.setStyleSheet("background-color: lightyellow; border: 2px solid black;")

        center_splitter.addWidget(image_view)
        center_splitter.addWidget(video_view)
        
        # 하단 스플리터 (중앙 스플리터 및 정보 테이블)
        bottom_splitter = QSplitter(Qt.Horizontal)

        self.info_table = QTableWidget()
        self.info_table.setRowCount(10)
        self.info_table.setColumnCount(3)
        self.info_table.setStyleSheet("background-color: lightgray; border: 1px solid black;")

        # 트리 위젯 설정
        tree_widget = QTreeWidget()
        tree_widget.setHeaderLabel("Tree View - s3://prj-wildlife/")

        # 테이블 정보 레이블 추가
        self.table_info_label = QLabel("Table: detect_log - Last Updated: ", self)
        font = QFont("Arial", 10, QFont.Bold)
        self.table_info_label.setFont(font)
        
        # 테이블 정보 레이블과 테이블 위젯을 포함하는 새로운 수직 레이아웃
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table_info_label)
        table_layout.addWidget(self.info_table)
        
        # 새로운 레이아웃을 포함하는 컨테이너 위젯
        table_container = QWidget()
        table_container.setLayout(table_layout)

        bottom_splitter.addWidget(table_container)
        bottom_splitter.addWidget(tree_widget)
        bottom_splitter.setSizes([350, 150])  # 중앙 스플리터와 정보 테이블의 높이 비율 설정

        # 전체 스플리터에 위젯 추가 및 높이 비율 설정
        main_splitter.addWidget(center_splitter)
        main_splitter.addWidget(bottom_splitter)
        main_splitter.setSizes([600, 400])  # 중앙과 하단 영역의 높이 비율 설정

        main_layout.addWidget(main_splitter)

        # 데이터베이스에서 데이터 가져오기
        self.loadTableData()


    def loadTableData(self):
        # 데이터베이스 연결 설정
        connection = pymysql.connect(   host='database-1.ciifx43v3wkq.ap-northeast-2.rds.amazonaws.com', 
                                        user='root', password='qaz51133', db='Project_ML', charset='utf8mb4')
        # 현재 시간 업데이트
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.table_info_label.setText(f"Table: detect_log - Last Updated: {current_time}")

        try:
            with connection.cursor() as cursor:
                # 데이터 조회 쿼리
                sql = "SELECT * FROM detect_log ORDER BY time DESC"
                cursor.execute(sql)
                results = cursor.fetchall()

                # 컬럼명 설정
                column_names = [column[0] for column in cursor.description]
                self.info_table.setColumnCount(len(column_names))
                self.info_table.setHorizontalHeaderLabels(column_names)

                # 테이블 위젯 설정
                self.info_table.setRowCount(len(results))

                for row_idx, row_data in enumerate(results):
                    for col_idx, col_data in enumerate(row_data):
                        self.info_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

                # 컬럼 너비를 내용에 맞게 조절
                header = self.info_table.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.ResizeToContents)

                # 컬럼 너비 저장
                column_widths = [header.sectionSize(column) for column in range(len(column_names))]

                # Interactive 모드로 변경
                header.setSectionResizeMode(QHeaderView.Interactive)

                # 저장된 컬럼 너비를 다시 적용
                for column, width in enumerate(column_widths):
                    self.info_table.setColumnWidth(column, width)

        finally:
            connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
