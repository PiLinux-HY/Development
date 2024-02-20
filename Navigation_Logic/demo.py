import math

V = 35
INF = float('inf')

class NodeLocation:
    def __init__(self, nodeId, latitude, longitude):
        self.nodeId = nodeId
        self.latitude = latitude
        self.longitude = longitude

def degreesToRadians(degrees):
    return degrees * (math.pi / 180.0)

def distanceBetweenPoints(lat1, lon1, lat2, lon2):
    phi1 = degreesToRadians(lat1)
    phi2 = degreesToRadians(lat2)
    deltaPhi = degreesToRadians(lat2 - lat1)
    deltaLambda = degreesToRadians(lon2 - lon1)
    a = math.sin(deltaPhi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(deltaLambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6371e3 * c

def Bearing(lat1, lon1, lat2, lon2):
    phi1 = degreesToRadians(lat1)
    lambda1 = degreesToRadians(lon1)
    phi2 = degreesToRadians(lat2)
    lambda2 = degreesToRadians(lon2)
    deltaLambda = lambda2 - lambda1
    X = math.cos(phi2) * math.sin(deltaLambda)
    Y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(deltaLambda)
    bearingRadians = math.atan2(X, Y)
    bearingDegrees = (bearingRadians * (180.0 / math.pi) + 360.0) % 360.0
    return bearingDegrees

def generateDirection(userBearing, targetBearing):
    angleDifference = (targetBearing - userBearing + 360) % 360
    if angleDifference > 315 or angleDifference <= 45:
        print("Continue straight")
    elif angleDifference > 45 and angleDifference <= 135:
        print("Turn right")
    elif angleDifference > 135 and angleDifference <= 225:
        print("Make a U-turn")
    elif angleDifference > 225 and angleDifference <= 315:
        print("Turn left")

def findNearestNode(userLat, userLon, nodeLocations):
    nearestNodeId = -1
    nearestDistance = INF
    for i, node in enumerate(nodeLocations):
        dist = distanceBetweenPoints(userLat, userLon, node.latitude, node.longitude)
        if dist < nearestDistance:
            nearestNodeId = i
            nearestDistance = dist
    return nearestNodeId

def initializeGraph():
    graph = [[INF if i != j else 0 for j in range(V)] for i in range(V)]
    # Add your edges here
    # Example: graph[0][1] = 60
    return graph

def minDistance(dist, sptSet):
    min_val = INF
    min_index = -1
    for v in range(V):
        if not sptSet[v] and dist[v] <= min_val:
            min_val = dist[v]
            min_index = v
    return min_index

def printPath(parent, j):
    if parent[j] == -1:
        return
    printPath(parent, parent[j])
    print(j + 1, end=" ")

def dijkstra(graph, src, dest):
    dist = [INF] * V
    sptSet = [False] * V
    parent = [-1] * V
    dist[src] = 0
    for _ in range(V - 1):
        u = minDistance(dist, sptSet)
        sptSet[u] = True
        for v in range(V):
            if not sptSet[v] and graph[u][v] and dist[u] != INF and dist[u] + graph[u][v] < dist[v]:
                parent[v] = u
                dist[v] = dist[u] + graph[u][v]
    print(f"Distance from Node {src + 1} to Node {dest + 1} is: {dist[dest]}")
    print("Path:", src + 1, end=" ")
    printPath(parent, dest)

nodeLocations = [
    NodeLocation(0, 37.30006, 126.8377),
    NodeLocation(1, 37.29985, 126.8371),
    # Add more nodes as needed
]

graph = initializeGraph()
# Define edges in your graph

userLatitude = 48.8566
userLongitude = 2.3522
nearestNodeId = findNearestNode(userLatitude, userLongitude, nodeLocations)

src = nearestNodeId
dest = 33  # Adjust based on the actual number of nodes

dijkstra(graph, src, dest)

# Assuming we have userBearing and targetBearing, for demonstration let's use the same location
if dest < len(nodeLocations):
    nextNodeLatitude = nodeLocations[dest].latitude
    nextNodeLongitude = nodeLocations[dest].longitude
    userBearing = Bearing(userLatitude, userLongitude, nextNodeLatitude, nextNodeLongitude)
    targetBearing = userBearing  # This should be calculated based on actual routing logic
    generateDirection(userBearing, targetBearing)
else:
    print("Destination node is out of range")
