import serial
import time
import string
import pynmea2



def getposition():
    try:
        port = "/dev/ttyAMA0"
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        
        while True:
            # 시리얼 데이터 수신
            newdata = ser.readline()

            # 수신한 데이터를 문자열로 변환하여 비교
            try:
                newdata_str = newdata.decode('ascii')  # ASCII로 디코딩
                if newdata_str.startswith("$GPRMC"):
                    newmsg = pynmea2.parse(newdata_str)
                    lat = newmsg.latitude
                    lng = newmsg.longitude
                    gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
                    return lat, lng
                    #print(gps)
            except UnicodeDecodeError:
                print("Error decoding NMEA data")

    except serial.SerialException as e:
        print("Serial connection error:", e)
        time.sleep(1)  # 재시도를 위해 잠시 대기
    
