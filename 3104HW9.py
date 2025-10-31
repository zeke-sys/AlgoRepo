import array
import math
import time
from datetime import datetime, timedelta
import itertools
import heapq



# implementing Kruskal's and Prim's algorithms for Minimum Spanning Tree
# Input: An edge list with weights [(0,1,1), (0,2,2), (1,2,1)] representing edges (i,j,weight)
# Output: A minimum spanning tree in the form of an edge list with weights: [(0,1,1), (1,2,1)]
# Edge lists are lists of triples (i,j,weight) with i<j, which represents an edge between nodes
# i and j with weight w.
# Sort final edge list in natural order, i.e., (0,1,2) before (1,2,1) before (0,2,0)
def kruskal(a):
    # Helper function to find the root of a node
    def find(parent, i):
        if parent[i] == i:
            return i
        else:
            parent[i] = find(parent, parent[i])
            return parent[i]

    # Helper function to union two subsets
    def union(parent, rank, x, y):
        xroot = find(parent, x)
        yroot = find(parent, y)
        if rank[xroot] < rank[yroot]: # optimize union by rank
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    # Sort edges based on weight
    a.sort(key=lambda x: x[2])
    n = max(max(i, j) for i, j, _ in a) + 1  # Number of nodes
    parent = [i for i in range(n)]
    rank = [0] * n

    mst = [] # resulting minimum spanning tree
    # iterate through sorted edges and apply union-find
    for u, v, w in a: 
        x = find(parent, u)
        y = find(parent, v)
        if x != y:
            # normalize edge endpoints to have smaller index first
            if u <= v:
                mst.append((u, v, w)) # include this edge in MST
            else:
                mst.append((v, u, w))
            union(parent, rank, x, y) # union the sets

    mst.sort()
    return mst

def prim(a):
    n = max(max(i, j) for i, j, _ in a) + 1  # Number of nodes
    adj = [[] for _ in range(n)]
    for u, v, w in a: # build adjacency list
        adj[u].append((v, w))
        adj[v].append((u, w))

    # track visited nodes
    visited = [False] * n
    min_heap = [(0, 0, -1)]  # (weight, current_node, parent_node)
    mst = []

    # Prim's algorithm using a priority queue
    while min_heap:
        weight, u, parent = heapq.heappop(min_heap)
        if visited[u]: # already visited
            continue
        visited[u] = True
        if parent != -1:
            # normalize edge endpoints so smaller index comes first
            if parent <= u:
                mst.append((parent, u, weight)) # add edge to MST
            else:
                mst.append((u, parent, weight))
        for v, w in adj[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (w, v, u)) # push adjacent edges

    mst.sort()
    return mst
    

# Find the most likely mutation tree
# Given a list of RNA fragments, return a spanning tree which maximizes the possibility of mutations
# The algorithm should construct a graph and then run your implementation of Kruskal's or Prim's algorithm on it
# The difficulty lies in determining the correct graph so that a minimum spanning tree in your graph
# corresponds to a maximum product spanning tree in terms of mutation probabilities
def mutation_tree(a):
    n = len(a)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            # Calculate mutation probability as the number of differing characters
            diff = sum(1 for x, y in zip(a[i], a[j]) if x != y)
            prob = 1 / (diff + 1)  # Avoid division by zero
            weight = 1 - prob  # Convert to weight for MST
            edges.append((i, j, weight))
    # compute MST on index-based graph
    mst_indices = kruskal(edges)
    # map MST back to fragment strings and compute total probability product
    mst = []
    total_prob = 1.0
    for u, v, w in mst_indices: # retrieve original fragments
        prob = 1 - w
        mst.append((a[u], a[v], prob)) # edge with mutation probability
        total_prob *= prob
    return mst, total_prob # return total mutation probability of the tree

# Example usage:
if __name__ == "__main__":
    fragments = ["ACGT", "ACGA", "TCGT", "ACGG"]
    mst = mutation_tree(fragments)
    print("Minimum Spanning Tree for Mutation Tree:")
    for edge in mst:
        print(edge)

