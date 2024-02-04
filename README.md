# 딥러닝 기반의 유해조수 판별 및 추적모델
## 개요
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
|DB, UI 등|<img src="https://img.shields.io/badge/amazonrds-527FFF?style=for-the-badge&logo=amazonrds&logoColor=white"> <img src="https://img.shields.io/badge/amazons3-569A31?style=for-the-badge&logo=amazons3&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/qt-41CD52?style=for-the-badge&logo=qt&logoColor=white"> <img src="https://img.shields.io/badge/opencv-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white">|
|AI|<img src="https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white">|
|개발환경|<img src="https://img.shields.io/badge/visualstudiocode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white"> <img src="https://img.shields.io/badge/googlecolab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white">|
|형상관리 및 협업|<img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"> <img src="https://img.shields.io/badge/slack-4A154B?style=for-the-badge&logo=slack&logoColor=white">|

## 시스템 구성도
![system_architecture](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/1a61b83c-ea2a-42cd-af16-a938abc7ce6c)

## 기능 리스트
+ 팬틸트 카메라 어플리케이션 및 디바이스
  + YOLOv8 모델과 openCV로 유해조수 탐지
  + 로컬과 AWS에 인식한 객체 로그 데이터와 녹화 영상 및 캡쳐 이미지를 업로드
+ 사용자 UI 프로그램
  + 팬틸트 카메라 선택 선택하여 해당 카메라 실시간 영상 조회
  + 탐지 결과와 녹화 영상, 캡쳐 이미지 조회
+ 데이터 저장 서버(DB)
  + 탐지 결과에 대한 정보, 녹화 영상과 캡쳐 이미지를 클라우드에 저장

## 객체 리스트
|   |   |   |
|---|---|---|
|고라니|노루|너구리|
|멧돼지|반달곰|토끼|
|얼룩다람쥐|다람쥐|백로|
|족제비|왜가리| |

## 탐지 및 퇴치 장치 GUI
![image](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146147393/fa4e1367-65cc-444b-89c9-39f50fd4f579)

① 실시간 영상  
② 녹화 영상 및 캡쳐 이미지 조회: Open File 버튼으로 로컬에 저장된 영상/이미지 파일 조회  
③ 객체 검출 정보: 검출 시간, 객체 정보, 경계박스 좌표에 대한 raw 데이터, 녹화 영상 및 캡쳐 이미지 저장 경로를 표시  

## 사용자 프로그램 GUI
![image](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146147393/3084dda8-8920-40ac-9804-07512545b0b8)

① 팬틸트 카메라 디바이스 선택  
② 실시간 영상
  + (좌) 바운딩 박스가 있는 영상
  + (우) 바운딩 박스가 없는 원본 영상
  
③ 유해조수 출현 기록 리스트: 유해조수가 검출된 시간을 선택하면 해당 영상 파일을 재생  
④ 출현 기록 영상 플레이어  

### 사용자 프로그램 GUI 사용법
1.팬틸트 카메라 디바이스 선택  
2.출현 기록 리스트 중 조회하고 싶은 시간을 선택  
3.녹화 기록 영상 플레이어를 통해 기록 시청  

## 설계 - 개발 일정
### 1. 딥러닝 스터디 (1주차 ~ 3주차)
   - 데이터 수집 및 라벨링
   - 개체 인식 및 추적 모델 구축

### 2. 팬틸트 카메라 APP 개발 및 딥러닝 성능개선 (2주차 ~ 3주차)
|**구분**|**역할**|
|---|---|
|이무봉, 박민재|Epoch 및 batch size 등 파라미터 조절 및 클래스 추가 등 방법을 통한 성능 개선|
|김태헌|팬틸트 카메라용 GUI 개발: PyQt 내에서 실시간 영상과 딥러닝 모델 통합|
|홍석진|DB 구축|

### 3. 시스템 통합 (3주차)
|**구분**|**역할**|
|---|---|
|박민재|Epoch 및 batch size 등 파라미터 조절 및 클래스 추가 등 방법을 통한 성능 개선|
|이무봉|사용자 GUI 개발: DB로부터 검출 기록을 선택 후 이에 대한 비디오 플레이어 개발|
|김태헌|팬틸트 카메라용 GUI 개발: 객체 인식 정보 및 영상/이미지를 AWS RDS와 AWS S3에 업로드|

### 4. 테스트 및 최종 정리 (4주차)
   - 사용자 프로그램과 팬틸트 카메라 APP 연동
   - 코드 디버깅

## 구현 및 결과
### GUI
|**팬틸트 카메라 APP**|**사용자 프로그램**|
|---|---|
|![객체인식 및 추적](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/ef172838-b472-4c3f-b793-b0aeb36b2aa6)|![KakaoTalk_Video_2023-12-15-10-56-23](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/c82cff4b-c50c-486d-a356-474072d838c0)|

### 모델 성능
|   |   |
|---|---|
|  ![confusion_matrix_normalized](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/5cdf6a7c-bc07-495c-a23b-95d6e643b8bb) |  ![confusion_matrix](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/e0623278-c60d-46eb-9588-9d985a11275e) |

## 회고
* 결론
  + 학습한 클래스의 종류가 적어 오버피팅 현상 발생.
  + 학습한 클래스의 종류를 늘렸으나, 사용했던 공공 데이터셋의 품질이 좋지 않았기 때문인지 마찬가지로 현상 발생.
  + 다양한 클래스와 많은 데이터셋의 수가 중요하지만, 데이터 품질이 모델에 가장 큰 영향을 끼친다.
* 아쉬운 점
  + Jetson Nano와 서보모터를 사용하여 개발하려고 했으나 디바이스의 Ubuntu와 Python 버전과 YOLOv8의 최소 요구사항 문제로 구현을 하지 못한 점.
  + DeepSORT, IOU Tracker, Kalman Filter와 같은 추적 알고리즘을 구현 및 적용하지 못한 점.

## 공유하고 싶은 팁

- colab 보다 노트북이 2.5배 빨랐다 !
- 적합한 라벨링 기준 !
![image](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/bec2004f-e80b-4ef0-b52c-94cbaddf0891)
- 

