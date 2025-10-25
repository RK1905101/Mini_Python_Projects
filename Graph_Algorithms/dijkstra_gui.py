# dijkstra_gui.py
# ---------------------------------------------------
# Visual Dijkstra Shortest Path using Tkinter Canvas
# Author: RK1905101
# ---------------------------------------------------

import tkinter as tk
from tkinter import messagebox, simpledialog
import math
import heapq

class GraphGUI:
    def __init__(self, master):
        self.master = master
        master.title("Dijkstra Shortest Path Visualizer")

        # Canvas setup
        self.canvas = tk.Canvas(master, width=800, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Side panel
        frame = tk.Frame(master, padx=10, pady=10)
        frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(frame, text="Dijkstra Visualizer", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(frame, text="Add Node", command=self.enable_add_node).pack(fill="x", pady=5)
        tk.Button(frame, text="Add Edge", command=self.enable_add_edge).pack(fill="x", pady=5)
        tk.Button(frame, text="Find Shortest Path", command=self.run_dijkstra).pack(fill="x", pady=10)
        tk.Button(frame, text="Reset Graph", command=self.reset).pack(fill="x", pady=5)

        # Node selections
        tk.Label(frame, text="Start Node:").pack(pady=2)
        self.start_var = tk.StringVar()
        self.start_menu = tk.OptionMenu(frame, self.start_var, "")
        self.start_menu.pack(pady=2)

        tk.Label(frame, text="End Node:").pack(pady=2)
        self.end_var = tk.StringVar()
        self.end_menu = tk.OptionMenu(frame, self.end_var, "")
        self.end_menu.pack(pady=2)

        # State
        self.mode = None
        self.nodes = {}  # name -> (x, y)
        self.edges = {}  # name -> list of (neighbor, weight)
        self.node_radius = 20
        self.node_count = 0
        self.edge_lines = []

        # Canvas bindings
        self.canvas.bind("<Button-1>", self.on_click)
        self.selected_node = None

    # ---------------- Node & Edge Creation ----------------
    def enable_add_node(self):
        self.mode = "add_node"
        messagebox.showinfo("Mode", "Click anywhere on canvas to add a node.")

    def enable_add_edge(self):
        if len(self.nodes) < 2:
            messagebox.showwarning("Error", "At least two nodes are required.")
            return
        self.mode = "add_edge"
        self.selected_node = None
        messagebox.showinfo("Mode", "Click on two nodes to connect them with an edge.")

    def on_click(self, event):
        if self.mode == "add_node":
            self.add_node(event.x, event.y)
        elif self.mode == "add_edge":
            self.handle_edge_click(event.x, event.y)

    def add_node(self, x, y):
        name = chr(65 + self.node_count)
        self.node_count += 1
        self.nodes[name] = (x, y)
        self.edges[name] = []
        self.canvas.create_oval(
            x - self.node_radius, y - self.node_radius,
            x + self.node_radius, y + self.node_radius,
            fill="lightblue", outline="black", width=2
        )
        self.canvas.create_text(x, y, text=name, font=("Arial", 12, "bold"))
        self.update_dropdowns()

    def handle_edge_click(self, x, y):
        clicked = self.get_node_at(x, y)
        if not clicked:
            return

        if not self.selected_node:
            self.selected_node = clicked
            self.highlight_node(clicked, "yellow")
        else:
            node1 = self.selected_node
            node2 = clicked
            if node1 == node2:
                self.highlight_node(node1, "lightblue")
                self.selected_node = None
                return

            weight = simpledialog.askfloat("Edge Weight", f"Enter weight for edge {node1} - {node2}:")
            if weight is None:
                return

            self.edges[node1].append((node2, weight))
            self.edges[node2].append((node1, weight))

            x1, y1 = self.nodes[node1]
            x2, y2 = self.nodes[node2]
            line = self.canvas.create_line(x1, y1, x2, y2, width=2)
            self.edge_lines.append((line, node1, node2))
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_text(mid_x, mid_y, text=str(weight), font=("Arial", 10, "bold"))

            self.highlight_node(node1, "lightblue")
            self.selected_node = None

    def get_node_at(self, x, y):
        for name, (nx, ny) in self.nodes.items():
            if math.hypot(x - nx, y - ny) <= self.node_radius:
                return name
        return None

    def highlight_node(self, node, color):
        x, y = self.nodes[node]
        self.canvas.create_oval(
            x - self.node_radius, y - self.node_radius,
            x + self.node_radius, y + self.node_radius,
            fill=color, outline="black", width=2
        )
        self.canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))

    def update_dropdowns(self):
        menu1 = self.start_menu["menu"]
        menu2 = self.end_menu["menu"]
        menu1.delete(0, "end")
        menu2.delete(0, "end")
        for node in self.nodes.keys():
            menu1.add_command(label=node, command=lambda value=node: self.start_var.set(value))
            menu2.add_command(label=node, command=lambda value=node: self.end_var.set(value))

    # ---------------- Dijkstra Algorithm ----------------
    def run_dijkstra(self):
        start = self.start_var.get()
        end = self.end_var.get()

        if not start or not end:
            messagebox.showwarning("Warning", "Please select both start and end nodes.")
            return
        if start not in self.nodes or end not in self.nodes:
            messagebox.showerror("Error", "Invalid node selected.")
            return

        distances, previous = self.dijkstra(start)
        if distances[end] == float('inf'):
            messagebox.showinfo("Result", f"No path found from {start} to {end}.")
            return

        path = self.reconstruct_path(previous, start, end)
        self.highlight_path(path)
        messagebox.showinfo("Shortest Path",
                            f"Shortest distance from {start} to {end}: {distances[end]}\nPath: {' → '.join(path)}")

    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.nodes}
        distances[start] = 0
        previous = {node: None for node in self.nodes}
        pq = [(0, start)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)
            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.edges[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        return distances, previous

    def reconstruct_path(self, previous, start, end):
        path = []
        current = end
        while current:
            path.append(current)
            current = previous[current]
        path.reverse()
        if path[0] != start:
            return []
        return path

    # ---------------- Visualization ----------------
    def highlight_path(self, path):
        for i in range(len(path) - 1):
            n1, n2 = path[i], path[i + 1]
            x1, y1 = self.nodes[n1]
            x2, y2 = self.nodes[n2]
            self.canvas.create_line(x1, y1, x2, y2, width=4, fill="red")

    def reset(self):
        self.canvas.delete("all")
        self.nodes.clear()
        self.edges.clear()
        self.node_count = 0
        self.update_dropdowns()


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()
