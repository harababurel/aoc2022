#!/usr/bin/env python3
import sys

lines = list(map(eval, filter(lambda x: x != '', map(str.strip, sys.stdin))))


def cmp(a, b):
    if type(a) is int and type(b) is int:
        return (a > b) - (a < b)

    if type(a) is int:
        a = [a]
    if type(b) is int:
        b = [b]

    for (x, y) in zip(a, b):
        if cmp(x, y) == 0:
            continue
        return cmp(x, y)

    return cmp(len(a), len(b))


ans = 0
for i in range(len(lines) // 2):
    a, b = lines[2 * i:2 * i + 2]

    print(cmp(a, b), a, b)
    if cmp(a, b) == -1:
        ans += i + 1

print(ans)
