import datetime
import cv2
from ultralytics import YOLO

CONFIDENCE_THRESHOLD = 0.7  # 최소 정확도
# 경계박스 색깔
GREEN = (0, 255, 0)  # 사람의 경우 초록색
RED = (0, 0 , 255)  # 타겟의 경우(사슴, 멧돼지) 빨간색
WHITE = (255, 255, 255) # 경계박스 글씨 색 하얀색


# 객체 이름을 확인하기 위한 
coco128 = open('/home/wintercamo/dev_ws/DL/src/cooc128.txt', 'r')
data = coco128.read()
class_list = data.split('\n')
coco128.close()

model = YOLO('/home/wintercamo/dev_ws/DL/src/runs/detect/train3/weights/best.pt')  # 학습 모델 불러오기

# 웹캠 설정
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    start = datetime.datetime.now()  # FPS를 표시하기 위해 현재 시간 가져옴.

    ret, frame = cap.read()

    if not ret:
        print('Cam Error')
        break

    detection = model(frame)[0]  # 학습 모델에 웹캠 영상을 넣어서 detection 결과를 변수에 대입

    # data : [xmin, ymin, xmax, ymax, confidence_score(정확도), class_id]
    for data in detection.boxes.data.tolist():
        confidence = float(data[4])
        
        # 대상이 최소 정확도보다 낮으면 무시
        if confidence < CONFIDENCE_THRESHOLD:
            continue  

        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])  # 경계박스의 너비, 높이 좌표
        label = int(data[5])  # 인식한 객체의 라벨(이름)

        if label == 2:
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), GREEN, 2)
        else:
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), RED, 2)
        cv2.putText(frame, class_list[label]+' '+str(round(confidence, 2)) + '%', (xmin, ymin), cv2.FONT_ITALIC, 1, WHITE, 2)

    end = datetime.datetime.now()  # FPS 종료

    # 상단에 FPS 표시하는 코드
    total = (end - start).total_seconds()
    print(f'Time to process 1 frame: {total * 1000:.0f} milliseconds')

    fps = f'FPS: {1 / total:.2f}'
    cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()