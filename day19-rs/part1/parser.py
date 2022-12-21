#!/usr/bin/env python3
import sys

for line in sys.stdin:
    p = line.split(' ')

    print(
        '("%s", Cli {id: %s, ore_robot_cost: %s, clay_robot_cost: %s, obsidian_robot_cost: vec![%s, %s], geode_robot_cost: vec![%s, %s], tmax: 24}),'
        % (p[1][:-1], p[1][:-1], p[6], p[12], p[18], p[21], p[27], p[30]))
