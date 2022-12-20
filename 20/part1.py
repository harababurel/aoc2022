#!/usr/bin/env python3
import sys

xs = list(map(int, sys.stdin))
ids = range(len(xs))


class Node:

    def __init__(self, id_, val, prv=None, nxt=None):
        self.id = id_
        self.val = val
        self.prv = prv
        self.nxt = nxt

    def __str__(self):
        # return "Node(id=%d, val=%d)" % (self.id, self.val)
        return "(%d)" % self.val


class List:

    def __init__(self, head=None):
        self.head = head
        # self.tail = head

    def append(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
            node.nxt = node
            node.prv = node
        else:
            self.tail.nxt = node
            self.head.prv = node

            node.nxt = self.head
            node.prv = self.tail
            self.tail = node

    def __str__(self):
        if self.head is None:
            return 'empty list'

        it = self.head
        ret = ""

        while True:
            ret += "%s" % it
            it = it.nxt
            if it == self.head:
                break
            ret += " -> "
        return ret

    def move_right(self, id_, moves=1):
        x = self.head

        while x.id != id_:
            x = x.nxt
            # print('asdf')

        for _ in range(moves):
            y = x.nxt
            # print("x is %s, y is %s" % (x,y))
            x.nxt = y.nxt
            x.prv.nxt = y
            y.prv = x.prv
            y.nxt.prv = x
            x.prv = y
            y.nxt = x

    def move_left(self, id_, moves=1):
        y = self.head
        while y.id != id_:
            y = y.nxt

        for _ in range(moves):
            x = y.prv
            y.prv = x.prv
            y.nxt.prv = x
            x.nxt = y.nxt
            x.prv.nxt = y
            x.prv = y
            y.nxt = x

    def score(self):
        it = self.head
        while it.val != 0:
            it = it.nxt
        ret = 0
        for i in range(1, 3001):
            it = it.nxt
            if i % 1000 == 0:
                ret += it.val
                # print("Adding %d" % it.val)
        return ret


l = List()
print(l)
for id_, x in zip(ids, xs):
    l.append(Node(id_, x))

print(l)
for id_, x in zip(ids, xs):
    if x == 0:
        continue
    print("Moving id=%d, x=%d" % (id_, x))
    if x > 0:
        l.move_right(id_, moves=abs(x))
    else:
        l.move_left(id_, moves=abs(x))

    # print(l)

print("Score: %d" % l.score())
