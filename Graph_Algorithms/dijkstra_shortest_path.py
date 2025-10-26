# dijkstra_shortest_path.py
# --------------------------
# Find the shortest path from a source node to all others using Dijkstra’s Algorithm.

import heapq

def dijkstra(graph, start):
    # graph is a dictionary: { node: [(neighbor, weight), ...] }
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]  # (distance, node)
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # Skip if we already found a better path
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            # If shorter path found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances


if __name__ == "__main__":
    graph = {
        'A': [('B', 2), ('C', 4)],
        'B': [('A', 2), ('C', 1), ('D', 7)],
        'C': [('A', 4), ('B', 1), ('D', 3)],
        'D': [('B', 7), ('C', 3)]
    }

    start_node = input("Enter start node (A/B/C/D): ").strip().upper()
    if start_node not in graph:
        print("Invalid start node!")
    else:
        shortest_paths = dijkstra(graph, start_node)
        print(f"\nShortest distances from {start_node}:")
        for node, distance in shortest_paths.items():
            print(f"{start_node} → {node}: {distance}")
