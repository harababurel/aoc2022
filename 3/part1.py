#!/usr/bin/env python3
import sys

ans = 0
for line in map(str.strip, sys.stdin):
    n = len(line)
    left, right = line[:n // 2], line[n // 2:]

    assert (len(left) == len(right))

    common = set(left).intersection(set(right))
    assert (len(common) == 1)

    x = common.pop()
    ans += ord(x.lower()) - ord('a') + 1
    if x != x.lower():
        ans += 26

print(ans)
