import socket

HOST = "10.50.42.217"
PORT = 12345

def telecom():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #전송부
        s.connect((HOST, PORT))
        message = input("전송할 메시지를 입력하세요: ")
        s.sendall(message.encode())

        #수신부
        data = s.recv(1024)
        entity = data.decode("utf-8")

        return entity
    