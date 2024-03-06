import socket

HOST = "10.50.42.217"
PORT = 1234

def transmit():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #전송부
        s.connect((HOST, PORT))
        message_destination = input("전송할 메시지를 입력하세요: ")
        message_latitude = 37.2974415 #example
        message_longitude = 126.8355968 #example
        message = f"{message_destination}|{message_latitude}|{message_longitude}"
        s.sendall(message.encode())

        #수신부
        data = s.recv(1024)
        entity = data.decode("utf-8")
        print("개체: ", entity) ## extract route algorithm
        splitted_entity = entity.split("|")

        return splitted_entity