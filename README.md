# deeplearning-repo-5
과정명 : ROS (SLAM/RAIDA) 개발 역량 강화를 위한 AI 자율주행 로봇 과정

### 팀명 : 헌터x헌태
### 팀원 : 이무봉, 박민재, 김태헌, 홍석진
### 
### 프로젝트 주제 : 딥러닝 기반의 유해조수 판별 및 추적모델 구축
### 프로젝트 목적 : 유해조수 판별 및 추적 모델 구축
### 
### 프로젝트 수행 방향
방향 및 일정 ( 전체 일정 4주)

1. 딥러닝 ( 1주차  ~ 3 주차) 
   1. 개체 인식
   2. 개체 추적
2. 딥러닝 적용 APP 및 Device (2 주차 ~ 3주차)
   1. 카메라 팬틸트 컨트롤
   2. 레이저 포인터 컨트롤
   3. 카메라 영상 스트리밍 (웹캠)
   4. 카메라 Application  (PC 앱 or 웹앱)
      1. 동작 영상 뷰어
      2. 사용자 이미지 업로드
3. 시스템 통합 (3 주차)
4.  테스트 및 최종 정리 (4 주차)

구현 내용
1. 개체 인식(Object Detection): 
   - 기술 선택: 딥 러닝 기반 모델(예: YOLO, SSD, Faster R-CNN)을 사용하여 실시간으로 개체를 인식할 수 있습니다.
   - 데이터 준비: 훈련 데이터를 수집하고 라벨링합니다. 이 단계는 선택한 모델의 정확도에 크게 영향을 미칩니다.
   - 모델 훈련: 수집한 데이터를 사용하여 모델을 훈련합니다. 이 과정은 컴퓨터의 성능에 따라 시간이 다소 걸릴 수 있습니다.

2. 개체 추적(Object Tracking):
   - 추적 알고리즘 선택: Kalman 필터, Mean-shift, CAMShift, 혹은 딥 러닝 기반 추적 알고리즘 중 선택합니다.
   - 알고리즘 통합: 인식된 개체에 대한 정보(위치, 크기 등)를 추적 알고리즘에 통합합니다. 이를 통해 개체가 움직일 때 이를 추적할 수 있습니다.

3. 카메라 제어(Camera Control):
   - 서보 모터 제어: 카메라를 움직이기 위해 서보 모터를 사용합니다. 서보 모터는 추적 대상의 위치에 따라 카메라의 각도를 조절합니다.
   - 소프트웨어 통합: 개체의 위치 변경에 따라 카메라가 자동으로 움직일 수 있도록 제어 알고리즘을 개발하고 소프트웨어에 통합합니다.

4. 시스템 통합 및 최적화:
   - 성능 평가: 시스템의 정확도와 반응 속도를 평가합니다.
   - 최적화: 필요에 따라 모델과 알고리즘을 수정하고 최적화하여 더 나은 성능을 얻습니다.

5. 실제 환경 테스트:
   - 테스트 실행: 다양한 환경과 조건에서 시스템을 테스트하여 신뢰성을 확보합니다.
   - 문제 해결: 테스트 중 발견된 문제점을 해결합니다.

### 프로젝트 수행 도구
Git hub
python3
라즈베리파이
펜틸트 카메라

### 


