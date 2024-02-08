import serial
import pynmea2

def location():
    while True:
        port="/dev/serial0"
        ser =serial.Serial(port,baudrate=9600,timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata =ser.readline()
        n_data =newdata.decode('latin-1')
        if n_data[0:6] == "$GPRMC":
            newloc=pynmea2.parse(n_data)
            lat=newloc.latitude
            lng=newloc.longitude
            break
    return lat,lng