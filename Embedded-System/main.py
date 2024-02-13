import recording
import playing
import RPI.GPIO as GPIO
import transmitting_module
import threading
button_pin = 27

global flag
flag = 0
a = 1 

def buttonPressed(channel) :
    flag = flag + 1



GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN)
GPIO.add_event_detect(button_pin, GPIO.RISING)
GPIO.add_event_callback(button_pin,buttonPressed)

try:
    while True:
        if flag == 1:
            playing.play("/home/piLinux2/Desktop/goal.wav") # please tell me destination
           


except KeyboardInterrupt:
    pass

GPIO.cleanup()


