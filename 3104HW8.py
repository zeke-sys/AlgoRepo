import array
import math
from collections import deque
import heapq

# implementing Breadth First and Depth First Search
# Note: Choose the next node in numerical order (node 3 is searched before node 5). The adjacency lists are already sorted in this order
# May use the heapq libraries for queues
# Be careful of the formatting for DFS. Each element of the return list is a tuple containing an int and nother tuple: (node_id, (start_time, stop_time))

# Given an adjacency list a,
# bfs(a, u) performs a breadth first search starting at node u and returns a list of nodes in the order in which they were seen
# INPUT: [[1] . [2], [0]], 1 (a 3 node cycle, starting BFS at node 1)
# OUTPUT: [1, 2, 0]
def bfs(a, u):
    n = len(a)
    if u < 0 or u >= n:
        return []
    visited = [False] * n
    order = []
    heap = []
    visited[u] = True
    heapq.heappush(heap, u)
    while heap:
        v = heapq.heappop(heap)
        order.append(v)
        for w in a[v]:
            if 0 <= w < n and not visited[w]:
                visited[w] = True
                heapq.heappush(heap, w)
    return order

# Given an adjacency list a,
# dfs(a) performs a depth first search starting at node 0 and returns a list of nodes in the order in which they were seen, with start and stop times
# INPUT: [[1], [2], [0]] (a 3 node cycle)
# OUTPUT: [(0, (1, 6)), (1, (2, 5)), (2, (3, 4))]
def dfs(a):
    n = len(a)
    color = [0] * n  # 0=white,1=gray,2=black
    times = [(0, 0)] * n
    time = 1

    def visit(u):
        nonlocal time
        color[u] = 1
        start = time
        time += 1
        for v in a[u]:
            if 0 <= v < n and color[v] == 0:
                visit(v)
        color[u] = 2
        stop = time
        time += 1
        times[u] = (start, stop)

    # start at 0 first, then ensure all nodes are explored
    if n > 0 and color[0] == 0:
        visit(0)
    for i in range(n):
        if color[i] == 0:
            visit(i)

    return sorted([(i, times[i]) for i in range(n)], key=lambda x: x[1][0])

# Finding cycles
# Write a function that returns whether a node is part of a cycle
# HINT: Modify the DFS to return early when it finds a cycle
# Given an adjancency list a and an index j, returns True if node j is part of a cycle, False if not
def part_of_a_cycle(a, j):
    n = len(a)
    if j < 0 or j >= n:
        return False
    color = [0] * n  # 0=white,1=gray,2=black
    parent = [-1] * n
    found = [False]  # flag to stop early if cycle containing j found

    def visit(u):
        if found[0]:
            return
        color[u] = 1
        for v in a[u]:
            if found[0]:
                return
            if not (0 <= v < n):
                continue
            if color[v] == 0:
                parent[v] = u
                visit(v)
            elif color[v] == 1:
                # back edge u -> v found, cycle exists
                # collect nodes on stack from u back to v
                x = u
                cycle_nodes = {v}
                while x != v and x != -1:
                    cycle_nodes.add(x)
                    x = parent[x]
                # check if j is in this cycle
                if j in cycle_nodes:
                    found[0] = True
                    return
        color[u] = 2

    for i in range(n):
        if color[i] == 0:
            visit(i)
        if found[0]:
            return True
    return False


# Example Usage
