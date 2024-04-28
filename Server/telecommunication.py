import socket
import NLP
import path


HOST = '0.0.0.0'  # 모든 인터페이스에서 연결을 수락
PORT = 1234     # 사용할 포트 번호

NLP.processing("나는 복지관 가고 싶어")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("서버 시작, 클라이언트 연결 대기 중...")
    while True:
        conn, addr = s.accept()
        with conn:
            print('클라이언트와 연결됨:', addr)
            while True:
                original = conn.recv(1024)
                if not original:
                    print('클라이언트가 연결을 종료했습니다.')
                    break
                data = original.decode("utf-8")
                print('수신된 데이터:', data)
                split_data = data.split("|")
                string = split_data[0]
                latitude = float(split_data[1])
                longitude = float(split_data[2])
                print(string)
                

                dest = NLP.processing(string) # revise to extract the destination
                print(dest)
                way_to_des = path.returnpath(dest, latitude, longitude)
                print("path:", way_to_des) # revise to send path
                conn.sendall(way_to_des.encode()) # revise to encode path