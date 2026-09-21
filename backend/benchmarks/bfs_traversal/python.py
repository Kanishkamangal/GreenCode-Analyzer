# Benchmark: BFS Traversal
# Category: Graph
# Algorithm: Breadth First Search - O(V + E)

import sys
from collections import deque

tokens = list(map(int, sys.stdin.buffer.read().split()))

if len(tokens) < 2:
    raise SystemExit

n = tokens[0]
m = tokens[1]

if n <= 0 or m < 0:
    raise SystemExit

required = 2 + 2 * m + 1

if len(tokens) < required:
    raise SystemExit

adj = [[] for _ in range(n)]

index = 2

for _ in range(m):
    u = tokens[index]
    v = tokens[index + 1]
    index += 2

    if 0 <= u < n and 0 <= v < n:
        adj[u].append(v)
        adj[v].append(u)

source = tokens[index]

if source < 0 or source >= n:
    raise SystemExit

visited = [False] * n
queue = deque([source])
visited[source] = True

result = []

while queue:
    node = queue.popleft()
    result.append(node)

    for nxt in adj[node]:
        if not visited[nxt]:
            visited[nxt] = True
            queue.append(nxt)

print(*result)
