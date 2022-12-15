#!/usr/bin/env python
import sys
import re
import math
from tqdm import trange, tqdm
import concurrent.futures
import multiprocessing


def d(p, q):
    x, y = p
    a, b = q
    return abs(x - a) + abs(y - b)


dirs = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
]

cache_capacity = 1000


def perimeter(sb):
    s, b = sb

    target_d = d(s, b)
    sx, sy = s
    bx, by = b
    cache = set()

    x, y = b
    for _ in range(4 * d(s, b)):
        # while True:
        for dx, dy in dirs:
            if d((x + dx, y + dy), s) == target_d:
                x += dx
                y += dy
                cache.add((x, y))

                for ddx, ddy in dirs:
                    cache.add((x + ddx, y + ddy))

                if len(cache) > cache_capacity:
                    for p in cache:
                        yield p
                    cache.clear()

                # print("adding %d %d" % (x, y))
                break
        if (x, y) == b:
            break

    for p in cache:
        yield p
    cache.clear()


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

for s_, b_ in tqdm(list(zip(ss, bs))):
    for (x, y) in perimeter((s_, b_)):
        # if x < 0 or y < 0 or x > 20 or y > 20:
        if x < 0 or y < 0 or x > 4000000 or y > 4000000:
            continue

        possible = True
        for s, b in zip(ss, bs):
            if (x, y) == s:
                possible = False
                break
            if (x, y) == b:
                possible = False
                break
            if d(s, (x, y)) <= d(s, b):
                possible = False
                break

        if possible:
            print("Found possible cell for beacon: %d, %d" % (x, y))
            print("Answer: %d" % (x * 4000000 + y))
            exit(0)
