from collections import deque
import heapq


def reconstruct(parent, start, goal):
    if goal not in parent and goal != start:
        return []

    path = []
    node = goal

    while node != start:
        path.append(node)
        node = parent[node]

    path.append(start)
    path.reverse()
    return path


# -------- BFS --------
def bfs(maze, start, goal):
    queue = deque([start])
    visited = {start}
    parent = {}
    explored = []

    while queue:
        node = queue.popleft()
        explored.append(node)

        if node == goal:
            return reconstruct(parent, start, goal), explored

        for neighbor in maze.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)

    return [], explored


# -------- DFS --------
def dfs(maze, start, goal):
    stack = [start]
    visited = set()
    parent = {}
    explored = []

    while stack:
        node = stack.pop()

        if node in visited:
            continue
        visited.add(node)
        explored.append(node)

        if node == goal:
            return reconstruct(parent, start, goal), explored

        for neighbor in maze.neighbors(node):
            if neighbor not in visited:
                parent[neighbor] = node
                stack.append(neighbor)

    return [], explored


# -------- A* --------
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def astar(maze, start, goal):
    heap = [(0, start)]
    parent = {}
    g_cost = {start: 0}
    explored = []
    visited = set()

    while heap:
        _, node = heapq.heappop(heap)

        if node in visited:
            continue
        visited.add(node)
        explored.append(node)

        if node == goal:
            return reconstruct(parent, start, goal), explored

        for neighbor in maze.neighbors(node):
            new_cost = g_cost[node] + 1

            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                f = new_cost + heuristic(neighbor, goal)
                heapq.heappush(heap, (f, neighbor))
                parent[neighbor] = node

    return [], explored