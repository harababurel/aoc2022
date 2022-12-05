#!/usr/bin/env python3
import sys
from collections import defaultdict
from pprint import pprint

lines = list(sys.stdin)
grid = defaultdict(list)

for l in lines:
    if '[' not in l:
        break

    for i in range(1, len(l), 4):
        if l[i] != ' ':
            grid[(i + 3) // 4].append(l[i])

for i in grid.keys():
    grid[i].reverse()

for l in lines:
    if 'move' not in l:
        continue

    parts = l.split(' ')
    qty, src, dst = map(int, (parts[1], parts[3], parts[5]))

    for _ in range(qty):
        grid[dst].append(grid[src].pop())

print(''.join([grid[i][-1] for i in sorted(grid.keys())]))
