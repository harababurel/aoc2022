#!/usr/bin/env python3
import sys
import re
from copy import deepcopy
"""
ABANDONED
Reimplemented in Rust
"""

lines = list(map(str.strip, sys.stdin))
print(lines)

tmax = 24


class Blueprint:
    def __init__(self, b_id, orc, crc, brc, grc):
        self.b_id = b_id
        self.orc = orc
        self.crc = crc
        self.brc = brc
        self.grc = grc


class State:
    def __init__(self, nor=1, ncr=0, nbr=0, ngr=0, o=0, c=0, b=0, g=0, t=0):
        self.nor = nor
        self.ncr = ncr
        self.nbr = nbr
        self.ngr = ngr
        self.o = o
        self.c = c
        self.b = b
        self.g = g
        self.t = t

    def __str__(self):
        return "State at t=%d:\n\tRobots: %d ore, %d clay, %d obsidian, %d geode\n\tResources: %d ore, %d clay, %d obsidian, %d geode" % (
            self.t, self.nor, self.ncr, self.nbr, self.ngr, self.o, self.c,
            self.b, self.g)


ans = 0


def explore(b, state):
    global ans

    if state.t == tmax:

        # if state.g > 0:
        #     print("Reached terminal state with %d geodes: %s" % (state.g, state))

        if state.g > ans:
            ans = state.g
            print("Found new best geode count: %d (quality = %d)" %
                  (ans, b.b_id * ans))
        return state.g

    ret = state.g

    # buy one geode robot
    if state.o >= b.grc[0] and state.b >= b.grc[1]:
        ns = deepcopy(state)
        ns.o -= b.grc[0]
        ns.b -= b.grc[1]

        ns.o += state.nor
        ns.c += state.ncr
        ns.b += state.nbr
        ns.g += state.ngr

        ns.ngr += 1

        ns.t = state.t + 1
        ret = max(ret, explore(b, ns))

    # buy one obsidian robot
    if state.o >= b.brc[0] and state.c >= b.brc[1]:
        ns = deepcopy(state)
        ns.o -= b.brc[0]
        ns.c -= b.brc[1]

        ns.o += state.nor
        ns.c += state.ncr
        ns.b += state.nbr
        ns.g += state.ngr

        ns.nbr += 1

        ns.t = state.t + 1
        ret = max(ret, explore(b, ns))

    # buy one clay robot
    if state.o >= b.crc:
        ns = deepcopy(state)
        ns.o -= b.crc

        ns.o += state.nor
        ns.c += state.ncr
        ns.b += state.nbr
        ns.g += state.ngr

        ns.ncr += 1

        ns.t = state.t + 1
        ret = max(ret, explore(b, ns))

    # buy one ore robot
    if state.o >= b.orc:
        ns = deepcopy(state)
        ns.o -= b.orc

        ns.o += state.nor
        ns.c += state.ncr
        ns.b += state.nbr
        ns.g += state.ngr

        ns.nor += 1

        ns.t = state.t + 1
        ret = max(ret, explore(b, ns))
    # buy nothing
    ns = deepcopy(state)
    ns.o += state.nor
    ns.c += state.ncr
    ns.b += state.nbr
    ns.g += state.ngr
    ns.t = state.t + 1
    ret = max(ret, explore(b, ns))

    return ret


for line in lines:
    match = re.search(
        r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.",
        line)
    if match:
        b_id = int(match.group(1))
        orc = int(match.group(2))
        crc = int(match.group(3))
        brc = (int(match.group(4)), int(match.group(5)))
        grc = (int(match.group(6)), int(match.group(7)))

        if b_id == int(sys.argv[1]):
            print("Processing blueprint with id=%d" % b_id)
            b = Blueprint(b_id, orc, crc, brc, grc)
            print("Best geode count: %d" % explore(b, State()))
            # print("blueprint_id: %d" % b_id)
            # print("ore_robot_cost: %d" % orc)
            # print("clay_robot_cost: %d" % crc)
            # print("obsidian_robot_cost: %d, %d" % brc)
            # print("geode_robot_cost: %d, %d" % grc)
            # print()
            break
    else:
        print("no match, check input or regex")
        exit(1)
