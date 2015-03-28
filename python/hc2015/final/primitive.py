#!/usr/bin/env python3

def to_int(*args):
    return [int(x) for x in args]

with open('inputs/large.txt') as fh:
    _, _, A = to_int(*fh.readline().split(' '))
    _, _, B, T = to_int(*fh.readline().split(' '))

print(' '.join(['1' for _ in range(B)]))

for _ in range(T - 1):
    print(' '.join(['0' for _ in range(B)]))
