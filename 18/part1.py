#!/usr/bin/env python3
import sys

lines = list(map(str.strip, sys.stdin))

cubes = [tuple(map(int, line.split(','))) for line in lines]

print(lines)
print(cubes)

deltas = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1),
]
ans = 0
for c in cubes:
    for dx, dy, dz in deltas:
        if (c[0] + dx, c[1] + dy, c[2] + dz) not in cubes:
            ans += 1

print(ans)
