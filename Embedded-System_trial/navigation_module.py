import gps_module
import threading
import time
V = 35
INF = float('inf')

def initialize_graph(graph):
    for i in range(V):
        for j in range(V):
            graph[i][j] = 0 if i == j else INF

    graph[0][1] = 60
    graph[1][0] = 60
    graph[1][2] = 17
    graph[2][1] = 17
    graph[2][3] = 61
    graph[3][2] = 61
    graph[3][4] = 26
    graph[3][5] = 58
    graph[4][3] = 26
    graph[5][3] = 58
    graph[5][6] = 26
    graph[6][5] = 26
    graph[6][7] = 22
    graph[6][8] = 45
    graph[7][6] = 22
    graph[7][23] = 102
    graph[8][6] = 45
    graph[8][9] = 13
    graph[8][10] = 42
    graph[9][8] = 13
    graph[10][8] = 42
    graph[10][11] = 9
    graph[10][25] = 17
    graph[11][10] = 9
    graph[11][12] = 60
    graph[12][11] = 60
    graph[12][13] = 75
    graph[12][28] = 31
    graph[13][12] = 75
    graph[13][14] = 21
    graph[13][18] = 10
    graph[13][31] = 94
    graph[14][13] = 21
    graph[14][15] = 10
    graph[14][33] = 75
    graph[15][14] = 10
    graph[15][16] = 35
    graph[15][18] = 21
    graph[16][15] = 35
    graph[16][17] = 27
    graph[17][16] = 27
    graph[18][13] = 10
    graph[18][15] = 21
    graph[18][19] = 75
    graph[18][22] = 50
    graph[19][18] = 75
    graph[19][20] = 8
    graph[20][19] = 8
    graph[21][22] = 15
    graph[22][18] = 50
    graph[22][21] = 15
    graph[22][23] = 72
    graph[23][7] = 102
    graph[23][22] = 72
    graph[23][24] = 13
    graph[24][23] = 13
    graph[25][10] = 17
    graph[25][26] = 62
    graph[25][28] = 60
    graph[26][25] = 62
    graph[26][27] = 26
    graph[26][30] = 60
    graph[27][26] = 26
    graph[28][12] = 31
    graph[28][25] = 60
    graph[28][29] = 25
    graph[29][28] = 25
    graph[29][30] = 37
    graph[30][26] = 60
    graph[30][29] = 37
    graph[30][31] = 73
    graph[31][13] = 94
    graph[31][30] = 73
    graph[31][32] = 24
    graph[32][31] = 24
    graph[32][33] = 9
    graph[32][34] = 33
    graph[33][14] = 75
    graph[33][32] = 9
    graph[33][34] = 30
    graph[34][32] = 33
    graph[34][33] = 30

def min_distance(dist, spt_set):
    min_val = float('inf')
    min_index = -1
    for v in range(V):
        if not spt_set[v] and dist[v] <= min_val:
            min_val = dist[v]
            min_index = v
    return min_index

def print_path(parent, j):
    if parent[j] == -1:
        return
    print_path(parent, parent[j])
    print(j + 1, end=" ")

def dijkstra(graph, src, dest):
    dist = [INF] * V
    spt_set = [False] * V
    parent = [-1] * V

    dist[src] = 0

    for _ in range(V - 1):
        u = min_distance(dist, spt_set)
        spt_set[u] = True
        for v in range(V):
            if not spt_set[v] and graph[u][v] and dist[u] != INF and dist[u] + graph[u][v] < dist[v]:
                parent[v] = u
                dist[v] = dist[u] + graph[u][v]

    print(f"Distance from Node {src + 1} to Node {dest + 1} is: {dist[dest]}")
    print("Path:", src + 1, end=" ")
    print_path(parent, dest)
    return list############

def navigation():


###메시지 큐 통신

def route(destination):
    graph = [[0] * V for _ in range(V)]
    initialize_graph(graph)

    src, dest = map(int, input().split())
    #dijkstra(graph, src - 1, dest - 1)
    gps = threading.Thread(target = gps_module.location) # 튜플 형태로 반환
    gps.start()

    dijkstra( graph, src - 1, dest -1)
    navi= threading.Thread(target = navigation())
    ######
    navi.start()

    
    