import pyaudio
import wave
import sys
import time
import RPI.GPIO as GPIO
import recording_module
import transmitting_module
import threading
import receiving_module
import navigaion_module

global flag
flag = 0 

def buttonPressed(channel) :
    flag = flag + 1

button_pin = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN)
GPIO.add_event_detect(button_pin, GPIO.RISING)
GPIO.add_event_callback(button_pin,buttonPressed)



try:
   while True:
       
       if flag == 1:
          recording_module
          transmitting_module
          location = receiving_module
          navigation_module(location)


except KeyboardInterrupt:
    pass

GPIO.cleanup()



