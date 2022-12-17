#!/usr/bin/env python3
import sys
import re
import math
from random import shuffle

flow = {}
dsts = {}

lines = list(map(str.strip, sys.stdin))
for line in lines:
    match = re.search(
        r"Valve (..) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.+)",
        line)
    if match:
        src = match.group(1)
        flow[src] = int(match.group(2))
        dsts[src] = list(map(str.strip, match.group(3).split(',')))
        shuffle(dsts[src])
    else:
        print("no match, check input or regex")
        exit(1)

cost = {}


def compute_shortest_paths():
    for x in flow.keys():
        for y in flow.keys():
            cost[(x, y)] = math.inf
        for y in dsts[x]:
            cost[(x, y)] = 1

    for x in flow.keys():
        cost[(x, x)] = 0

    for z in flow.keys():
        for x in flow.keys():
            for y in flow.keys():
                cost[(x, y)] = min(cost[(x, y)], cost[(x, z)] + cost[(z, y)])


N_ROUNDS = 26
best = 0

compute_shortest_paths()

print('      ' + '  '.join(sorted(flow.keys())))
for x in sorted(flow.keys()):
    print("%s: " % x, end='')
    for y in sorted(flow.keys()):
        print("%r   " % cost[(x, y)], end='')
    print()

nonzero_nodes = list(filter(lambda x: flow[x] > 0, flow.keys()))
print(nonzero_nodes)

best = 0
while True:
    shuffle(nonzero_nodes)
    mid = len(nonzero_nodes) // 2

    xs = nonzero_nodes[:mid]
    ys = nonzero_nodes[mid:]

    flow_per_round = [0 for _ in range(N_ROUNDS + 1)]

    for nodes in (xs, ys):
        current = 'AA'
        t = 0

        for x in nodes:
            distance = cost[(current, x)]
            if t + distance + 1 > N_ROUNDS:
                # total_flow += flow_per_round * (N_ROUNDS - t)
                t += (N_ROUNDS - t)
                break
            else:
                # total_flow += flow_per_round * distance
                t += distance

                # Open newly visited valve
                current = x
                # total_flow += flow_per_round
                t += 1
                flow_per_round[t] += flow[current]

    total_flow = 0
    for i in range(1, N_ROUNDS):
        flow_per_round[i] += flow_per_round[i - 1]
        total_flow += flow_per_round[i]

    if total_flow > best:
        best = total_flow
        print(
            "Found new best=%d using sequence %r for me and %r for elephant" %
            (best, xs, ys))

# Found new best=2343 using sequence ['OK', 'HF', 'CQ', 'GV', 'HX', 'IR', 'UN', 'GR', 'JI', 'XM', 'OH', 'BX', 'GB', 'LC']
