# deeplearning-repo-5

## 과정명
ROS (SLAM/RAIDA) 개발 역량 강화를 위한 AI 자율주행 로봇 과정

## 팀명
| 팀명   | 헌터 x 헌태 |
|--------|------|
|  |   ![DALL·E 2023-12-14 17 46 51 - Modify the existing logo of a project focused on protecting crops from pests such as wild boars and deer by adding stylish sunglasses to both the wild](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/669b227d-648e-48bb-bbbc-670394ee2771)   |

## 팀원
| 이름   | 역할 |
|--------|------|
| 이무봉 |   데이터셋 변환 및 모델학습   |
| 박민재 |   사용자 GUI   |
| 김태헌 |   객체인식 및 추적   |
| 홍석진 |   데이터베이스 설계   |

## 프로젝트 주제
딥러닝 기반의 유해조수 판별 및 추적모델 구축

## 프로젝트 목적
유해조수 판별 및 추적 모델 구축

## 시스템 구성도
![system_architecture](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/1a61b83c-ea2a-42cd-af16-a938abc7ce6c)

## 객체인식 및 추적
|    |  |
|--------|------|
|  |   데이터셋 변환 및 모델학습   |
|  |      |
|  |   객체인식 및 추적   |
|  |   ![객체인식 및 추적](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/ef172838-b472-4c3f-b793-b0aeb36b2aa6)   |

## GUI
|    |  |
|--------|------|
|  |   데이터셋 변환 및 모델학습   |
|  |   GUI   |
|  |   객체인식 및 추적   |
|  |   ![GUI 이미지](https://github.com/addinedu-ros-3rd/deeplearning-repo-5/assets/146153434/66404ce3-e573-463d-a453-2d199418e26e)   |



## 프로젝트 수행 방향
### 1. 딥러닝 (1주차 ~ 3주차)
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


| rain_batch |  |  |
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

### 3. 카메라 제어(Camera Control)
   - 서보 모터 제어: 카메라 각도 조절
   - 소프트웨어 통합: 카메라 자동 움직임 제어

### 4. 시스템 통합 및 최적화
   - 성능 평가: 시스템 정확도 및 반응 속도 평가
   - 최적화: 모델 및 알고리즘 수정 및 최적화

### 5. 실제 환경 테스트
   - 테스트 실행: 다양한 환경에서 시험
   - 문제 해결: 테스트 중 발견된 문제 해결

## 프로젝트 수행 도구
- Git Hub
- Python3
- 라즈베리파이
- 팬틸트 카메라



