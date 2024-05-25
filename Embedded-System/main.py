# -*- coding: utf-8 -*-

import recording
import stt
import playing
import transmitting_
import threading
import queue
import time
import pyaudio
import serial
from path import degrees_to_radians, dijkstra, find_nearest_node, distance_between_points, NodeLocation, returnpath, initialize_graph, building_map
import math
import re
import pynmea2
import string


button_pin = 27

global flag
flag = 0
a = 1

QUEUE_SIZE = 100


def clear_queue(q):
    try:
        while not q.empty():
            q.get_nowait()
    except queue.Empty:
        pass
    
lat_ = queue.LifoQueue(QUEUE_SIZE)
lon_ = queue.LifoQueue(QUEUE_SIZE)

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(button_pin, GPIO.IN)
#GPIO.add_event_detect(button_pin, GPIO.RISING)
#GPIO.add_event_callback(button_pin,buttonPressed)


node_locations = [
         NodeLocation(0, 37.30007, 126.8377),
        NodeLocation(1, 37.29986, 126.8372),
        NodeLocation(2, 37.29980, 126.8370),
        NodeLocation(3, 37.29927, 126.8373),
        NodeLocation(4, 37.29916, 126.8371),
        NodeLocation(5, 37.29882, 126.8376),
        NodeLocation(6, 37.29857, 126.8377),
        NodeLocation(7, 37.29840, 126.8378),
        NodeLocation(8, 37.29846, 126.83738),
        NodeLocation(9, 100, 300),
        NodeLocation(10, 37.29825, 126.8369),
        NodeLocation(11, 37.29816, 126.8369),
        NodeLocation(12, 37.29795, 126.83635),
        NodeLocation(13, 37.29761, 126.83558),
        NodeLocation(14, 37.29752, 126.8353),
        NodeLocation(15, 37.29737, 126.83548),
        NodeLocation(16, 37.29704, 126.83569),
        NodeLocation(17, 37.29700, 126.83546),
        NodeLocation(18, 37.29749, 126.83563), #29753
        NodeLocation(19, 37.29693, 126.8360),
        NodeLocation(20, 37.29696, 126.8360),
        NodeLocation(21, 37.29758, 126.8362),
        NodeLocation(22, 37.29769, 126.8361), #29761
        NodeLocation(23, 37.29798, 126.8368),
        NodeLocation(24, 37.29790, 126.8369),
        NodeLocation(25, 37.29839, 126.8368),
        NodeLocation(26, 37.29891, 126.8365),
        NodeLocation(27, 37.29899, 126.8366),
        NodeLocation(28, 37.29815, 126.83616),
        NodeLocation(29, 37.29844, 126.83610),
        NodeLocation(30, 37.29868, 126.83604),
        NodeLocation(31, 37.29835, 126.83519),
        NodeLocation(32, 37.29821, 126.8349),
        NodeLocation(33, 37.29811, 126.8349),
        NodeLocation(34, 37.29804, 126.8347),
        NodeLocation(35, 37.30002, 126.8371),
        NodeLocation(36, 37.29997, 126.8369),
        NodeLocation(37, 37.29965, 126.8361),
        NodeLocation(38, 37.29949, 126.8362),
        NodeLocation(39, 37.29924, 126.8351),
        NodeLocation(40, 37.29903, 126.8346),
        NodeLocation(41, 37.29886, 126.8348),
        NodeLocation(42, 37.29889, 126.8343),
        NodeLocation(43, 37.29874, 126.8339),
        NodeLocation(44, 37.29923, 126.8336),
        NodeLocation(45, 37.29876, 126.8345),
        NodeLocation(46, 37.29636, 126.83609),
        NodeLocation(47, 37.29629, 126.83615),
        NodeLocation(48, 37.296128, 126.83626),
        NodeLocation(49, 37.29620, 126.8365),
        NodeLocation(50, 37.29600, 126.83636),
        NodeLocation(51, 37.29607, 126.8366),
        NodeLocation(52, 37.29476, 126.83714),
        NodeLocation(53, 37.29493, 126.8373),
        NodeLocation(54, 37.29471, 126.83712),
        NodeLocation(55, 37.29377, 126.83712),
        NodeLocation(56, 37.29335, 126.83611),
        NodeLocation(57, 37.29326, 126.83619),
        NodeLocation(58, 37.293145, 126.83601),
        NodeLocation(59, 37.293072, 126.835706),
        NodeLocation(60, 37.29301, 126.83560),
        NodeLocation(61, 37.292626, 126.835818),
        NodeLocation(62, 37.29250, 126.83554),
        NodeLocation(63, 37.29923, 126.8356),
        NodeLocation(64, 37.29899, 126.8358),
        NodeLocation(65, 37.29939, 126.8356)
    ]

