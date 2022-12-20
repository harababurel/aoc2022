#!/usr/bin/env python3
from copy import deepcopy

xs = list(map(int, input().split()))
ys = deepcopy(xs)
ni = [i for i in range(len(xs))]
print(xs)
print("Initial state:  %r (ni = %r)" % (ys, ni))
for i in range(len(xs)):
    j = ni[i]
    x = ys[j]
    moves = abs(x)
    print("Time to move value %d by %d positions" % (x, x))

    # if moves < 0 and abs(moves) > j: # it will wrap around left end
    #     moves = len(xs) - abs(moves)-1 # replace with complementary moves
    #     print("Will move by %d instead of %d" % (moves, x))
    # elif moves > 0 and x + moves >= len(xs):
    #     moves = len(xs)-moves-1

    while moves > 0:
        moves -= 1
        already_moved = False
        if x > 0:
            nj = j + 1
            if nj >= len(xs):
                assert(False)
            else:
                ni[j] += 1
                ni[j+1] -= 1
        else:
            nj = j - 1

            if nj < 0:
                print("Doing a fancy left end move")
                ys = ys[1:] + [ys[0]]
                # for k in range(1, len(ys)):
                #     ni[k] -= 1
                nj = len(xs)-1
                # ni[0] = len(xs)-1
                already_moved = True
                print("After fancy swap: %r (ni = %r)" % (ys, ni))
                moves += 1 # this one doesn't count
            else:
                ni[j] -= 1
                ni[j-1] += 1


        if not already_moved:
            # nj = (nj + len(xs)) % len(xs)
            print("swapping indices %d with %d (vals %d and %d)" % (j, nj, ys[j], ys[nj]))
            # ni[j], ni[nj] = nj, j
            ys[j], ys[nj] = ys[nj], ys[j]
            print("ni = %r" % ni)
        j = nj
    print("After moving %d: %r (ni = %r)" % (x, ys, ni))
    print()

    if i==3:
        break

print(ys)
