#!/usr/bin/env python3
import sys

ans = 0
for l in sys.stdin:
    left, right = l.strip().split(',')

    a, b = map(int, left.split('-'))
    x, y = map(int, right.split('-'))

    if (a <= x and x <= b) or (x <= a and a <= y):
        ans += 1

print(ans)
