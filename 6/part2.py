#!/usr/bin/env python3
k = 14
s = input()
for i in range(k, len(s)+1):
    if len(set(s[i-k:i])) == k:
        print(i)
        break
