#!/usr/bin/env python3
import sys

print("Ans is %r" % sum(sorted(list(map(lambda p: sum(map(int, p.strip().split('\n'))), ''.join(list(sys.stdin)).split('\n\n'))))[-3:]))
