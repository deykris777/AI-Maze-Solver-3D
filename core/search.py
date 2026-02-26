from collections import deque
import heapq

def reconstruct(visited,start,goal):
    if goal not in visited:
        return []
    path=[]
    cur=goal
    while cur:
        path.append(cur)
        cur=visited[cur]
    return path[::-1]

def bfs(maze,start,goal):
    q=deque([start])
    visited={start:None}
    explored=[]
    while q:
        node=q.popleft()
        explored.append(node)
        if node==goal: break
        for nb in maze.neighbors(*node):
            if nb not in visited and nb not in maze.traps:
                visited[nb]=node
                q.append(nb)
    return reconstruct(visited,start,goal), explored

def dfs(maze,start,goal):
    stack=[start]
    visited={start:None}
    explored=[]
    while stack:
        node=stack.pop()
        explored.append(node)
        if node==goal: break
        for nb in maze.neighbors(*node):
            if nb not in visited and nb not in maze.traps:
                visited[nb]=node
                stack.append(nb)
    return reconstruct(visited,start,goal), explored

def heuristic(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def astar(maze,start,goal):
    pq=[]
    heapq.heappush(pq,(0,start))
    visited={start:None}
    cost={start:0}
    explored=[]
    while pq:
        _,node=heapq.heappop(pq)
        explored.append(node)
        if node==goal: break
        for nb in maze.neighbors(*node):
            if nb in maze.traps: continue
            new=cost[node]+1
            if nb not in cost or new<cost[nb]:
                cost[nb]=new
                priority=new+heuristic(nb,goal)
                heapq.heappush(pq,(priority,nb))
                visited[nb]=node
    return reconstruct(visited,start,goal), explored