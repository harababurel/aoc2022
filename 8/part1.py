#!/usr/bin/env python3
import sys

grid = list(map(list, map(str.strip, sys.stdin)))
grid = [list(map(int, line)) for line in grid]

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)

dirs = [up, down, left, right]

dirname = {
    up: "up",
    down: "down",
    left: "left",
    right: "right",
}


def partial_max(grid, i, j, d):
    if i in (-1, len(grid)) or j in (-1, len(grid[0])):
        return -1
    return max(grid[i][j], partial_max(grid, i + d[0], j + d[1], d))


def is_visible(grid, i, j, d):
    return grid[i][j] > partial_max(grid, i + d[0], j + d[1], d)


ans = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        visible_from = list(filter(lambda d: is_visible(grid, i, j, d), dirs))
        if visible_from:
            print("Tree %s (%d, %d) is visible from directions: %r" %
                  (grid[i][j], i, j,
                   list(map(lambda d: dirname[d], visible_from))))
            ans += 1
    print()
print(ans)
