import socket

HOST = "172.20.10.9"
PORT = 1234

def telecom(message_destination, message_latitude, message_longitude):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #전송부
        s.connect((HOST, PORT))
        #message_destination = input("전송할 메시지를 입력하세요: ")
        #message_latitude = 37.2974415 #example
        #message_longitude = 126.8355968 #example
        message = f"{message_destination}|{message_latitude}|{message_longitude}"
        s.sendall(message.encode())

        #수신부
        data = s.recv(1024)
        entity = data.decode("utf-8")
        print("경로: ", entity) ## extract route algorithm
        
        return entity
