import socket

HOST = "10.50.42.217"
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("전송할 메시지를 입력하세요: ")
        s.sendall(message.encode())