import math
import time
import re

V = 66
INF = float('inf')

def extract_route_indices(route_str):
    # 숫자만 추출
    node_ids = re.findall(r'\d+', route_str)
    # 추출된 문자열 숫자를 정수 리스트로 변환
    return [int(node_id) for node_id in node_ids]

building_map = {
        "학술정보관": 17,
        "복지관": 34,
        "제4공학관" : 20,
        "제3공학관" : 21,
        "제1공학관" : 24,
        "제1학술관" :29,
        "컨퍼러스홀" : 4,
        "정문" : 0,
        "셔틀콕" : 5,
        "제2과기관" : 8,
        "본관": 44,
        "경상관": 37,
        "국제문화관": 39,
        "기숙사": 62,
        "제1과기관": 64
    }

class NodeLocation:
    def __init__(self, nodeId, latitude, longitude):
        self.nodeId = nodeId
        self.latitude = latitude
        self.longitude = longitude

class CautionZone:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node
        
caution_zones = [
        CautionZone(7, 8),
        CautionZone(8, 7),
    
        CautionZone(14,15),
        CautionZone(15,14),
        
        CautionZone(14,19),
        CautionZone(19,14),
        
        CautionZone(16,19),
        CautionZone(19,16),
        
        CautionZone(15,16),
        CautionZone(16,15),
        
        CautionZone(38, 39),
        CautionZone(39, 38),
        
        CautionZone(40, 64),
        CautionZone(64, 40),
        
        CautionZone(41, 42),
        CautionZone(42, 41),
        
        CautionZone(41, 43),
        CautionZone(43, 41),
        
        CautionZone(43, 46),
        CautionZone(46, 43),
        
        CautionZone(47, 48),
        CautionZone(48, 47),
        
        CautionZone(49, 51),
        CautionZone(51, 49),
        
        CautionZone(50, 52),
        CautionZone(52, 50),
        
        CautionZone(53, 54),
        CautionZone(54, 53),
 
        CautionZone(53, 55),
        CautionZone(55, 53),
        
        CautionZone(57, 58),
        CautionZone(58, 57),
        
        CautionZone(58, 59),
        CautionZone(59, 58),
        
        CautionZone(60, 61),
        CautionZone(61, 60)       
]

