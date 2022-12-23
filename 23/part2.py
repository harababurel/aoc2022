#!/usr/bin/env python3
import sys
from collections import defaultdict
from copy import deepcopy

lines = list(map(str.strip, sys.stdin))

elves = set([(i, j) for j in range(len(lines[0])) for i in range(len(lines))
             if lines[i][j] == '#'])

print('\n'.join(lines))
print(elves)


def display_elves(elves):
    imin = min([e[0] for e in elves])
    imax = max([e[0] for e in elves])
    jmin = min([e[1] for e in elves])
    jmax = max([e[1] for e in elves])

    for i in range(imin - 1, imax + 2):
        for j in range(jmin - 1, jmax + 2):
            if (i, j) in elves:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()


print("Initial state:")
display_elves(elves)
r = 0
while True:
    r += 1
    target = {}
    proposed_by = defaultdict(int)
    for e in elves:
        i, j = e
        above = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1)]
        below = [(i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
        left = [(i - 1, j - 1), (i, j - 1), (i + 1, j - 1)]
        right = [(i - 1, j + 1), (i, j + 1), (i + 1, j + 1)]

        if True not in [
                point in elves for point in above + below + left + right
        ]:
            continue

        dirs = [above, below, left, right]
        for _ in range((r - 1) % 4):
            dirs = dirs[1:] + [dirs[0]]

        for d in dirs:
            if True not in [point in elves for point in d]:
                proposal = d[1]
                target[e] = proposal
                proposed_by[proposal] += 1
                break

    elves_moved = 0
    new_elves = set()
    for e in elves:
        if e in target and proposed_by[target[e]] == 1:
            new_elves.add(target[e])
            elves_moved += 1
        else:
            new_elves.add(e)
    elves = new_elves

    print("After round %d: %d elves moved" % (r, elves_moved))
    # display_elves(elves)

    if elves_moved == 0:
        print("First round where no elf moves: %d" % r)
        exit(0)
