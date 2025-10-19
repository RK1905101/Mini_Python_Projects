# 🧮 Dijkstra's Shortest Path Algorithm – Python Project Suite

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python" alt="Python Badge">
  <img src="https://img.shields.io/badge/Algorithms-Graph%20Theory-orange" alt="Graph Badge">
  <img src="https://img.shields.io/github/license/RK1905101/Mini_Python_Projects" alt="License Badge">
  <img src="https://img.shields.io/badge/UI-Tkinter-green" alt="Tkinter Badge">
</p>

A comprehensive collection of **Dijkstra’s Shortest Path Algorithm** implementations in Python — from a basic CLI version to an interactive GUI visualizer built with **Tkinter**.  

This project helps learners understand graph traversal, priority queues, and shortest-path computation in a **progressive**, hands-on way.

---

## 🧠 Overview

**Dijkstra’s Algorithm** is one of the most fundamental algorithms in computer science used to find the shortest paths between nodes in a weighted graph.

This project suite includes **four different implementations**:

| Version | Type | Description |
|----------|------|-------------|
| 🧩 `dijkstra_shortest_path.py` | CLI | Core implementation using a priority queue (`heapq`) |
| 🌐 `dijkstra_visualizer.py` | Matplotlib | Visual graph rendering using `networkx` + `matplotlib` |
| 💬 `dijkstra_interactive.py` | Console | Dynamic user input for custom graphs, edges, and weights |
| 🎨 `dijkstra_gui.py` | Tkinter GUI | Full graphical version – add nodes, edges, and visualize paths interactively |

---

## 📂 Project Structure

```
Graph_Algorithms/
│
├── dijkstra_shortest_path.py      # Core CLI version
├── dijkstra_visualizer.py         # Visual version with matplotlib
├── dijkstra_interactive.py        # Interactive console version
├── dijkstra_gui.py                # Tkinter GUI visualizer
└── README.md                      # Documentation
```

---

## ⚙️ Installation & Setup

**1. Clone this Repository**
```bash
git clone https://github.com/RK1905101/Mini_Python_Projects.git
cd Mini_Python_Projects/Graph_Algorithms
```

**2. Install Required Libraries**
Only the visualizer version needs external dependencies:
```bash
pip install networkx matplotlib
```

The other three scripts use only Python’s standard library.

**3. Run Any Version**
```bash
# CLI version
python dijkstra_shortest_path.py

# Matplotlib visual version
python dijkstra_visualizer.py

# Interactive console version
python dijkstra_interactive.py

# GUI version (Tkinter)
python dijkstra_gui.py
```

---

## 💻 Usage Guide

### 🧩 1. CLI Version
- Edit the example graph dictionary or use the default one.
- Input the start node (e.g., `A`), and the program prints shortest distances.

### 🌐 2. Visualizer Version
- Uses `networkx` and `matplotlib` to show a visual graph.
- The shortest path is highlighted in **red**.
- A popup shows the total distance and route.

### 💬 3. Interactive Console Version
- Input any number of nodes (e.g., `A`, `B`, `C`, ...).
- Add edges like:  
  ```
  A B 2
  A C 4
  B C 1
  done
  ```
- Choose start and end nodes → see shortest path and distances.

### 🎨 4. Tkinter GUI Version
- Click **“Add Node”** → click anywhere on the canvas to create nodes.
- Click **“Add Edge”** → click two nodes, then enter a weight.
- Select start and end nodes from dropdowns.
- Click **“Find Shortest Path”** → path highlights in red and result pops up.

---

## 🧩 Key Concepts Illustrated
- Graph Representation (Adjacency List)
- Priority Queue (`heapq`)
- Greedy shortest-path computation
- Path reconstruction via parent mapping
- Visualization with `networkx` and `Tkinter`
- Modular programming for multiple UI types

---

## 🧑‍💻 Educational Value

| Skill Area | Learned Concept |
|-------------|-----------------|
| Data Structures | Adjacency list, dictionaries, heaps |
| Algorithms | Dijkstra’s shortest path, greedy optimization |
| UI Programming | Tkinter Canvas, event binding |
| Visualization | Dynamic graph rendering |
| Software Design | Modular code structure & user interaction |

---

> “Algorithms are the poetry of logic. Each line leads to elegance through efficiency.”  
> — *Abhishek Sharma*
