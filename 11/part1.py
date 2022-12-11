#!/usr/bin/env python3
import sys
from pprint import pprint


def apply_operation(op, x):
    y = x if op[-1] == 'old' else int(op[-1])

    return {'+': x + y, '*': x * y}[op[1]]


rounds = 20
lines = list(map(str.strip, sys.stdin))
monkeys = {}

for i in range(0, len(lines), 7):
    monkey_id = int(lines[i].split(' ')[1][:-1])
    monkeys[monkey_id] = {
        'items':
        list(map(int, map(str.strip, lines[i + 1].split(":")[1].split(',')))),
        'operation':
        lines[i + 2].split('=')[1].strip().split(' '),
        'div_test':
        int(lines[i + 3].split()[-1]),
        'success_target':
        int(lines[i + 4].split()[-1]),
        'fail_target':
        int(lines[i + 5].split()[-1]),
        'inspections':
        0,
    }
    pprint(monkeys[monkey_id])

for _ in range(rounds):
    for monkey_id in sorted(monkeys.keys()):
        m = monkeys[monkey_id]
        for worry in m['items']:
            new_worry = apply_operation(m['operation'], worry) // 3

            dest = m['success_target'] if new_worry % m[
                'div_test'] == 0 else m['fail_target']
            monkeys[dest]['items'].append(new_worry)

        m['inspections'] += len(m['items'])
        m['items'].clear()

xs = sorted(monkeys.values(), key=lambda m: m['inspections'])
print("Answer: %d" % (xs[-1]['inspections'] * xs[-2]['inspections']))
