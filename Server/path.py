import math

V = 35
INF = float('inf')

building_map = {
        "학술정보관": 18,
        "복지관": 35,
        "제4공학관" : 21,
        "제3공학관" : 22,
        "제1학술관" :30,
        "컨퍼러스홀" : 28,
        "정문" : 1,
        "셔틀콕" : 6,
        "제2과기관" : 10,
        "본관": 12        
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

    graph[2][1]=17
    graph[2][3]=61

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

    graph[17][16]=27

    graph[18][13]=10
    graph[18][15]=21
    graph[18][19]=75
    graph[18][22]=50

    graph[19][18]=75
    graph[19][20]=8

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

    graph[32][31]=24
    graph[32][33]=9
    graph[32][34]=33

    graph[33][14]=75
    graph[33][32]=9
    graph[33][34]=30

    graph[34][32]=33
    graph[34][33]=30
    return graph

def min_distance(dist, spt_set):
    min_val = INF
    min_index = -1
    for i, val in enumerate(dist):
        if not spt_set[i] and val < min_val:
            min_val = val
            min_index = i
    return min_index

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
    print(path)
    # Convert the path list to a string using '|' as a separator
    path_str = ' | '.join(map(str, path))
    return path_str  # Return the path as a string


def returnpath(dest, user_lat,user_lon):
    graph = initialize_graph()
    # Define your graph connections here

    node_locations = [
        NodeLocation(0, 37.30006, 126.8377),
        NodeLocation(1, 37.29985, 126.8371),
        # Add more nodes as necessary
    ]

    nearest_node_id = find_nearest_node(user_lat, user_lon, node_locations)

    src = nearest_node_id
    dest = find_des_node(building_map,dest)  # Example destination node ID
    way = dijkstra(graph, src, dest)

    return way
    # Removed the path print statement as per request
    # Now the function returns the path array directly
