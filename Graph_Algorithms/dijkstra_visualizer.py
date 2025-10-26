# dijkstra_visualizer.py
# --------------------------
# Visualize Dijkstra’s shortest path using NetworkX and Matplotlib

import heapq
import networkx as nx
import matplotlib.pyplot as plt

def dijkstra(graph, start):
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


def visualize(graph, start, end, previous):
    G = nx.Graph()
    
    # Add edges
    for node, edges in graph.items():
        for neighbor, weight in edges:
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G)
    
    # Build shortest path
    path = []
    current = end
    while current:
        path.append(current)
        current = previous[current]
    path = path[::-1]
    
    # Draw base graph
    nx.draw(G, pos, with_labels=True, node_size=1200, node_color='lightblue', font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    
    # Highlight shortest path
    if len(path) > 1:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='red')
    
    plt.title(f"Shortest Path from {start} to {end}: {' → '.join(path)}")
    plt.show()


if __name__ == "__main__":
    graph = {
        'A': [('B', 2), ('C', 4)],
        'B': [('A', 2), ('C', 1), ('D', 7)],
        'C': [('A', 4), ('B', 1), ('D', 3)],
        'D': [('B', 7), ('C', 3)]
    }
    
    start = input("Enter start node (A/B/C/D): ").strip().upper()
    end = input("Enter end node (A/B/C/D): ").strip().upper()
    
    if start not in graph or end not in graph:
        print("Invalid node name!")
    else:
        distances, previous = dijkstra(graph, start)
        print(f"\nShortest distance from {start} to {end}: {distances[end]}")
        visualize(graph, start, end, previous)
