#!/usr/bin/env python3
import sys

lines = list(map(str.strip, sys.stdin))

t = 1
x = 1

xs = {}

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

print("tmax = %d" % max(xs.keys()))

ans = 0
for t in range(20, 1 + max(xs.keys()), 40):
    ans += t * xs[t]
    print("Adding %d * %d = %d" % (t, xs[t], t * xs[t]))

print(ans)
