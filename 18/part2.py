#!/usr/bin/env python3
import sys

lines = list(map(str.strip, sys.stdin))

cubes = set([tuple(map(int, line.split(','))) for line in lines])

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

# Gaps larger than this are considered to be open air outside the drops
MAX_VISITED = 2000


def explore(sx, sy, sz):
    visited = set([])
    q = [(sx, sy, sz)]
    while q:
        x, y, z = q.pop()
        visited.add((x, y, z))

        if len(visited) > MAX_VISITED:  # probably open space
            return set([])

        for dx, dy, dz in deltas:
            nx, ny, nz = x + dx, y + dy, z + dz
            if (nx, ny, nz) not in cubes and (nx, ny, nz) not in visited:
                q.append((nx, ny, nz))
                visited.add((x, y, z))

    if len(visited) < MAX_VISITED:  # probably a self contained air pocket
        return visited


xmin = min(cubes, key=lambda c: c[0])[0]
xmax = max(cubes, key=lambda c: c[0])[0]
ymin = min(cubes, key=lambda c: c[1])[1]
ymax = max(cubes, key=lambda c: c[1])[1]
zmin = min(cubes, key=lambda c: c[2])[2]
zmax = max(cubes, key=lambda c: c[2])[2]

for x in range(xmin, xmax + 1):
    for y in range(ymin, ymax + 1):
        for z in range(zmin, zmax + 1):
            if (x, y, z) not in cubes:
                pocket = explore(x, y, z)

                if len(pocket) > 0:
                    for c in pocket:
                        cubes.add(c)
                    print("Found air pocket sized %d: %r" %
                          (len(pocket), pocket))

ans = 0
for c in cubes:
    for dx, dy, dz in deltas:
        if (c[0] + dx, c[1] + dy, c[2] + dz) not in cubes:
            ans += 1

print(ans)
