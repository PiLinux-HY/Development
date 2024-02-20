import math

V = 35
INF = float('inf')

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

def initialize_graph():
    graph = [[INF if i != j else 0 for j in range(V)] for i in range(V)]
    # Define graph connections here, similar to the C code
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

    return path  # Return the path array

def main():
    graph = initialize_graph()
    # Define your graph connections here

    node_locations = [
        NodeLocation(0, 37.30006, 126.8377),
        NodeLocation(1, 37.29985, 126.8371),
        # Add more nodes as necessary
    ]

    user_lat = 48.8566
    user_lon = 2.3522
    nearest_node_id = find_nearest_node(user_lat, user_lon, node_locations)

    src = nearest_node_id
    dest = 34  # Example destination node ID
    path = dijkstra(graph, src, dest)

    # Removed the path print statement as per request
    # Now the function returns the path array directly

if __name__ == "__main__":
    main()
