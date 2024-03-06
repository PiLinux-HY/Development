#include <stdio.h>
#include <stdlib.h>
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

int minDistance(long long dist[], bool sptSet[]) {
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
// 수정된 dijkstra 함수와 필요한 다른 함수들은 그대로 유지
void dijkstra(int graph[V][V], int src, int dest, int parent[V]) {
    long long dist[V];
    int i, count, u, v;
    bool sptSet[V];

    for (i = 0; i < V; i++) {
        parent[src] = -1;
        dist[i] = INF;
        sptSet[i] = false;
    }

    dist[src] = 0;

    for (count = 0; count < V - 1; count++) {
        u = minDistance(dist, sptSet);
        sptSet[u] = true;

        for (v = 0; v < V; v++)
            if (!sptSet[v] && graph[u][v] && dist[u] != INF && dist[u] + graph[u][v] < dist[v]) {
                parent[v] = u;
                dist[v] = dist[u] + graph[u][v];
            }
    }
    printf("Distance from Node %d to Node %d is: %lld\n", src + 1, dest + 1, dist[dest]);
    printf("Path: %d\n ", src + 1);
    printPath(parent, dest);
}
// 최단 경로를 역추적하여 다음 노드를 찾는 함수
int getNextNodeInPath(int parent[], int currentNode, int dest) {
    while (parent[dest] != currentNode && parent[dest] != -1) {
        dest = parent[dest];
    }
    return dest;
}

int main() {
    int graph[V][V];
    initializeGraph(graph);
    NodeLocation nodeLocations[V] = {
        // 노드 위치 초기화 {노드번호,위도,경도}
        {0, 37.30007, 126.8377},
        {1, 37.29986, 126.8372},
        {2, 37.29980, 126.8370},
        {3, 37.29927, 126.8373},
        {4, 37.29916, 126.8371},
        {5, 37.29882, 126.8376},
        {6, 37.29857, 126.8377},
        {7, 37.29840, 126.8378},
        {8, },
        {9, },
        {10, 37.29825, 126.8369},
        {11, 37.29816, 126.8369},
        {12, 37.29790, 126.8363},
        {13, 37.29761, 126.8356},
        {14, 37.29752, 126.8353},
        {15, 37.29738, 126.8354},
        {16, 37.29710, 126.8356},
        {17, 37.29700, 126.8353},
        {18, 37.29747, 126.8356},
        {19, 37.29693, 126.8360},
        {20, 37.29696, 126.8360},
        {21, 37.29758, 126.8362},
        {22, 37.29769, 126.8361},
        {23, 37.29798, 126.8368},
        {24, 37.29790, 126.8369},
        {25, 37.29839, 126.8368},
        {26, 37.29891, 126.8365},
        {27, 37.29899, 126.8366},
        {28, 37.29814, 126.8361},
        {29, 37.29836, 126.8361},
        {30, 37.29864, 126.8358},
        {31, 37.29834, 126.8351},
        {32, 37.29821, 126.8349},
        {33, 37.29811, 126.8349},
        {34, 37.29804, 126.8347}
    };
    
    double prevLatitude = 0, prevLongitude = 0; // 사용자의 이전 위치
    bool isFirstUpdate = true; // 첫 위치 업데이트 확인

    // 사용자의 현재 위치 입력
    double userLatitude, userLongitude;
    printf("Enter your current latitude and longitude: ");
    scanf("%lf %lf", &userLatitude, &userLongitude);

    int nearestNodeId = findNearestNode(userLatitude, userLongitude, nodeLocations, V);
    printf("Nearest node to your location: %d\n", nearestNodeId + 1);

    int dest;
    printf("Enter your destination node (1 to %d): ", V);
    scanf("%d", &dest);
    dest--; // 사용자 입력 조정

    int parent[V];
    dijkstra(graph, nearestNodeId, dest, parent);
    
    // 기존 코드에서 다음 노드 방향 계산 부분
    int nextNode = getNextNodeInPath(parent, nearestNodeId, dest);
    double nextNodeLatitude = nodeLocations[nextNode].latitude;
    double nextNodeLongitude = nodeLocations[nextNode].longitude;
    // 초기 방향 지시를 위한 targetBearing 계산
    double targetBearing = Bearing(userLatitude, userLongitude, nextNodeLatitude, nextNodeLongitude);

    // 초기 방향 지시 제공
    generateDirection(targetBearing, targetBearing); // 이제 targetBearing을 사용하여 목표 방향을 제공

    // 사용자 위치 업데이트 및 새로운 방향 지시 로직
    while (true) {
        printf("Enter your current latitude and longitude: ");
        scanf("%lf %lf", &userLatitude, &userLongitude);

        // 사용자의 실제 이동 방향 계산
        double userBearing = Bearing(prevLatitude, prevLongitude, userLatitude, userLongitude);

        // 다음 노드를 찾고, 다음 노드로의 목표 방향 계산
        int currentNode = findNearestNode(userLatitude, userLongitude, nodeLocations, V);
        nextNode = getNextNodeInPath(parent, currentNode, dest);
        nextNodeLatitude = nodeLocations[nextNode].latitude;
        nextNodeLongitude = nodeLocations[nextNode].longitude;
        targetBearing = Bearing(userLatitude, userLongitude, nextNodeLatitude, nextNodeLongitude);

        // 사용자의 현재 방향과 목표 방향을 기반으로 방향 지시 제공
        generateDirection(userBearing, targetBearing);

        // 사용자와 목적지 사이의 거리를 계산하여 목적지 도착 여부 확인
        double distanceToDestination = distanceBetweenPoints(userLatitude, userLongitude, nodeLocations[dest].latitude, nodeLocations[dest].longitude);
        if (distanceToDestination <= 5) {
            printf("You are now very close to your destination.\n");
            break;
        }
        prevLatitude = userLatitude;
        prevLongitude = userLongitude;
    }
    return 0;
}