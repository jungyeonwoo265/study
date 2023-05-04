import json
import socketserver
import pickle
import threading
from datetime import timedelta, datetime
import cv2, dlib
import numpy as np
from imutils import face_utils
from keras.models import load_model
import struct


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        (IP, PORT) = self.client_address
        client = self.request, (IP, PORT)
        # print(client)

        if client not in MultiServerObj.clients:
            MultiServerObj.clients.append(client)
            print(f"{datetime.now().strftime('%D %T')}\n{IP} : {PORT} 가 연결되었습니다.")
        MultiServerObj.receive_messages(self.request)


# 멀티 클라이언트를 서비스하기 위해서 두 개의 클래스를 부모로 갖는 파생 클래스 생성
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass  # 아무일도 하지 않기 때문에 pass 넣음


class MultiServer:
    def __init__(self):
        self.clients = []  # 접속된 클라이언트 소켓 목록을 넣을 모든 클라이언트 소켓 저장 리스트

    # 클라이언트에서 요청이 오면 실행될 함수
    def receive_messages(self, client_socket):
        face_cascade = cv2.CascadeClassifier("C:/Users/kdt/haarcascade_frontalface_default.xml")
        left_eye_cascade = cv2.CascadeClassifier("C:/Users/kdt/haarcascade_lefteye_2splits.xml")
        right_eye_cascade = cv2.CascadeClassifier("C:/Users/kdt/haarcascade_righteye_2splits.xml")
        model = load_model("C:/Users/kdt/model.h5")
        status1 = 5
        status2 = 5
        while True:
            data = b''
            video = b''
            #try:
            packet = client_socket.recv(4)
            #if len(packet) > 0:
            total_len = int.from_bytes(packet, byteorder='little', signed=True)
            data_len = 0
            while(total_len > data_len):
                data = client_socket.recv(total_len-data_len)
                data_len += len(data)
                # 데이터 더해주는거
                video += data

            print('video 길이:', len(video))
            print('data 길이1:', len(data))

            img_array = np.frombuffer(video, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            # 눈 검출 및 모델 예측 부분
            height, width, _ = img.shape
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]

                left_eye = left_eye_cascade.detectMultiScale(roi_gray)
                right_eye = right_eye_cascade.detectMultiScale(roi_gray)

                for (x1, y1, w1, h1) in left_eye:
                    cv2.rectangle(roi_color, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 1)
                    eye1 = roi_color[y1:y1 + h1, x1:x1 + w1]
                    eye1 = cv2.resize(eye1, (86, 86))
                    eye1 = np.expand_dims(eye1, axis=0)
                    pred1 = model.predict(eye1)
                    print(f"감았을때 예측 : {pred1}")
                    status1 = np.argmax(pred1)
                    print(f"status1 : {status1}")
                    break

                for (x2, y2, w2, h2) in right_eye:
                    cv2.rectangle(roi_color, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 1)
                    eye2 = roi_color[y2:y2 + h2, x2:x2 + w2]
                    eye2 = cv2.resize(eye2, (86, 86))
                    eye2 = np.expand_dims(eye2, axis=0)
                    pred2 = model.predict(eye2)
                    print(f"떴을때 예측 : {pred2}")
                    status2 = np.argmax(pred2)
                    print(f"status2 : {status2}")
                    break

                # If the eyes are closed, start counting

                if status1 == 1 and status2 == 1:
                    client_socket.send(status1.to_bytes(4, 'little'))
                    count += 1
                    cv2.putText(img, "Eyes Closed, Frame count: " + str(count), (10, 30), cv2.FONT_HERSHEY_COMPLEX,
                                1, (0, 0, 255), 1)
                    if count >= 10:
                        cv2.putText(img, "Drowsiness Alert!!!", (100, height - 20), cv2.FONT_HERSHEY_COMPLEX, 1,
                                    (0, 0, 255), 2)

                else:
                    client_socket.send(status1.to_bytes(4, 'little'))
                    cv2.putText(img, "Eyes Open", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
                    count = 0

                #try:
                    #ret, frame = img.read()

                cv2.imshow('image', img)



                if cv2.waitKey(1) == ord('q'):
                    img.release()
                    cv2.destroyAllWindows()
                    print('4')
                # data = b''
            #     except:
            #         pass
            #
            # except json.JSONDecodeError as e:
            #     print("json 에러")
            #     break
            # except:
            #     print("에러")
            #     break


if __name__ == "__main__":

    MultiServerObj = MultiServer()  # MultiServer클래스의 객체 생성
    host, port = '10.10.21.109', 9000
    '''
        # 아래 코드와 비슷하게 돌아감. with를 사용해서 만들어보고 싶었음
        server = ThreadedTCPServer((host, port), TCPHandler)
        server.serve_forever()
    '''
    # socketserver을 이용해서 TCP 서버 소켓 객체 생성
    with ThreadedTCPServer((host, port), TCPHandler) as server:
        server.serve_forever()  # 서버를 실행하고 서비스를 무한 반복한다