def initialize_graph():
    graph = [[INF if i != j else 0 for j in range(V)] for i in range(V)]
    # Define graph connections here, similar to the C code
    graph[0][1]=60

    graph[1][0]=60
    graph[1][2]=17
    graph[1][35]=19

    graph[2][1]=17
    graph[2][3]=61
    graph[2][36]=20
    graph[2][38]=81

    graph[3][2]=61
    graph[3][4]=26
    graph[3][5]=58

    graph[4][3]=26

    graph[5][3]=58
    graph[5][6]=26

    graph[6][5]=26
    graph[6][7]=22
    graph[6][8]=45

    graph[7][6]=22
    graph[7][23]=102

    graph[8][6]=45
    graph[8][9]=13
    graph[8][10]=42

    graph[9][8]=13

    graph[10][8]=42
    graph[10][11]=9
    graph[10][25]=17

    graph[11][10]=9
    graph[11][12]=60

    graph[12][11]=60
    graph[12][13]=75
    graph[12][28]=31

    graph[13][12]=75
    graph[13][14]=21
    graph[13][18]=10
    graph[13][31]=94

    graph[14][13]=21
    graph[14][15]=10
    graph[14][33]=75

    graph[15][14]=10
    graph[15][16]=35
    graph[15][18]=21

    graph[16][15]=35
    graph[16][17]=27
    graph[16][46]=96

    graph[17][16]=27

    graph[18][13]=10
    graph[18][15]=21
    graph[18][19]=75
    graph[18][22]=50

    graph[19][18]=75
    graph[19][20]=8
    graph[19][49]=90

    graph[20][19]=8

    graph[21][22]=15

    graph[22][18]=50
    graph[22][21]=15
    graph[22][23]=72

    graph[23][7]=102
    graph[23][22]=72
    graph[23][24]=13

    graph[24][23]=13

    graph[25][10]=17
    graph[25][26]=62
    graph[25][28]=60

    graph[26][25]=62
    graph[26][27]=26
    graph[26][30]=60

    graph[27][26]=26
    graph[27][38]=66

    graph[28][12]=31
    graph[28][25]=60
    graph[28][29]=25

    graph[29][28]=25
    graph[29][30]=37

    graph[30][26]=60
    graph[30][29]=37
    graph[30][31]=73

    graph[31][13]=94
    graph[31][30]=73
    graph[31][32]=24
    graph[31][41]=65

    graph[32][31]=24
    graph[32][33]=9
    graph[32][34]=33
    graph[32][45]=76

    graph[33][14]=75
    graph[33][32]=9
    graph[33][34]=30

    graph[34][32]=33
    graph[34][33]=30
    
    graph[35][1]=19
    graph[35][36]=13
    
    graph[36][2]=20
    graph[36][35]=13
    graph[36][37]=81
    
    graph[37][36]=81
    graph[37][38]=20
    graph[37][65]=59
    
    graph[38][2]=81
    graph[38][27]=69
    graph[38][37]=20
    graph[38][63]=59
    
    graph[39][65]=40
    graph[39][40]=49
    
    graph[40][39]=49
    graph[40][41]=21
    graph[40][42]=31
    
    graph[41][31]=65
    graph[41][40]=21
    graph[41][63]=89
    
    graph[42][40]=31
    graph[42][43]=44
    graph[42][45]=21
    
    graph[43][42]=44
    graph[43][44]=62
    
    graph[44][43]=62
    
    graph[45][42]=21
    graph[45][32]=76
    
    graph[46][16]=96
    graph[46][47]=8
    
    graph[47][46]=8
    graph[47][48]=22
    
    graph[48][47]=22
    graph[48][50]=17
    
    graph[49][19]=90
    graph[49][51]=16
    
    graph[50][48]=17
    graph[50][52]=142
    
    graph[51][49]=16
    graph[51][53]=142
    
    graph[52][50]=142
    graph[52][53]=23
    graph[52][54]=16
    
    graph[53][51]=142
    graph[53][52]=23
    
    graph[54][52]=16
    graph[54][55]=103
    
    graph[55][54]=103
    graph[55][56]=100
    
    graph[56][55]=100
    graph[56][57]=13
    
    graph[57][56]=13
    graph[57][58]=15
    
    graph[58][57]=15
    graph[58][59]=28
    
    graph[59][58]=28
    graph[59][60]=12
    
    graph[60][59]=12
    graph[60][61]=46
    
    graph[61][60]=46
    graph[61][62]=40
    
    graph[62][61]=40
    
    graph[63][38]=59
    graph[63][41]=89
    graph[63][64]=31
    graph[63][65]=21
    
    graph[64][63]=31
    
    graph[65][37]=59
    graph[65][39]=40
    graph[65][63]=21
    
    return graph

def degrees_to_radians(degrees):
    return degrees * (math.pi / 180.0)

def distance_between_points(lat1, lon1, lat2, lon2):
    phi1 = degrees_to_radians(lat1)
    phi2 = degrees_to_radians(lat2)
    delta_phi = degrees_to_radians(lat2 - lat1)
    delta_lambda = degrees_to_radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371e3 * c

def find_nearest_node(user_lat, user_lon, node_locations):
    nearest_node_id = -1
    nearest_distance = INF
    for i, node in enumerate(node_locations):
        dist = distance_between_points(user_lat, user_lon, node.latitude, node.longitude)
        if dist < nearest_distance:
            nearest_node_id = i
            nearest_distance = dist
    return nearest_node_id

def find_des_node(building_map,dest):  
    return building_map.get(dest, None)

def min_distance(dist, spt_set):
    min_val = INF
    min_index = -1
    for i, val in enumerate(dist):
        if not spt_set[i] and val < min_val:
            min_val = val
            min_index = i
    return min_index
