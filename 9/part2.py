#!/usr/bin/env python3
import sys
from random import randint

DEBUG = False

dirs = {
    'D': (1, 0),
    'U': (-1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

diags = {
    'DL': (1, -1),
    'DR': (1, 1),
    'UL': (-1, -1),
    'UR': (-1, 1),
}


def touching(x, y, i, j):
    return abs(x - i) <= 1 and abs(y - j) <= 1


def manhattan(x, y, i, j):
    return abs(x - i) + abs(y - j)


rope_length = 10
nodes = [(0, 0) for _ in range(rope_length)]
xmin = xmax = ymin = ymax = 0

trace = set()

for move in list(map(str.split, sys.stdin)):
    d, steps = move[0], int(move[1])

    for _ in range(steps):
        hx, hy = nodes[0]
        nodes[0] = (hx + dirs[d][0], hy + dirs[d][1])

        xmin, xmax = min(xmin, nodes[0][0]), max(xmax, nodes[0][0])
        ymin, ymax = min(ymin, nodes[0][1]), max(ymax, nodes[0][1])

        for i in range(1, len(nodes)):
            hx, hy = nodes[i - 1]
            tx, ty = nodes[i]

            if not touching(hx, hy, tx, ty):
                # as close as possible or touching if distances are equal
                best = min(
                    list(dirs.values()) + list(diags.values()),
                    key=lambda delta:
                    (manhattan(hx, hy, tx + delta[0], ty + delta[1]),
                     touching(hx, hy, tx + delta[0], ty + delta[1])))
                tx += best[0]
                ty += best[1]

            nodes[i] = (tx, ty)
            xmin, xmax = min(xmin, tx), max(xmax, tx)
            ymin, ymax = min(ymin, ty), max(ymax, ty)

        trace.add(nodes[-1])

        if DEBUG:
            print(nodes)
            for x in range(xmin - 3, xmax + 3):
                for y in range(ymin - 3, ymax + 3):
                    c = '.'

                    for i in range(len(nodes)):
                        if (x, y) == nodes[i]:
                            c = str(i)
                    if c == '.':
                        if (x, y) == (0, 0):
                            c = 's'
                        elif (x, y) in trace:
                            c = '#'
                    print(c, end='')
                print()
            print()

print(trace)
print("Answer is: %d" % len(trace))
