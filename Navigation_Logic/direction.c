#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <limits.h>
#include <stdbool.h>
#include <float.h>

#define V 35
#define INF INT_MAX

typedef struct {
    int nodeId;
    double latitude;
    double longitude;
} NodeLocation;

double degreesToRadians(double degrees) {
    return degrees * (M_PI / 180.0);
}

double distanceBetweenPoints(double lat1, double lon1, double lat2, double lon2) {
    double phi1 = degreesToRadians(lat1);
    double phi2 = degreesToRadians(lat2);
    double deltaPhi = degreesToRadians(lat2 - lat1);
    double deltaLambda = degreesToRadians(lon2 - lon1);
    double a = sin(deltaPhi / 2) * sin(deltaPhi / 2) +
               cos(phi1) * cos(phi2) *
               sin(deltaLambda / 2) * sin(deltaLambda / 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));
    return 6371e3 * c; // 결과는 미터 단위
}

double Bearing(double lat1, double lon1, double lat2, double lon2) {
    double phi1 = degreesToRadians(lat1);
    double lambda1 = degreesToRadians(lon1);
    double phi2 = degreesToRadians(lat2);
    double lambda2 = degreesToRadians(lon2);

    double deltaLambda = lambda2 - lambda1;
    double X = cos(phi2) * sin(deltaLambda);
    double Y = cos(phi1) * sin(phi2) - sin(phi1) * cos(phi2) * cos(deltaLambda);
    double bearingRadians = atan2(X, Y);
    double bearingDegrees = fmod((bearingRadians * (180.0 / M_PI) + 360.0), 360.0);
    return bearingDegrees;
}

void generateDirection(double userBearing, double targetBearing) {
    double angleDifference = fmod(targetBearing - userBearing + 360, 360);

    if (angleDifference > 315 || angleDifference <= 45) {
        printf("Continue straight\n");
    } else if (angleDifference > 45 && angleDifference <= 135) {
        printf("Turn right\n");
    } else if (angleDifference > 135 && angleDifference <= 225) {
        printf("Make a U-turn\n");
    } else if (angleDifference > 225 && angleDifference <= 315) {
        printf("Turn left\n");
    }
}

int findNearestNode(double userLat, double userLon, NodeLocation *nodeLocations, int numNodes) {
    int nearestNodeId = -1;
    double nearestDistance = DBL_MAX;
    for (int i = 0; i < numNodes; i++) {
        double dist = distanceBetweenPoints(userLat, userLon, nodeLocations[i].latitude, nodeLocations[i].longitude);
        if (dist < nearestDistance) {
            nearestNodeId = i; // nodeId 대신 i를 사용하여 배열의 인덱스를 저장
            nearestDistance = dist;
        }
    }
    return nearestNodeId;
}

void initializeGraph(int graph[V][V]) {
    // 그래프 초기화 로직
    for (int i = 0; i < V; i++) {
        for (int j = 0; j < V; j++) {
            graph[i][j] = (i == j) ? 0 : INF; //i와j가 같다면 0, 아니면 무한대로 초기화.
        }
    }
    // 노드 간의 연결 및 거리 정의
    // 예: graph[0][1] = 60; 은 노드 1에서 노드 2로 가는 거리가 60임을 의미.
    graph[0][1]=60; //0과1번 노드사이의 거리는 60

    graph[1][0]=60;
    graph[1][2]=17;

    graph[2][1]=17;
    graph[2][3]=61;

    graph[3][2]=61;
    graph[3][4]=26;
    graph[3][5]=58;

    graph[4][3]=26;

    graph[5][3]=58;
    graph[5][6]=26;

    graph[6][5]=26;
    graph[6][7]=22;
    graph[6][8]=45;

    graph[7][6]=22;
    graph[7][23]=102;

    graph[8][6]=45;
    graph[8][9]=13;
    graph[8][10]=42;

    graph[9][8]=13;

    graph[10][8]=42;
    graph[10][11]=9;
    graph[10][25]=17;

    graph[11][10]=9;
    graph[11][12]=60;

    graph[12][11]=60;
    graph[12][13]=75;
    graph[12][28]=31;

    graph[13][12]=75;
    graph[13][14]=21;
    graph[13][18]=10;
    graph[13][31]=94;

    graph[14][13]=21;
    graph[14][15]=10;
    graph[14][33]=75;

    graph[15][14]=10;
    graph[15][16]=35;
    graph[15][18]=21;

    graph[16][15]=35;
    graph[16][17]=27;

    graph[17][16]=27;

    graph[18][13]=10;
    graph[18][15]=21;
    graph[18][19]=75;
    graph[18][22]=50;

    graph[19][18]=75;
    graph[19][20]=8;

    graph[20][19]=8;

    graph[21][22]=15;

    graph[22][18]=50;
    graph[22][21]=15;
    graph[22][23]=72;

    graph[23][7]=102;
    graph[23][22]=72;
    graph[23][24]=13;

    graph[24][23]=13;

    graph[25][10]=17;
    graph[25][26]=62;
    graph[25][28]=60;

    graph[26][25]=62;
    graph[26][27]=26;
    graph[26][30]=60;

    graph[27][26]=26;

    graph[28][12]=31;
    graph[28][25]=60;
    graph[28][29]=25;

    graph[29][28]=25;
    graph[29][30]=37;

    graph[30][26]=60;
    graph[30][29]=37;
    graph[30][31]=73;

    graph[31][13]=94;
    graph[31][30]=73;
    graph[31][32]=24;

    graph[32][31]=24;
    graph[32][33]=9;
    graph[32][34]=33;

    graph[33][14]=75;
    graph[33][32]=9;
    graph[33][34]=30;

    graph[34][32]=33;
    graph[34][33]=30;
}