class CautionZone:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node
         
caution_zones = [
        CautionZone(7, 8),
    
        CautionZone(14,15),
        
        CautionZone(14,19),
        
        CautionZone(16,19),
        
        CautionZone(15,16),
        
        CautionZone(38, 39),
        
        CautionZone(40, 64),
        
        CautionZone(41, 42),
        
        CautionZone(41, 43),
        
        CautionZone(43, 46),
        
        CautionZone(47, 48),
        
        CautionZone(49, 51),
        
        CautionZone(51, 49),
        
        CautionZone(50, 52),
        
        CautionZone(53, 54),
 
        CautionZone(53, 55),
        
        CautionZone(57, 58),
        
        CautionZone(58, 59),
        
        CautionZone(60, 61)
           
]


def check_and_warn_if_caution_zone(current, next):
    for zone in caution_zones:
        if (zone.from_node == current and zone.to_node == next) or (zone.from_node == next and zone.to_node == current):
            print(f"Caution: You are traveling through a caution zone between Node {current + 1} and Node {next + 1}. Please be careful!")
            playing.play("/home/raspberrypi/Desktop/graduate_project_test_/in_front_of_crosswalk.wav")
            
def extract_route_indices(route_str):
    # 숫자만 추출
    node_ids = re.findall(r'\d+', route_str)
    # 추출된 문자열 숫자를 정수 리스트로 변환
    return [int(node_id) for node_id in node_ids]

def bearing(lat1, lon1, lat2, lon2):
    phi1 = degrees_to_radians(lat1)
    lambda1 = degrees_to_radians(lon1)
    phi2 = degrees_to_radians(lat2)
    lambda2 = degrees_to_radians(lon2)
    delta_lambda = lambda2 - lambda1
    X = math.cos(phi2) * math.sin(delta_lambda)
    Y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
    bearing_radians = math.atan2(X, Y)
    bearing_degrees = (bearing_radians * (180.0 / math.pi) + 360.0) % 360.0
    return bearing_degrees

def generate_direction(user_bearing, target_bearing):
    angle_difference = target_bearing - user_bearing
    if angle_difference > 180:
        angle_difference -= 360
    elif angle_difference < -180:
        angle_difference += 360

    if -45 < angle_difference <= 45:
        return "Continue straight"
    elif 45 < angle_difference <= 170:
        return "Turn right"
    elif angle_difference > 170 or angle_difference <= -170:
        return "Make a U-turn"
    elif -170 < angle_difference <= -45:
        return "Turn left"
    
