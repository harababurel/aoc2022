#!/usr/bin/env python3
import sys

lines = list(map(str.strip, sys.stdin))

t = 1
x = 1

xs = {t: x}

for line in lines:
    if line == 'noop':
        t += 1
        xs[t] = x
    else:
        k = int(line.split(' ')[1])
        t += 1
        xs[t] = x

        t += 1
        x += k
        xs[t] = x

width = 40
for t in range(1, max(xs.keys())):
    cursor = (t - 1) % width
    x = xs[t]

    c = '#' if cursor in [x - 1, x, x + 1] else '.'
    print(c, end='\n' if t % width == 0 else '')
