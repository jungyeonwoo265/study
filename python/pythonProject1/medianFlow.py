import cv2

# 비디오 파일 열기
cap = cv2.VideoCapture('video1.mp4')
if not cap.isOpened():
    print("비디오 열기 실패")
    exit()
else:
    print("비디오 열기 성공")
    # 화면 크기 확인
    tracker = cv2.TrackerCSRT_create()

    ret, img = cap.read()

    bbox =  cv2.selectROI(img, False)
    tracker.init(img, bbox)

while True:
    # 비디오 읽기
    ret, img = cap.read()

    if not ret:
        print("비디오 재생 완료")
        exit()

    success, box = tracker.update(img)

    left, top, w, h = [int(v) for v in box]

    cv2.rectangle(img, pt1=(left,top), pt2=(left+w,top+h), color=(0, 0, 0))

    # 비디오 재생하기
    cv2.imshow("img", img)
    # 비디오 종료 시키기
    if cv2.waitKey(1) == ord("q"):
        print("비디오 강제 종료")
        break

cap.release()
cv2.destroyAllWindows()