"""
def navigate(user_lat, user_lon, current_node, next_node, way, node_locations, graph, isFirstUpdate, prev_lat, prev_lon, sentence):
    # 현재 사용자와 가장 가까운 노드 찾기
    prev_next_node = next_node
    nearest_node_id = find_nearest_node(user_lat, user_lon, node_locations) + 1  # 경로 인덱스와 일치하도록 +1
    print(f'nodeid:{nearest_node_id}')
    
    # 경로상에서 현재 노드의 위치 찾기
    if nearest_node_id in way:
        nearest_index = way.index(nearest_node_id)
    else:
        # 가장 가까운 노드가 경로에 없는 경우, 현재 노드를 유지
        nearest_index = None
    
    user_to_next_node_distance = distance_between_points(user_lat, user_lon, node_locations[next_node - 1].latitude, node_locations[next_node - 1].longitude)
    if user_to_next_node_distance <= 3:
        current_node = next_node
        current_index = way.index(current_node)
        # 다음 노드 설정
        if current_index + 1 < len(way):
            next_node = way[current_index + 1]
        else:
            next_node = current_node  # 리스트의 끝에 도달했을 경우, 현재 노드 유지
    else:
        current_index = way.index(current_node) if current_node in way else nearest_index
        current_node = current_node
        
    print(f'current:{current_node}')    
    print(f'next:{next_node}')
    # 경고 구역 체크
    check_and_warn_if_caution_zone(current_node, next_node)

    # 다음 노드까지의 방향 계산
    next_lat = node_locations[next_node - 1].latitude  # 인덱스 조정
    next_lon = node_locations[next_node - 1].longitude
    target_bearing = bearing(user_lat, user_lon, next_lat, next_lon)
    
    node_to_node_distance = distance_between_points(
        node_locations[current_node - 1].latitude, node_locations[current_node - 1].longitude,
        next_lat, next_lon
    )


    # 경로 재탐색 로직
    if user_to_next_node_distance > node_to_node_distance + 5:
        print("경로 재탐색")
        playing.play("/home/raspberrypi/Desktop/graduate_project_test_/refind.wav")
        new_route_str = transmitting_.telecom(sentence, user_lat, user_lon)
        new_way = extract_route_indices(new_route_str)
        current_node = nearest_node_id
        next_node = new_way[new_way.index(current_node) + 1] if (new_way.index(current_node) + 1) < len(new_way) else current_node
        way = new_way
        
    # 사용자의 현재 방향 계산
    if isFirstUpdate:
        user_bearing = target_bearing
        isFirstUpdate = False
    else:
        user_bearing = bearing(prev_lat, prev_lon, user_lat, user_lon)

    # 방향 지시 생성
    direction = generate_direction(user_bearing, target_bearing)
    
    if current_node == prev_next_node :
    #if user_to_next_node_distance <= 3 :
        if (direction == "Continue straight") :
            playing.play("/home/raspberrypi/Desktop/graduate_project_test_/go_forward.wav")
        elif (direction == "Turn right") :
            playing.play("/home/raspberrypi/Desktop/graduate_project_test_/turn_right.wav")
        elif (direction == "Make a U-turn") :
            playing.play("/home/raspberrypi/Desktop/graduate_project_test_/u_turn.wav")
        elif (direction == "Turn left") :
            playing.play("/home/raspberrypi/Desktop/graduate_project_test_/turn_left.wav")
   
    return current_node, next_node, way, user_lat, user_lon, isFirstUpdate, direction
"""

def navigate(user_lat, user_lon, current_node, next_node, way, node_locations, isFirstUpdate, prev_lat, prev_lon, sentence, warn):
    nearest_node_id = find_nearest_node(user_lat, user_lon, node_locations) + 1
    
    if nearest_node_id in way :
        nearest_index = way.index(nearest_node_id)
    else :
        nearest_index = None
        
    user_to_next_node_distance = distance_between_points(user_lat, user_lon, node_locations[next_node - 1].latitude, node_locations[next_node - 1].longitude)
    
    if user_to_next_node_distance <= 3:
        current_node = next_node
        current_index = way.index(current_node)
        warn = True
        
        if current_index + 1 < len(way):
            next_node = way[current_index + 1]
        else:
            next_node = current_node
    else:
        current_index = way.index(current_node) if current_node in way else nearest_index
        current_node = current_node
    
    print(f'current:{current_node}')
    print(f'next:{next_node}')
    
    if warn:
        check_and_warn_if_caution_zone(current_node, next_node)
        warn = False
    
    next_lat = node_locations[next_node - 1].latitude
    next_lon = node_locations[next_node - 1].longitude
    target_bearing = bearing(node_locations[current_node - 1].latitude, node_locations[current_node - 1].longitude, next_lat, next_lon)
    
    if isFirstUpdate:
        user_bearing = target_bearing
        isFirstUpdate = False
    else:
        prev_node = way[current_index - 1] if current_index > 0 else current_node
        prev_lat = node_locations[prev_node - 1].latitude
        prev_lon = node_locations[prev_node - 1].longitude
        user_bearing = bearing(prev_lat, prev_lon, node_locations[current_node - 1].latitude, node_locations[current_node - 1].longitude)
        if (prev_node == current_node):
            user_bearing = target_bearing
        
    node_to_node_distance = distance_between_points(node_locations[current_node - 1].latitude, node_locations[current_node - 1].longitude, next_lat, next_lon)
    
    #if user_to_next_node_distance > node_to_node_distance + 5:
     #   playing.play("/home/raspberrypi/Desktop/graduate_project_test_/refind.wav")
      #  new_route_str = transmitting_.telecom(sentence, user_lat, user_lon)
       # new_way = extract_route_indices(new_route_str)
        #current_node = nearest_node_id
        #next_node = new_way[new_way.index(current_node) + 1] if (new_way.index(current_node) + 1) < len(new_way) else current_node
        #way = new_way
                    
    direction = generate_direction(user_bearing, target_bearing)
    
    if user_to_next_node_distance > 3 and direction != "Continue straight":
        direction = "Continue straight"
    
    return current_node, next_node, way, user_lat, user_lon, isFirstUpdate, direction, warn
        
