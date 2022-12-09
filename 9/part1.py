#!/usr/bin/env python3
import sys

DEBUG=False

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

hx, hy = tx, ty = 0, 0
xmin = xmax = ymin = ymax = 0


def touching(x, y, i, j):
    return abs(x - i) <= 1 and abs(y - j) <= 1


def manhattan(x, y, i, j):
    return abs(x - i) + abs(y - j)


trace = set([(tx, ty)])

for move in list(map(str.split, sys.stdin)):
    d, steps = move[0], int(move[1])

    for _ in range(steps):
        hx += dirs[d][0]
        hy += dirs[d][1]

        xmin, xmax = min(xmin, hx), max(xmax, hx)
        ymin, ymax = min(ymin, hy), max(ymax, hy)

        if not touching(hx, hy, tx, ty):
            for dx, dy in list(dirs.values()) + list(diags.values()):
                if manhattan(hx, hy, tx + dx, ty + dy) <= 1:
                    tx += dx
                    ty += dy
                    break
        xmin, xmax = min(xmin, tx), max(xmax, tx)
        ymin, ymax = min(ymin, ty), max(ymax, ty)
        trace.add((tx, ty))

        if DEBUG:
            for x in range(xmin-3, xmax+3):
                for y in range(ymin-3, ymax+3):
                    c = '.'
                    if (x, y) == (hx, hy):
                        c = 'H'
                    elif (x, y) == (tx, ty):
                        c = 'T'
                    elif (x, y) == (0, 0):
                        c = 's'
                    elif (x, y) in trace:
                        c = '#'
                    print(c, end='')
                print()
            print()

if DEBUG:
    print(trace)
print("Answer is: %d" % len(trace))
