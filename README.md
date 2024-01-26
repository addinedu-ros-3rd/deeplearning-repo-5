# 딥러닝 기반의 유해조수 판별 및 추적모델
## 개요
![객체인식 및 추적](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/ef172838-b472-4c3f-b793-b0aeb36b2aa6)
![KakaoTalk_Video_2023-12-15-10-56-23](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/c82cff4b-c50c-486d-a356-474072d838c0)

+ 딥러닝 모델을 사용하여 실시간으로 유해조수를 판별하여 타겟팅을 하는 팬틸트 카메라 어플리케이션과 디바이스.
+ 유해조수 판별 로그와 영상/사진을 클라우드에 업로드하고, 이를 조회할 수 있는 관리자 프로그램.

## 팀원
|이름|역할|
|--------|------|
|팀장 박민재|사용자 GUI|
|이무봉|데이터셋 변환 및 모델학습|
|김태헌|팬틸트 카메라용 객체인식 및 추적 어플리케이션 개발|
|홍석진|데이터베이스 설계|

## 프로젝트 기간
2023.11.16 ~ 2023.12.15 (중 10일)

## 기술스택
|   |   |
|---|---|
|개발환경|<img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white">|
|언어|<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">|
|DB, UI 등|<img src="https://img.shields.io/badge/amazonrds-527FFF?style=for-the-badge&logo=amazonrds&logoColor=white"> <img src="https://img.shields.io/badge/amazons3-569A31?style=for-the-badge&logo=amazons3&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/qt-41CD52?style=for-the-badge&logo=qt&logoColor=white">, OpenCV|
|AI|Pytorch|
|개발환경|VScode, Colab|
|형상관리 및 협업|Github, Slack|

## 시스템 구성도
![system_architecture](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/1a61b83c-ea2a-42cd-af16-a938abc7ce6c)

## 기능 리스트
+ 팬틸트 카메라 어플리케이션 및 디바이스
  + YOLOv8 모델과 openCV로 유해조수 탐지
  + 로컬과 AWS에 인식한 객체 로그 데이터와 녹화 영상을 업로드
## 객체인식 및 추적
|    |  |
|--------|------|
|  |   데이터셋 변환 및 모델학습   |
|  |      |
|  |   객체인식 및 추적   |
|  |     |

## GUI
|    |  |
|--------|------|
|  |   데이터셋 변환 및 모델학습   |
|  |   개발자  GUI  |
|  |   ![GUI 이미지](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/66404ce3-e573-463d-a453-2d199418e26e)   |
|  | 사용자 GUI   |
|  |<img width="603" alt="KakaoTalk_Photo_2023-12-15-10-41-42" src="https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/1d986c97-f77e-478a-8929-c2e1387196fb">|  

|    |  |
|----------------|---------------|
|   ![KakaoTalk_Video_2023-12-15-10-56-23 2](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/e22c7dd1-bdc4-4bd1-bcbb-5e937e14fd90) |  |


## 프로젝트 수행 방향
### 1. 딥러닝 (1주차 ~ 3주차)
   - 데이터 수집
   - 데이터 라벨링
   - 개체 인식
   - 개체 추적

### 2. 딥러닝 적용 APP 및 Device (2주차 ~ 3주차)
   - 카메라 팬틸트 컨트롤
   - 레이저 포인터 컨트롤
   - 카메라 영상 스트리밍 (웹캠)
   - 카메라 Application (PC 앱 or 웹앱)
       - 동작 영상 뷰어
       - 사용자 이미지 업로드

### 3. 시스템 통합 (3주차)
### 4. 테스트 및 최종 정리 (4주차)

## 구현 내용

### 1. 객체 인식(Object Detection)
   - 기술 선택: 딥 러닝 기반 모델(예: YOLO, SSD, Faster R-CNN)
   - 데이터 준비: 훈련 데이터 수집 및 라벨링
   - 모델 훈련: 수집한 데이터로 모델 훈련


### 2. 개체 추적(Object Tracking)
   - 추적 알고리즘 선택: Kalman 필터, Mean-shift, CAMShift 등
   - 알고리즘 통합: 인식된 개체 정보 추적


| train_batch |  |  |
|--------|------|------|
| ![train_batch0](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/83ff5be5-7610-4b03-9e7d-9792d1ff160c) | ![train_batch1](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/c8a8956c-8fd3-4860-9aa6-08008183189c) | ![train_batch2](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/1c03fea3-c96d-4f21-bc32-a90576d23d70) |
| ![train_batch145880](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/1d560c68-7118-4ca3-b550-fbd90cb43b88) | ![train_batch145881](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/ddbea988-73bd-4d30-b47a-fbe57b480c6b) | ![train_batch145882](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/ca0ee812-9c6e-4edb-a4af-f9480345a177) |
||||
|  ![val_batch0_labels](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/ca67e2eb-7446-449d-8e60-028f3c28bc8c) |  ![val_batch0_pred](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/ef2bde67-f4d1-4c8e-84e8-f3dcd3c6d4ac) |  ![val_batch1_labels](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/6c49c6ab-b989-4e45-bc27-b9b7d4ef61a6)
 |
 |  ![val_batch1_pred](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/1bea6d89-b100-4525-828a-fc7a707faea1) |  ![val_batch2_labels](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/a75a1379-c219-4b66-8c43-bb3d9efdd52c) |  ![val_batch2_pred](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/db7a02b2-716b-4306-b286-10fe9ada81d2)
 |
|   |   |   |
|   |   |   |
![image](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/1d4e6bfc-6785-4bac-88bb-f0d2529fc642)

### 3. 카메라 제어(Camera Control)
   - 서보 모터 제어: 카메라 각도 조절
   - 소프트웨어 통합: 카메라 자동 움직임 제어

### 4. 시스템 통합 및 최적화
   - 성능 평가: 시스템 정확도 및 반응 속도 평가
   - 최적화: 모델 및 알고리즘 수정 및 최적화

|   |   |   |
|--------|------|------|
|   |  ![confusion_matrix_normalized](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/5cdf6a7c-bc07-495c-a23b-95d6e643b8bb) |  ![confusion_matrix](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/e0623278-c60d-46eb-9588-9d985a11275e) |


### 5. 실제 환경 테스트
   - 테스트 실행: 다양한 환경에서 시험
   - 문제 해결: 테스트 중 발견된 문제 해결

## 프로젝트 수행 도구
- Git Hub
- YOLO v8
- AWS
- mySQL(RDS)
- 웹캠

## 공유하고 싶은 팁

- colab 보다 노트북이 2.5배 빨랐다 !
- 적합한 라벨링 기준 !
![image](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/bec2004f-e80b-4ef0-b52c-94cbaddf0891)
- 