graph = initialize_graph()

def t1_main():
    #playing.play("/home/piLinux2/Desktop/goal.wav") # please tell me destination
    print("t1_main started")
    playing.play("/home/raspberrypi/Desktop/graduate_project_test_/tell_goal.wav") #목적지를 찾겠습니다. 잠시만 기다려주세요
    recording.audio()
    #lon = lon_.get()
    #lat = lat_.get()
    
    #print("latitude" + lat)
    #print("longitude" + lon)
    
    sentence = stt.transcribe_audio()
    
    playing.play("/home/raspberrypi/Desktop/graduate_project_test_/finding.wav") #목적지를 찾겠습니다. 잠시만 기다려주세요
    #sentence = "나는 학술정보관 가고 싶어"
    lat = lat_.get()
    
    #lon = 126.8377
    lon = lon_.get()
    #lat = 37.30007 #lon_.get()
        
    route_str = transmitting_.telecom(sentence, lat, lon)
    
    if(route_str == "None"):
        playing.play("/home/raspberrypi/Desktop/graduate_project_test_/tell_goal.wav") #목적지를 찾겠습니다. 잠시만 기다려주세요
        recording.audio()
        sentence = stt.transcribe_audio()
        lat = lat_.get()
        lon = lon_.get()
        route_str = transmitting_.telecom(sentence, lat, lon)
        
    route = extract_route_indices(route_str)
    print(f"route :{route}")
    lat = lat_.get()#37.0007 #
    lon = lon_.get()#126.8377 #
  # 노드 위치 딕셔너리
    current_node, next_node = route[0], route[1]
    
    print(f' previous current node:{current_node}, next node:{next_node}')
    isFirstUpdate = True
    warn = True
    prev_lat = lat
    prev_lon = lon
    last_direction = "Continue straight"
    
    print("Go Forward")
    ##playing.play("/home/raspberrypi/Desktop/graduate_project_test_/go_forward.wav")
    
    while current_node != route[-1]:
        lat = lat_.get()#float(input("lat:"))#37.30007
        clear_queue(lat_)
        lon = lon_.get()#float(input("lon:"))#126.8377
        clear_queue(lon_)
        print(f"from Queue lat: {lat} lon : {lon}")
        current_node, next_node, route, prev_lat, prev_lon, isFirstUpdate, last_direction, warn = navigate(lat, lon, current_node, next_node, route, node_locations, isFirstUpdate, prev_lat, prev_lon, sentence, warn)
        
        if current_node == route[-1]:
            print("You have reached your destination.")
            playing.play("/home/raspberrypi/Desktop/graduate_project_test_/finish.wav")
            break
        
        print(f'Next:{last_direction}')
        
        if (last_direction == "Continue straight") :
            print("Continue straight")
            ##playing.play("/home/raspberrypi/Desktop/graduate_project_test_/go_forward.wav")
        elif (last_direction == "Turn right") :
            print("Turn right")
            ##playing.play("/home/raspberrypi/Desktop/graduate_project_test_/turn_right.wav")
        elif (last_direction == "Make a U-turn") :
            ##playing.play("/home/raspberrypi/Desktop/graduate_project_test_/u_turn.wav")
            print("Make a U-turn")
        elif (last_direction == "Turn left") :
            ##playing.play("/home/raspberrypi/Desktop/graduate_project_test_/turn_left.wav")
            print("Turn left")
   
        time.sleep(5)

    #playing.play("/home/raspberrypi/Desktop/graduate_project_test_/finish.wav") # 목적지를 안내해드리겠습니다.
    print("t1_main finished")
    
def t2_main(*args, **kwargs):
    try:
        print("t2_main execute")
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
                    latitude = newmsg.latitude
                    longitude = newmsg.longitude
                    print(f"original data : {latitude}, {longitude}")
                    lat_.put(latitude)
                    lon_.put(longitude)
                    #print("X")
                    #print(f"{latitude} + {longitude}")
            except UnicodeDecodeError:
                    print("Error decoding NMEA data")
    except Exception as e:
        print(f"An error occurred: {e}")
                
if __name__ == "__main__":
    t1 = threading.Thread(target = t1_main)
    t2 = threading.Thread(target = t2_main)
    t2.start()
    t1.start()
    t2.join()
    t1.join()
    
    

