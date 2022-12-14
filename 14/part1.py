#!/usr/bin/env python3
import sys
import time
from collections import defaultdict

lines = list(map(str.strip, sys.stdin))
grid = defaultdict(str)

for line in lines:
    points = list(
        map(lambda s: tuple(map(int, s.split(','))), line.split('->')))
    print(points)

    for i in range(len(points) - 1):
        p, q = points[i:i + 2]
        dx, dy = q[0] - p[0], q[1] - p[1]
        if dx != 0:
            dx //= abs(dx)
        if dy != 0:
            dy //= abs(dy)

        grid[p] = '#'
        while p != q:
            p = (p[0] + dx, p[1] + dy)
            grid[p] = '#'

grid[(500, 0)] = '+'


def display_grid(grid):
    xs = list(map(lambda p: p[0], grid.keys()))
    ys = list(map(lambda p: p[1], grid.keys()))
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    for y in range(ymin - 1, ymax + 2):
        for x in range(xmin - 1, xmax + 2):
            print(grid.get((x, y), '.'), end='')
            # if (x,y) in grid:
            #     print(grid[, end = '')
            # else:
            #     print('.', end='')
        print()
    print()
    time.sleep(0.01)


floor_y = max(
    list(map(lambda p: p[1], filter(lambda p: grid[p] == '#', grid.keys()))))


def is_outside_grid(grid, p):
    return p[1] > floor_y


successful_units = 0
while True:
    x, y = 500, 1

    grid[(x, y)] = '*'
    while True:
        # display_grid(grid)

        if is_outside_grid(grid, (x, y)):
            print("Sand unit has fallen outside the grid")
            print("Answer is: %d units of sand" % successful_units)
            exit(0)

        if grid.get((x, y + 1), '.') == '.':  # below empty
            grid[(x, y)] = '.'
            y += 1
            grid[(x, y)] = '*'
        elif grid.get((x - 1, y + 1), '.') == '.':
            grid[(x, y)] = '.'
            x -= 1
            y += 1
            grid[(x, y)] = '*'
        elif grid.get((x + 1, y + 1), '.') == '.':
            grid[(x, y)] = '.'
            x += 1
            y += 1
            grid[(x, y)] = '*'
        else:
            print("Sand unit has stopped at (%d, %d)" % (x, y))
            successful_units += 1
            break
