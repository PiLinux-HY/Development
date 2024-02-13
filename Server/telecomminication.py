import socket

HOST = '0.0.0.0'  # 모든 인터페이스에서 연결을 수락
PORT = 12345      # 사용할 포트 번호

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("서버 시작, 클라이언트 연결 대기 중...")
    conn, addr = s.accept()
    with conn:
        print('클라이언트와 연결됨:', addr)
        while True:
            original = conn.recv(1024)
            if not original:
                break
            data = original.decode
            print('수신된 데이터:', data)