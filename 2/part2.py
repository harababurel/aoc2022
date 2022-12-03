#!/usr/bin/env python3
import sys

value = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

score = {
    ('A', 'X'): 3,
    ('A', 'Y'): 6,
    ('A', 'Z'): 0,
    ('B', 'X'): 0,
    ('B', 'Y'): 3,
    ('B', 'Z'): 6,
    ('C', 'X'): 6,
    ('C', 'Y'): 0,
    ('C', 'Z'): 3,
}

lines = list(map(tuple, map(str.split, map(str.strip, sys.stdin))))

ans = 0
for l in lines:
    for choice in 'XYZ':
        if l[1]=='X' and score[(l[0], choice)] == 0:
            ans += 0 + value[choice]
        if l[1]=='Y' and score[(l[0], choice)] == 3:
            ans += 3 + value[choice]
        if l[1]=='Z' and score[(l[0], choice)] == 6:
            ans += 6 + value[choice]
print(ans)
