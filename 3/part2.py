#!/usr/bin/env python3
import sys

ans = 0
lines = list(map(str.strip, sys.stdin))

for i in range(len(lines) // 3):
    a, b, c = lines[3 * i:3 * i + 3]
    common = set(a).intersection(set(b)).intersection(set(c))

    assert (len(common) == 1)
    x = common.pop()

    ans += ord(x.lower()) - ord('a') + 1
    if x != x.lower():
        ans += 26

print(ans)
