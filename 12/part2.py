#!/usr/bin/env python3
import sys, math
from queue import PriorityQueue

grid = list(map(str.strip, sys.stdin))

deltas = [(-1, 0), (1, 0), (0, 1), (0, -1)]


def canMove(a, b):
    if a == 'S':
        a = 'a'
    if b == 'E':
        b = 'z'
    return ord(b) <= ord(a) + 1


def inside(i, j, n, m):
    return 0 <= i and i < n and 0 <= j and j < m


def dijkstra(grid):
    n = len(grid)
    m = len(grid[0])
    best = [[math.inf for _ in range(m)] for _ in range(n)]
    visited = [[False for _ in range(m)] for _ in range(n)]
    q = PriorityQueue()

    for i in range(n):
        for j in range(m):
            if grid[i][j] in 'Sa':
                best[i][j] = 0
            if grid[i][j] == 'E':
                ti, tj = i, j
            q.put((best[i][j], i, j))

    while not q.empty():
        (d, i, j) = q.get()
        visited[i][j] = True
        if d == math.inf:
            break

        print("Entered %r (%d, %d), d=%r" % (grid[i][j], i, j, d))

        for di, dj in deltas:
            ni, nj = i + di, j + dj

            if inside(ni, nj, n, m) \
                    and not visited[ni][nj] \
                    and canMove(grid[i][j], grid[ni][nj]) \
                    and d + 1 < best[ni][nj]:
                best[ni][nj] = d + 1
                q.put((best[ni][nj], ni, nj))

    return best[ti][tj]


print(dijkstra(grid))
