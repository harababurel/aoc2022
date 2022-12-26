#!/usr/bin/env python3
from copy import deepcopy
from tqdm import trange

dx = 1745
df = 2778

xi = 3314
xf = 1000000000000

fi = 5254

k = (xf - xi) // dx

xc = xi + k*dx
fc = fi + k*df

print(xc)


wind = input()
base = "+-------+"
layer = '|.......|'
HMAX =  10**4

wind_delta = {
    '>': 1,
    '<': -1,
}

grid = [list(base)] + [list(layer) for _ in range(int(HMAX * 1.6))]

shapes = {
    '-': [(0, 0), (1, 0), (2, 0), (3, 0)],
    '+': [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    'L': [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    '|': [(0, 0), (0, 1), (0, 2), (0, 3)],
    '#': [(0, 0), (0, 1), (1, 0), (1, 1)],
}


def display_grid(grid):
    for line in grid[::-1]:
        print(''.join(line))
    print()


def floor(grid):
    return grid.index(list(layer)) - 1


def would_hit_something(grid, rx, ry, shape_key):
    for dx, dy in shapes[shape_key]:
        if grid[ry + dy][rx + dx] != '.':
            return True
    return False


def print_shape_to_grid(grid, rx, ry, shape_key):
    for dx, dy in shapes[shape_key]:
        grid[ry + dy][rx + dx] = '#'


shape_id = 0
wind_id = 0
last = 0
f = {}


to_subtract = 0
for shape_id in range(HMAX):
    shape_key = '-+L|#'[shape_id % len(shapes)]
    # print("Time to place a  %s" % shape_key)

    rx, ry = 3, floor(grid) + 4
    # print_shape_to_grid(grid, rx, ry, shape_key)

    while True:
        current_wind = wind[wind_id % len(wind)]
        wind_id += 1
        if not would_hit_something(grid, rx + wind_delta[current_wind], ry,
                                   shape_key):
            # print("Will apply wind %s" % current_wind)
            rx += wind_delta[current_wind]
        else:
            # print("Applying wind %s would result in a hit" % current_wind)
            pass

        if not would_hit_something(grid, rx, ry - 1, shape_key):  # gravity
            ry -= 1
        else:
            print_shape_to_grid(grid, rx, ry, shape_key)
            break

    if shape_id+1 == 3314:
        fast_forward_shape_id = xc
        fast_forward_f = fc
        print("We are at x=%d, f=%d but we consider it to be x=%d, f=%d" % (shape_id+1, floor(grid), fast_forward_shape_id,  fast_forward_f))
    if shape_id+1 > 3314:
        fast_forward_shape_id += 1
        fast_forward_f += floor(grid) - last

        if fast_forward_shape_id == 10**12:
            print("answer: %d" % fast_forward_f)
            exit(0)


    last = floor(grid)


    # if shape_id+1 == 3314 + 558:
    #     snd = floor(grid)
    #     print("asdf: %d" % floor(grid))


    # f[shape_id + 1] = floor(grid)
    # if (shape_id + 181) % 1745 == 4:
    #     fg = floor(grid)
    #     print("floor level after %d shapes: %d (+%d)" %
    #           (shape_id + 1, fg, fg - last))
    #     last = fg

# exit(0)

# print("Searching for periods")
# xs = sorted(f.keys())

# possible_periods = set()
# for i in trange(len(xs)):
#     for j in range(i + 1, len(xs)):
#         x1, x2 = xs[i], xs[j]
#         f1, f2 = f[x1], f[x2]
#         dx = x2 - x1
#         df = f2 - f1
#         possible = True

#         k = 0
#         while True:
#             a = x1 + k * dx
#             b = x1 + (k + 1) * dx
#             k += 1

#             if a not in f or b not in f:
#                 break

#             if f[b] - f[a] != df:
#                 possible = False
#                 break

#         if possible and k > 6 and df not in possible_periods:
#             print(
#                 "Found possible period: x1=%d, x2=%d (dx=%d), f1=%d, f2=%d, (df=%d)"
#                 % (x1, x2, dx, f1, f2, df))
#             possible_periods.add(df)
#             for p in range(1, k):
#                 assert f[x1 + p * dx] == f[x1] + p * df

# print(s)
# print(grid)
# display_grid(grid)
# print("floor level: %d" % floor(grid))

# after 3314 shapes: h=5254
print("x_checkpoint = %d (next one: %d)" % (xc, xi+(k+1)*dx))
print("f_checkpoint = %d (next one: %d)" % (fc, fi+(k+1)*df))
print("ans = %d" % fc)

# 1591977077332 too low
# 1591977075454 too low
# 1591977077350 bad

# to try:
# 1591977077348 bad
# 1591977077352 correct
