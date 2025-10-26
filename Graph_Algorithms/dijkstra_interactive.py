# dijkstra_interactive.py
# ------------------------------------------------------
# Interactive Dijkstra's Algorithm implementation
# Users can input any number of nodes, edges, and weights.
# ------------------------------------------------------

import heapq

def dijkstra(graph, start):
    # Initialize distances and priority queue
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    previous = {node: None for node in graph}

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous


def build_graph():
    print("\n--- BUILD YOUR GRAPH ---")
    n = int(input("Enter number of nodes: "))
    graph = {}

    print("\nEnter node names (e.g., A, B, C...):")
    nodes = []
    for i in range(n):
        node = input(f"Node {i+1}: ").strip().upper()
        graph[node] = []
        nodes.append(node)

    print("\nEnter edges in the format: Source Destination Weight")
    print("Type 'done' when finished adding edges.\n")

    while True:
        edge_input = input("Edge: ").strip()
        if edge_input.lower() == "done":
            break
        try:
            src, dest, weight = edge_input.split()
            weight = float(weight)
            if src not in graph or dest not in graph:
                print("❌ Invalid node name! Try again.")
                continue
            graph[src].append((dest, weight))
            graph[dest].append((src, weight))  # Undirected by default
        except ValueError:
            print("❌ Invalid format! Please use: A B 4")

    return graph, nodes


def reconstruct_path(previous, start, end):
    path = []
    current = end
    while current:
        path.append(current)
        current = previous[current]
    path.reverse()
    if path[0] != start:
        return None  # no valid path
    return path


if __name__ == "__main__":
    print("✨ Dijkstra's Shortest Path Finder ✨")
    graph, nodes = build_graph()

    start = input("\nEnter start node: ").strip().upper()
    end = input("Enter destination node: ").strip().upper()

    if start not in graph or end not in graph:
        print("❌ Invalid start or end node!")
    else:
        distances, previous = dijkstra(graph, start)
        path = reconstruct_path(previous, start, end)

        print("\n--- RESULTS ---")
        print(f"Shortest distance from {start} to {end}: {distances[end]}")
        if path:
            print(f"Shortest path: {' → '.join(path)}")
        else:
            print("No path found between the given nodes!")

        print("\nAll shortest distances from", start)
        for node, dist in distances.items():
            print(f"{start} → {node}: {dist}")
