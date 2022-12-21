#!/usr/bin/env python3
import sys
from pprint import pprint
from copy import deepcopy
from tqdm import trange, tqdm
from concurrent.futures import ThreadPoolExecutor

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


def solve(x):
    ms = deepcopy(monkeys)
    ms['root'] = (ms['root'][0], '==', ms['root'][2])
    ms['humn'] = x
    while type(ms['root']) != bool:
        for m in ms.keys():
            if type(ms[m]) in (int, float):
                continue

            a, op, b = ms[m]

            if type(a) == str and type(ms[a]) in (int, float):
                a = ms[a]

            if type(b) == str and type(ms[b]) in (int, float):
                b = ms[b]

            if type(a) in (int, float) and type(b) in (int, float):
                ms[m] = compute(a, op, b)
            else:
                ms[m] = (a, op, b)

        # pprint(monkeys)

    if ms['root'] == True:
        # return (x, True)
        print("root is %r when humn is %d" % (ms['root'], x))
    # return (x, False)


def expression(m):
    if type(monkeys[m]) != tuple:
        return monkeys[m]

    l, r = expression(monkeys[m][0]), expression(monkeys[m][2])

    if type(l) == str and 'x' not in l:
        l = eval(l)
    if type(r) == str and 'x' not in r:
        r = eval(r)
    return "(%s%s%s)" % (l, monkeys[m][1], r)


monkeys['root'] = (monkeys['root'][0], '==', monkeys['root'][2])
monkeys['humn'] = 'x'
print(expression('root'))

# n_threads = 12
# xmin = 0
# xmax = 10**6
# # t = tqdm(total=(xmax-xmin))
# for x in trange(xmin + int(sys.argv[1]), xmax + 1, n_threads):
#     solve(x)
# # with ThreadPoolExecutor(max_workers=7) as executor:
# #     for (x, ans) in executor.map(solve, range(xmin, xmax+1)):
# #         if ans:
# #             print("root is %r when humn is %d" % (ans, x))

# #         t.update()
