#!/usr/bin/env python3
import sys
from typing import List, Optional, Any


class File:

    def __init__(self,
                 filename: str,
                 parent=None,
                 size: Optional[int] = None,
                 isDir: bool = False):
        self.filename = filename
        self.size = size
        self.isDir = isDir

        self.parent: File = self if filename == '/' else parent
        self.children: dict[str, Any] = {}

    def maybeCreateChild(self,
                         child_name: str,
                         size: Optional[int] = None,
                         isDir: bool = True):
        if child_name not in self.children:
            self.children[child_name] = File(child_name, self, size, isDir)

    def getChild(self, child_name: str) -> Optional[Any]:
        return self.children.get(child_name)


root: File = File("/", isDir=True)
current: File = root
assert (root.parent == root)

for line in sys.stdin:
    parts = line.strip().split(' ')
    if line.startswith('$'):
        cmd = parts[1]

        if cmd == 'ls':
            continue
        if cmd == 'cd':
            newDir = parts[2]

            if newDir == '.':
                continue
            elif newDir == '..':
                current = current.parent
            elif newDir == '/':
                current = root
            else:
                current.maybeCreateChild(newDir)
                current = current.getChild(newDir)

    else:  # processing the `ls` output
        size_or_type, filename = parts

        isDir = size_or_type == 'dir'
        size = None if isDir else int(size_or_type)

        current.maybeCreateChild(filename, size, isDir)


def displayTree(current, level=0):
    global ans
    print(2 * level * ' ', '- ', current.filename, end=' ')
    if current.isDir:
        print("(dir, total=%r)" % current.size)
        if current.size <= 100000:
            ans += current.size
    else:
        print("(size=%d)" % current.size)

    for child in current.children.values():
        displayTree(child, level + 1)


def computeSizes(current):
    if current.isDir:
        current.size = 0

    for child in current.children.values():
        computeSizes(child)
        current.size += child.size


ans = 0
computeSizes(root)
displayTree(root)
print("Answer is: %d" % ans)
