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

# for s in dsts.keys():
#     dsts[s] = sorted(dsts[s], key=lambda x: flow[x], reverse=True)

# print("%r" % flow)
# print("%r" % dsts)

# dp[t, s, 0/1] = maximum profit that can be obtained starting at time <t> in node <s>, having it open/closed

# dp = defaultdict(int)
# for t in range(29, -1, -1):
#     for s in flow.keys():

#         # assume s is open
#         pass

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


N_ROUNDS = 30

best = 0


def explore(node, active_so_far, released_so_far, t):
    global best
    if released_so_far > best:
        best = released_so_far
        print("New best released after %d rounds: %d (%r)" %
              (t, best, active_so_far))

    if t == N_ROUNDS:
        return 0

    round_flow = sum(map(flow.get, active_so_far))
    # print("This round at t=%d gives us %d flow" % (t, round_flow))

    for neighbor in dsts[node]:
        explore(neighbor, active_so_far, released_so_far + round_flow, t + 1)

    if flow[node] > 0 and node not in active_so_far:
        explore(node, active_so_far + [node], released_so_far + round_flow,
                t + 1)


compute_shortest_paths()

print('      ' + '  '.join(sorted(flow.keys())))
for x in sorted(flow.keys()):
    print("%s: " % x, end='')
    for y in sorted(flow.keys()):
        print("%r   " % cost[(x, y)], end='')
    print()
# explore("AA", [], 0, 0)

nonzero_nodes = list(filter(lambda x: flow[x] > 0, flow.keys()))
print(nonzero_nodes)

best = 0
while True:
    shuffle(nonzero_nodes)
    t = 0
    current = 'AA'
    flow_per_round = 0
    total_flow = 0

    for x in nonzero_nodes:
        distance = cost[(current, x)]

        if t + distance + 1 > N_ROUNDS:
            # print(
            #     "Can't move any more, will stay in node %s until the end of time"
            #     % current)

            total_flow += flow_per_round * (N_ROUNDS - t)
            t += (N_ROUNDS - t)
            break

        else:
            total_flow += flow_per_round * distance
            t += distance

            # Open newly visited valve
            current = x
            total_flow += flow_per_round
            t += 1
            flow_per_round += flow[current]

    total_flow += flow_per_round * (N_ROUNDS - t)

    if total_flow > best:
        best = total_flow
        print("Found new best=%d using sequence %r" %
              (best, nonzero_nodes[:nonzero_nodes.index(x) + 1]))

# Found new best=1673 using sequence ['OK', 'HF', 'CQ', 'GV', 'GR', 'JI', 'XM', 'OH', 'UN']
