#!/usr/bin/env python3

def to_int(*args):
    return [int(x) for x in args]

with open('inputs/large.txt') as fh:
    _, _, A = to_int(*fh.readline().split(' '))
    _, _, B, T = to_int(*fh.readline().split(' '))

print(' '.join(['1' for _ in range(B)]))


def get_movement(turn, i):
    if turn > A:
        return 0

    target_balloons_per_alt = B / A
    if i < target_balloons_per_alt * (turn + 1):
        return 0
    return 1


for turn in range(T - 1):
    print(' '.join([str(get_movement(turn, i)) for i in range(B)]))