# main에서 사용할거면 여기서 선언 안해도 될듯
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
        NodeLocation(59, 37.29320, 126.83568),
        NodeLocation(60, 37.29301, 126.83560),
        NodeLocation(61, 37.292626, 126.835818),
        NodeLocation(62, 37.29250, 126.83554),
        NodeLocation(63, 37.29923, 126.8356),
        NodeLocation(64, 37.29899, 126.8358),
        NodeLocation(65, 37.29939, 126.8356)
    ]

def check_and_warn_if_caution_zone(current, next):
    for zone in caution_zones:
        if (zone.from_node == current and zone.to_node == next) or (zone.from_node == next and zone.to_node == current):
            print(f"Caution: You are traveling through a caution zone between Node {current} and Node {next}. Please be careful!")

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

    if -30 < angle_difference <= 30:
        return "Continue straight"
    elif 30 < angle_difference <= 170:
        return "Turn right"
    elif angle_difference > 170 or angle_difference <= -170:
        return "Make a U-turn"
    elif -170 < angle_difference <= -30:
        return "Turn left"

def dijkstra(graph, src, dest):
    dist = [INF] * V
    parent = [-1] * V
    spt_set = [False] * V
    dist[src] = 0

    for _ in range(V - 1):
        u = min_distance(dist, spt_set)
        spt_set[u] = True

        for v in range(V):
            if not spt_set[v] and graph[u][v] != INF and dist[u] + graph[u][v] < dist[v]:
                parent[v] = u
                dist[v] = dist[u] + graph[u][v]

    # Path reconstruction
    path = []
    current = dest
    while current != -1:
        path.append(current + 1)  # Adjusting index to match human-readable form (1-indexed)
        current = parent[current]
    path.reverse()  # Reverse the path to start from the source
    # Convert the path list to a string using '|' as a separator
    path_str = ' | '.join(map(str, path))
    return path_str  # Return the path as a string

def returnpath(dest, user_lat,user_lon):
    graph = initialize_graph()

    nearest_node_id = find_nearest_node(user_lat, user_lon, node_locations)

    src = nearest_node_id
    dest = find_des_node(building_map, dest)  # Example destination node ID
    way = dijkstra(graph, src, dest)

    return way

graph = initialize_graph()

# main에서 선언해서 사용해야 할 것.
# route, lat, lon, node_locations(main에 새로 선언), graph(initialize import해서 선언)
"""def navigate(way, user_lat, user_lon, node_locations, graph):
    current_node = way[0]
    dest = way[-1]
    index = 0

    while current_node != dest:
        # 사용자의 현재 위치를 입력받습니다.
        try:
            user_lat, user_lon = map(float, input("Enter your current latitude and longitude: ").split()) # 여기에 받아온 위도 경도 입력값으로 사용하면 됨
            # main에서 lat, lon이용해서 입력
        except ValueError:
            print("Invalid input. Please enter valid latitude and longitude.")
            continue

        # 현재 노드에서 가장 가까운 노드를 다시 찾습니다.
        nearest_node_id = find_nearest_node(user_lat, user_lon, node_locations)
        print(f"Currently nearest node: Node {nearest_node_id + 1}")

        # 다음 목적지 노드를 경로에서 확인합니다.
        if index + 1 < len(way):
            next_node = way[index + 1]
        else:
            print("You have reached your destination.")
            break

        # 다음 노드까지의 거리를 계산합니다.
        next_lat = node_locations[next_node].latitude
        next_lon = node_locations[next_node].longitude
        distance_to_next_node = distance_between_points(user_lat, user_lon, next_lat, next_lon)

        # 다음 노드까지의 거리가 50미터 이상인 경우 경로를 재탐색합니다.
        if distance_to_next_node > 50:
            print("You are deviating from the path. Recalculating route...")
            _, way = dijkstra(graph, nearest_node_id, dest)
            index = way.index(nearest_node_id)  # 경로에서 현재 위치의 새 인덱스를 찾습니다.
            continue

        # 다음 노드가 경고 구역에 있는지 확인합니다.
        check_and_warn_if_caution_zone(current_node, next_node)

        # 사용자에게 다음 노드까지의 방향을 안내합니다.
        target_bearing = bearing(user_lat, user_lon, next_lat, next_lon)
        user_bearing = target_bearing  # 사용자의 진행 방향 추정
        direction = generate_direction(user_bearing, target_bearing)
        print(f"Next step: {direction}")

        # 목적지에 도착했는지 확인합니다.
        if next_node == dest:
            print("You have reached your destination.")
            break

        # 다음 노드를 현재 노드로 업데이트하고 인덱스를 증가시킵니다.
        current_node = next_node
        index += 1
        
        # 1초간 대기
        time.sleep(1) """

