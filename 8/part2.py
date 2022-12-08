#!/usr/bin/env python3
import sys
import math

grid = list(map(list, map(str.strip, sys.stdin)))
grid = [list(map(int, line)) for line in grid]

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)

dirs = [up, down, left, right]

ans = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        scores = []
        for d in dirs:
            steps = 0
            ni, nj = i, j
            while True:
                ni, nj = ni + d[0], nj + d[1]
                if ni in (-1, len(grid)) or nj in (-1, len(grid[0])):
                    break
                steps += 1
                if grid[i][j] <= grid[ni][nj]:
                    break
            scores.append(steps)

        print("Tree %d (%d, %d) has scores %r, total is %d" %
              (grid[i][j], i, j, scores, math.prod(scores)))
        ans = max(ans, math.prod(scores))
    print()
print("Answer is %d" % ans)
