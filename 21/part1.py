#!/usr/bin/env python3
import sys
from pprint import pprint

lines = list(map(str.strip, sys.stdin))

monkeys = {}

for line in lines:
    parts = line.split(' ')
    monkey = parts[0][:-1]
    if len(parts) == 2:
        val = int(parts[1])
        monkeys[monkey] = val
    else:
        a, op, b = parts[1:]
        monkeys[monkey] = (a, op, b)


def compute(a, op, b):
    return eval("%d %s %d" % (a, op, b))


while type(monkeys['root']) not in (int, float):
    for m in monkeys.keys():
        if type(monkeys[m]) in (int, float):
            continue

        a, op, b = monkeys[m]

        if type(a) == str and type(monkeys[a]) in (int, float):
            a = monkeys[a]

        if type(b) == str and type(monkeys[b]) in (int, float):
            b = monkeys[b]

        if type(a) in (int, float) and type(b) in (int, float):
            monkeys[m] = compute(a, op, b)
        else:
            monkeys[m] = (a, op, b)

    pprint(monkeys)

print("root is %r" % monkeys['root'])