"""def navigate(user_lat, user_lon, current_node, next_node, way, node_locations, graph, isFirstUpdate, prev_lat, prev_lon):
    # Calculate the distance to the next node
    next_lat = node_locations[next_node].latitude
    next_lon = node_locations[next_node].longitude
    distance_to_next_node = distance_between_points(user_lat, user_lon, next_lat, next_lon)
    current_node = find_nearest_node(user_lat, user_lon, node_locations)
    next_node = 

    '''if distance_to_next_node > 50:
        print("You are deviating from the path. Recalculating route…")
        nearest_node_id = find_nearest_node(user_lat, user_lon, node_locations)
        print(f'lan:{user_lat} lon:{user_lon}')
        print(nearest_node_id)
        route_str = dijkstra(graph, nearest_node_id, way[-1])
        new_way = extract_route_indices(route_str)
        print(new_way)
        index = new_way.index(nearest_node_id+1)
        return new_way[index], new_way[index+1] if index+1 < len(new_way) else new_way[index], new_way, index, user_lat, user_lon
        '''
    if distance_to_next_node > 50:
        # Recalculating route
        nearest_node_id = find_nearest_node(user_lat, user_lon, node_locations)
        route_str = dijkstra(graph, nearest_node_id, way[-1])
        new_way = extract_route_indices(route_str)
        index = new_way.index(nearest_node_id + 1)
        return new_way[index], new_way[index+1] if index+1 < len(new_way) else new_way[index], new_way, index, user_lat, user_lon

    check_and_warn_if_caution_zone(current_node, next_node)

    # Provide the direction to the next node
    target_bearing = bearing(user_lat, user_lon, next_lat, next_lon)
    user_bearing = target_bearing if isFirstUpdate else bearing(prev_lat, prev_lon, user_lat, user_lon)
    isFirstUpdate = False

    direction = generate_direction(user_bearing, target_bearing)
    print(f"Next step: {direction}")

    # Move to the next node
    ## current_node = find_nearest_node(user_lat, user_lon, node_locations)
    #index = way.index(current_node) + 1
    #next_node = way[index] if index < len(way) else current_node

    return current_node, next_node, way, way.index(current_node), user_lat, user_lon 
    
def navigate(user_lat, user_lon, current_node, next_node, way, node_locations, graph, isFirstUpdate, prev_lat, prev_lon):
    # Calculate the current to next node distance
    current_node = find_nearest_node(user_lat, user_lon, node_locations)
    current_index = way.index(current_node+1)
    next_node = way[current_index]
    print(f'c_index:{current_index},{way[current_index]}')
    print(f'nextnode:{next_node} current:{current_node}')
    print(f'way:{way}')
    print(f'{way[0]},{way[1]},{way[2]},{way[3]},{way[4]},{way[5]},{way[6]},{way[7]},{way[8]}')
    next_lat = node_locations[next_node].latitude
    next_lon = node_locations[next_node].longitude
    #distance_to_next_node = distance_between_points(user_lat, user_lon, next_lat, next_lon)

    # if distance_to_next_node > 100:
    #     print("You are deviating from the path. Recalculating route...")
    #     nearest_node_id = find_nearest_node(user_lat, user_lon, node_locations)
    #     route_str = dijkstra(graph, nearest_node_id, way[-1])
    #     new_way = extract_route_indices(route_str)
    #     index = new_way.index(nearest_node_id + 1)
    #     current_node = new_way[index]
    #     next_node = new_way[index + 1] if index + 1 < len(new_way) else current_node
    # else:
    #      # Update current_node to next_node if the next node is reached
    #      index = way.index(current_node + 1)
    #      next_node = way[index + 1] if index + 1 < len(way) else current_node
    #      print(f'nextnode:{next_node}')

    # Check if moving through a caution zone
    check_and_warn_if_caution_zone(current_node, next_node)

    # Calculate bearing to the next node
    print(f'next:{next_lat},{next_lon} now:{user_lat},{user_lon} prev:{prev_lat},{prev_lon}')
    target_bearing = bearing(user_lat, user_lon, next_lat, next_lon)
    print(target_bearing)
    if (isFirstUpdate==True) :
        user_bearing = target_bearing
        isFirstUpdate = False
    else :
        user_bearing = bearing(prev_lat, prev_lon, user_lat, user_lon)
    print(user_bearing)
    isFirstUpdate = False

    # Determine the navigation direction
    direction = generate_direction(user_bearing, target_bearing)
    print(f"Next step: {direction}")

    return current_node, next_node, way ,user_lat, user_lon, isFirstUpdate """

