#!/usr/bin/env python3

s = input()
for i in range(4, len(s)+1):
    if len(set(s[i-4:i])) == 4:
        print(i)
        break