int minDistance(int dist[], bool sptSet[]) {
    // 최소 거리를 찾는 로직
    int min = INT_MAX, min_index = -1;
    for (int v = 0; v < V; v++)
        if (sptSet[v] == false && dist[v] <= min)
            min = dist[v], min_index = v; 
    return min_index;
}

void printPath(int parent[], int j) {
    // 경로를 출력하는 로직
     if (parent[j] == -1) 
        return;
    printPath(parent, parent[j]); //재귀로 계속 위의 부모node를 입력받아 경로를 역추적하여 출력한다.
    printf("%d ", j + 1);
}

void dijkstra(int graph[V][V], int src, int dest) {
    // 다익스트라 알고리즘 구현
    int dist[V];
    bool sptSet[V];
    int parent[V];

    for (int i = 0; i < V; i++) {
        parent[i] = -1;
        dist[i] = INF;
        sptSet[i] = false;
    }

    dist[src] = 0;

    for (int count = 0; count < V - 1; count++) { //V-1인이유:마지막 남은 노드는 자연스럽게 다음 노드가 되기때문.
        int u = minDistance(dist, sptSet);
        sptSet[u] = true;
        for (int v = 0; v < V; v++)
            if (!sptSet[v] && graph[u][v] && dist[u] != INF && ((long long)dist[u] + graph[u][v] < dist[v])) { //최단경로에 아직 포함되어있지않고, 전 노드에 연결되어있으며, 
                parent[v] = u;
                dist[v] = dist[u] + graph[u][v];
            }
    }

    printf("Distance from Node %d to Node %d is: %d\n", src + 1, dest + 1, dist[dest]);
    printf("Path: %d ", src + 1);
    printPath(parent, dest);
}

int main() {
    int graph[V][V];
    initializeGraph(graph);
    
    NodeLocation nodeLocations[V] = {
        // 노드 위치 초기화 {노드번호,위도,경도}
        {0, 37.30006, 126.8377},
        {1, 37.29985, 126.8371},
        {2, 37.29980, 126.8370},
        {3, 37.29925, 126.8374},
        {4, 37.29911, 126.8370},
        {5, 37.29884, 126.8376},
        {6, },
        {7, },
        {8, },
        {9, },
        {10, },
        {11, },
        {12, },
        {13, },
        {14, },
        {15, },
        {16, },
        {17, },
        {18, },
        {19, },
        {20, },
        {21, },
        {22, },
        {23, },
        {24, },
        {25, },
        {26, },
        {27, },
        {28, },
        {29, },
        {30, },
        {31, },
        {32, },
        {33, },
        {34, }
    };

    // 사용자의 현재 위치와 목적지 설정
    double userLatitude = 48.8566; // 현재 위치의 위도 예시
    double userLongitude = 2.3522;  // 현재 위치의 경도 예시
    int nearestNodeId = findNearestNode(userLatitude, userLongitude, nodeLocations, V);

    // 목적지 설정 및 다익스트라 알고리즘으로 경로 계산
    int src = nearestNodeId;
    int dest = 34; // 예시 목적지
    dijkstra(graph, src, dest);

    // 사용자의 현재 방향과 목적지 방향을 기반으로 방향 지시 생성
    // 이 부분은 실제 GPS 데이터를 사용하여 반복적으로 업데이트해야 합니다.
    double nextNodeLatitude = nodeLocations[dest].latitude;
    double nextNodeLongitude = nodeLocations[dest].longitude;
    double userBearing = Bearing(userLatitude, userLongitude, nextNodeLatitude, nextNodeLongitude);
    double targetBearing = userBearing; // 실제 구현에서는 다음 노드로의 방향을 계산해야 합니다.
    generateDirection(userBearing, targetBearing);

    return 0;
}
