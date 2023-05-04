# fashion_pose.py : MPII를 사용한 신체부위 검출
import cv2

# MPII에서 각 파트 번호, 선으로 연결될 POSE_PAIRS
BODY_PARTS = {"Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
              "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
              "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
              "Background": 15}

POSE_PAIRS = [["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
              ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
              ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
              ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"]]

# 각 파일 path
protoFile = "C:\\Users\\Kiot\\PycharmProjects\\pythonProject1\\pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "C:\\Users\\Kiot\\PycharmProjects\\pythonProject1\\pose_iter_160000.caffemodel"

# 위의 path에 있는 network 불러오기
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

cap = cv2.VideoCapture("video1.mp4")

if not cap.isOpened():
    print("exit")
    exit()
else:
    print("open")

while True:
    # 비디오 읽기
    ret, img = cap.read()

    if not ret:
        print("비디오 재생 완료")
        exit()

    imgH, imgW, _ = img.shape
    # 네트워크에 입력하기 위해 이미지 전처리
    inpBlob = cv2.dnn.blobFromImage(img, 1.0/255, (imgW, imgH), (0,0,0), swapRB=False, crop=False)
    # 전처리된 이미지 네트워크에 입력
    net.setInput(inpBlob)
    # 결과 받아오기
    output = net.forward()
    # EX) output.shape = (1, 15, 44, 44) : 1은 이미지 ID, 15은 감지된 사람 수, 44x44는 출력 맵의 크기
    H = output.shape[2]
    W = output.shape[3]
    # 결과 출력
    # print("이미지 ID : ", len(output[0]), ", H : ", output.shape[2], ", W : ", output.shape[3])  # 이미지 ID
    # 각 파트 검출하기
    points = []
    for i in range(15):
        # 해당 신체 부위 신뢰도 얻기
        probMap = output[0, i, :, :]
        # 가장 높은 확률을 가진 좌표값 찾기
        minVal, prob, minloc, point = cv2.minMaxLoc(probMap)
        # 원래 이미지에 맞게 좌표 변환
        x = (imgW * point[0])/W
        y = (imgH * point[1])/H
        # print(f"point {i} - prob : {prob}")
        # 신로도로 신체부위 위치 표시
        if prob > 0.1:
            cv2.circle(img, (int(x), int(y)), 3, (0, 255, 255), thickness=-1,
                       lineType=cv2.FILLED)  # circle(그릴곳, 원의 중심, 반지름, 색)
            cv2.putText(img, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
                        lineType=cv2.LINE_AA)
            points.append((int(x), int(y)))
        else:
            points.append(None)
    # 원본 이미지에 인식된 부위와 연결선을 그릴 이미지 생성
    imgCopy = img
    # print(f"POSE_PAIRS : {POSE_PAIRS}")
    # print(f"points : {points}")

    # 각 POSE_PAIRS에 해당하는 신체부위 연결
    for pair in POSE_PAIRS:
        partA = pair[0]  # Head
        partA = BODY_PARTS[partA]  # 0
        partB = pair[1]  # Neck
        partB = BODY_PARTS[partB]  # 1

        print(partA, " 와 ", partB, " 연결\n")
        if points[partA] and points[partB]:
            # 각 부위와 연결선 그리기
            cv2.line(imgCopy, points[partA], points[partB], (0, 255, 0), 2)
    # 연결선을 만든 이미지를 출력
    cv2.imshow("Output-Keypoints", imgCopy)
    # 비디오 종료 시키기
    if cv2.waitKey(1) == ord("q"):
        print("비디오 강제 종료")
        break

# 카메라 해제
cap.release()
# 모든 윈도우 종료
cv2.destroyAllWindows()