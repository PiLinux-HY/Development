# -*- coding: utf-8 -*-

import recording
import stt
import playing
import transmitting_
import threading
import queue
import time
import pyaudio
import gps__
import navi

button_pin = 27

global flag
flag = 0
a = 1

QUEUE_SIZE = 5

def buttonPressed(channel) :
    flag = flag + 1

lat_ = queue.Queue(QUEUE_SIZE)
lon_ = queue.Queue(QUEUE_SIZE)

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(button_pin, GPIO.IN)
#GPIO.add_event_detect(button_pin, GPIO.RISING)
#GPIO.add_event_callback(button_pin,buttonPressed)


def t1_main():
    #playing.play("/home/piLinux2/Desktop/goal.wav") # please tell me destination
    print("t1_main started")
    playing.play("/home/raspberrypi/Desktop/graduate_project_test_/tell_goal.wav") #목적지를 찾겠습니다. 잠시만 기다려주세요
    recording.audio()
    lon = lon_.get()
    lat = lat_.get()
    print("latitude" + lat)
    print("longitude" + lon)
    
    sentence = stt.transcribe_audio()
    
    playing.play("/home/raspberrypi/Desktop/graduate_project_test_/finding.wav") #목적지를 찾겠습니다. 잠시만 기다려주세요
    #sentence = "나는 학술정보관 가고 싶어"
    route = transmitting_.telecom(sentence)
    playing.play("/home/raspberrypi/Desktop/graduate_project_test_/will_guide.wav") # 목적지를 안내해드리겠습니다.


    while 1:
        lon = lon_.get()
        lat = lat_.get()
        navi.navigate(route, lat, lon, graph)
    print("t1_main finished")
    
def t2_main():
    while(1):
        print("t2 started")
        latitude, longitude = gps__.getposition()
        lat_.put(latitude)
        lon_.put(longitude)
        
        time.sleep(0.1)
        print("t2 finished")
        
    
if __name__ == "__main__":
    t1 = threading.Thread(target = t1_main)
    t2 = threading.Thread(target = t2_main)
    t2.start()
    t1.start()
    t2.join()
    t1.join()
    
