#!/usr/bin/env python3
import sys

print("Ans is %d" % max(map(lambda p: sum(map(int, p.strip().split('\n'))), ''.join(list(sys.stdin)).split('\n\n'))))
