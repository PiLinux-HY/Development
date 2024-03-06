import recording
import playing
import RPI.GPIO as GPIO
import transmitting_module
import threading
import stt_module_wav
import threading
import queue

button_pin = 27

global flag
flag = 0
a = 1 

def buttonPressed(channel) :
    flag = flag + 1

lat = queue.Queue()
lon = queue.Queue()

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN)
GPIO.add_event_detect(button_pin, GPIO.RISING)
GPIO.add_event_callback(button_pin,buttonPressed)

def t1_main():
    try:
        while True:
            if flag == 1:
                playing.play("/home/piLinux2/Desktop/goal.wav") # please tell me destination
                recording.audio()
                stt_module_wav.transcribe_audio("/home/piLinux2/Desktop/output.wav")
                playing.play("/home/piLinux2/Desktop/finding.wav") # 목적지를 찾겠습니다. 잠시만 기다려주세요
                route = transmitting_module.transmit()
                playing.play("/home/piLinux2/Desktop/guide.wav") # 목적지를 안내해드리겠습니다.


                location = transmitting_module.telecom()


    except KeyboardInterrupt:
        pass

GPIO.cleanup()

def t2_main():
    while True:
        s#####gps 모듈 코드


t1 = threading.Thread(target=t1_main)
t1.start

t2 = threading.Thread(target=t2_main)
t2.start


t1.join
t2.join