def navigate(user_lat, user_lon, current_node, next_node, way, node_locations, graph, isFirstUpdate, prev_lat, prev_lon):
    # 현재 사용자와 가장 가까운 노드 찾기
    nearest_node_id = find_nearest_node(user_lat, user_lon, node_locations) + 1  # 경로 인덱스와 일치하도록 +1
    print(f'nodeid:{nearest_node_id}')
    # 경로상에서 현재 노드의 위치 찾기
    if nearest_node_id in way:
        current_index = way.index(nearest_node_id)
        current_node = nearest_node_id
    else:
        # 가장 가까운 노드가 경로에 없는 경우, 현재 노드를 유지
        current_index = way.index(current_node)
        print('else')
    print(f'current:{current_node}')
    # 다음 노드 설정
    if current_index + 1 < len(way):
        next_node = way[current_index + 1]
    else:
        next_node = current_node  # 리스트의 끝에 도달했을 경우, 현재 노드 유지
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

    # 사용자 위치에서 다음 노드까지의 거리
    user_to_next_node_distance = distance_between_points(user_lat, user_lon, next_lat, next_lon)

    # 경로 재탐색 로직
    if user_to_next_node_distance > node_to_node_distance:
        print("경로 재탐색")
        new_route_str = dijkstra(graph, nearest_node_id, way[-1])
        new_way = extract_route_indices(new_route_str)
        current_node = nearest_node_id
        next_node = new_way[new_way.index(current_node) + 1] if (new_way.index(current_node) + 1) < len(new_way) else current_node

    # 사용자의 현재 방향 계산
    if isFirstUpdate:
        user_bearing = target_bearing
        isFirstUpdate = False
    else:
        user_bearing = bearing(prev_lat, prev_lon, user_lat, user_lon)

    # 방향 지시 생성
    direction = generate_direction(user_bearing, target_bearing)
    print(f"Next step: {direction}")

    return current_node, next_node, way, user_lat, user_lon, isFirstUpdate


def main():
    lat = 37.30007
    lon = 126.8377
    route_str = returnpath("학술정보관", lat, lon)
    print(f"route_str:{route_str}")
    route = extract_route_indices(route_str)
    print(f"route:{route}")
    
    current_node = route[0]
    next_node = route[1]
    #index = 0
    isFirstUpdate = True
    prev_lat = lat
    prev_lon = lon
    
    while current_node != route[-1]:
        lat = float(input("lat:"))#37.30007#lat_.get
        lon = float(input("lon:"))#126.8377#lon_.get()
        current_node, next_node, route, prev_lat, prev_lon, isFirstUpdate = navigate(lat, lon, current_node, next_node, route, node_locations, graph, isFirstUpdate, prev_lat, prev_lon)
        if current_node == route[-1]:
            print("You have reached your destination.")
            break
        time.sleep(1)
    
if __name__ == "__main__":
    main()
