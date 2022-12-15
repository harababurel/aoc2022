#!/usr/bin/env python3
import sys
import re
import math
from tqdm import trange

lines = list(map(str.strip, sys.stdin))

ss = []
bs = []
xmin, xmax = math.inf, -math.inf
for line in lines:
    match = re.search(
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
        line)
    if match:
        sx, sy, bx, by = map(int, match.group(1, 2, 3, 4))
        xmin = min([xmin, sx, bx, sx - bx, sx + bx])
        xmax = max([xmax, sx, bx, sx - bx, sx + bx])
        ss.append((sx, sy))
        bs.append((bx, by))
        print("Sensor: %d %d, Beacon: %d %d" % (sx, sy, bx, by))
    else:
        print("No match, check input")
        exit(1)


def d(p, q):
    x, y = p
    a, b = q
    return abs(x - a) + abs(y - b)


# target_y = 10
target_y = 2000000
ans = 0

print("Searching between xmin=%d, xmax=%d" % (xmin, xmax))

for x in trange(xmin, xmax + 1):
    possible = True

    for i in range(len(ss)):
        if (x, target_y) == ss[i]:
            possible = False
            break
        if (x, target_y) == bs[i]:
            possible = True
            break

        if d(ss[i], (x, target_y)) <= d(ss[i], bs[i]):
            possible = False
            break

    if not possible:
        ans += 1
        # print("Impossible cell: %d, %d" % (x, target_y))

print("Answer: %d impossible cells" % ans)
