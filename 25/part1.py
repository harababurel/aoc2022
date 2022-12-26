#!/usr/bin/env python3
import sys


def decode(s):
    f = 1
    x = 0

    for c in s[::-1]:
        if c in '12':
            x += int(c) * f
        if c == '-':
            x -= f
        if c == '=':
            x -= 2 * f
        f *= 5

    return x


ans = 0
for line in map(str.strip, sys.stdin):
    print("%s: %d" % (line, decode(line)))
    ans += decode(line)

# 33841257499180
# 2--2-0=--0--100-=210

print()
s = '2--2-0=--0--100-=210'
print("got:      %d" % decode(s))
print("expected: %d" % ans)

print("Answer is %s" % s)
