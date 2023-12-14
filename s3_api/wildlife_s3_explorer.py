# 필요 라이브러리
# !pip install boto3 pyqt5

# 필요 인증파일
# ~/.aws/credentials

# AWS S3 클라이언트 설정
# s3_client = boto3.client('s3', region_name='ap-northeast-2')
# bucket_name = 'prj-wildlife'


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
import boto3

class S3Explorer(QWidget):
    def __init__(self, s3_client, bucket_name):
        super().__init__()
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(['Name', 'Size', 'Last Modified'])
        self.layout.addWidget(self.tree)

        self.populateTree()

    def selectFileInTreeWithPath(self, file_path):
        parts = file_path.split('/')
        current_item = self.tree.invisibleRootItem()  # 루트에서 시작

        for part in parts:
            found = False
            # 현재 항목의 자식들을 순회
            for i in range(current_item.childCount()):
                child = current_item.child(i)
                if child.text(0) == part:
                    current_item = child  # 다음 경로 부분을 위해 현재 항목 업데이트
                    found = True
                    break
            if not found:
                return  # 경로에 해당하는 항목을 찾지 못함

            if part != parts[-1]:  # 마지막 부분이 아니면 확장
                current_item.setExpanded(True)

        self.tree.setCurrentItem(current_item)  # 마지막 항목 선택

    def populateTree(self):
        response = self.s3_client.list_objects(Bucket=self.bucket_name)
        tree_dict = {"/": self.tree}

        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                size = obj['Size']
                last_modified = obj['LastModified'].strftime("%Y-%m-%d %H:%M:%S")

                parts = key.split('/')
                path = ""

                for part in parts[:-1]:
                    if part:
                        path = path + "/" + part if path else part
                        if path not in tree_dict:
                            parent_path = "/".join(path.split('/')[:-1])
                            parent = tree_dict[parent_path] if parent_path else self.tree
                            tree_dict[path] = QTreeWidgetItem(parent, [part])
                        parent = tree_dict[path]

                if parts[-1]:  # 파일 추가
                    QTreeWidgetItem(parent, [parts[-1], str(size), last_modified])

# AWS S3 클라이언트 설정 및 애플리케이션 실행
if __name__ == '__main__':
    app = QApplication(sys.argv)
    s3_client = boto3.client('s3', region_name='ap-northeast-2')
    bucket_name = 'prj-wildlife'
    ex = S3Explorer(s3_client, bucket_name)
    ex.show()
    ex.selectFileInTreeWithPath('image/20231214/image_20231214205800.jpg')  # 여기서 'your-file-name'을 원하는 파일 이름으로 변경하세요.
    sys.exit(app.exec_())
