import math

V = 66
INF = float('inf')

building_map = {
        "학술정보관": 17,
        "복지관": 34,
        "제사공학관" : 20,

        "제삼공학관" : 21,

        "제일공학관" : 24,

        "제일학술관" : 29,

        "컨퍼러스홀" : 4,
        "정문" : 0,
        "셔틀콕" : 5,
        "제이과기관" : 8,

        "본관": 44,
        "경상관": 37,
        "국제문화관": 39,
        "기숙사": 62,
        "제일과기관": 64,

   
    }

class NodeLocation:
    def __init__(self, nodeId, latitude, longitude):
        self.nodeId = nodeId
        self.latitude = latitude
        self.longitude = longitude

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

def min_distance(dist, spt_set):
    min_val = INF
    min_index = -1
    for i, val in enumerate(dist):
        if not spt_set[i] and val < min_val:
            min_val = val
            min_index = i
    return min_index

def dijkstra(graph, src, dest, dest_neg=None):
    dist = [INF] * V
    parent = [-1] * V
    spt_set = [False] * V
    dist[src] = 0
    if dest_neg is not None:
        dist[dest_neg] = INF

    for _ in range(V - 1):
        u = min_distance(dist, spt_set)
        spt_set[u] = True

        for v in range(V):
            if dest_neg is not None and v == dest_neg:
                continue
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
    print(path)
    # Convert the path list to a string using '|' as a separator
    path_str = ' | '.join(map(str, path))
    return path_str  # Return the path as a string


def returnpath(dest, user_lat, user_lon, dest_neg = None):
    graph = initialize_graph()
    # Define your graph connections here

    if(dest == "4공학관"):
        dest =  "제사공학관"
    elif(dest == "3공학관"):
        dest =  "제삼공학관"
    elif(dest == "1공학관"):
        dest =  "제일공학관"
    elif(dest == "1학술관"):
        dest =  "제일학술관"
    elif(dest == "2과기관"):
        dest =  "제이공학관"
    elif(dest == "1과기관"):
        dest =  "제일과기관"

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
        NodeLocation(12, 37.29790, 126.8363),
        NodeLocation(13, 37.29761, 126.8356),
        NodeLocation(14, 37.29752, 126.8353),
        NodeLocation(15, 37.29738, 126.8354),
        NodeLocation(16, 37.29710, 126.8356),
        NodeLocation(17, 37.29700, 126.8353),
        NodeLocation(18, 37.29747, 126.8356), #29753
        NodeLocation(19, 37.29693, 126.8360),
        NodeLocation(20, 37.29696, 126.8360),
        NodeLocation(21, 37.29758, 126.8362),
        NodeLocation(22, 37.29769, 126.8361), #29761
        NodeLocation(23, 37.29798, 126.8368),
        NodeLocation(24, 37.29790, 126.8369),
        NodeLocation(25, 37.29839, 126.8368),
        NodeLocation(26, 37.29891, 126.8365),
        NodeLocation(27, 37.29899, 126.8366),
        NodeLocation(28, 37.29814, 126.8361),
        NodeLocation(29, 37.29836, 126.8361),
        NodeLocation(30, 37.29864, 126.8358),
        NodeLocation(31, 37.29834, 126.8351),
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
        NodeLocation(46, 37.29636, 126.8361),
        NodeLocation(47, 37.29627, 126.8362),
        NodeLocation(48, 37.29611, 126.8362),
        NodeLocation(49, 37.29620, 126.8365),
        NodeLocation(50, 37.29597, 126.8363),
        NodeLocation(51, 37.29607, 126.8366),
        NodeLocation(52, 37.29484, 126.8371),
        NodeLocation(53, 37.29493, 126.8373),
        NodeLocation(54, 37.29469, 126.8371),
        NodeLocation(55, 37.29379, 126.8371),
        NodeLocation(56, 37.29335, 126.8361),
        NodeLocation(57, 37.29324, 126.8361),
        NodeLocation(58, 37.29320, 126.8360),
        NodeLocation(59, 37.29307, 126.8357),
        NodeLocation(60, 37.29300, 126.8356),
        NodeLocation(61, 37.29262, 126.8358),
        NodeLocation(62, 37.29245, 126.8354),
        NodeLocation(63, 37.29923, 126.8356),
        NodeLocation(64, 37.29899, 126.8358),
        NodeLocation(65, 37.29939, 126.8356)

        # Add more nodes as necessary
    ]

    nearest_node_id = find_nearest_node(user_lat, user_lon, node_locations)

    src = nearest_node_id
    dest = find_des_node(building_map,dest)  # Example destination node ID
    way = dijkstra(graph, src, dest, dest_neg)

    return way
    # Removed the path print statement as per request
    # Now the function returns the path array directly
