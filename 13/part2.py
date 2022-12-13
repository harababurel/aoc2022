#!/usr/bin/env python3
import sys
import functools

lines = list(map(eval, filter(lambda x: x != '', map(str.strip, sys.stdin))))
a = [[2]]
b = [[6]]
lines.extend([a, b])

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

lines.sort(key=functools.cmp_to_key(cmp))

print(lines)
print((lines.index(a)+1) * (lines.index(b)+1))
