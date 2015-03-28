#!/usr/bin/env python3
import random


def to_int(*args):
    return [int(x) for x in args]

with open('inputs/large.txt') as fh:
    _, _, A = to_int(*fh.readline().split(' '))
    _, _, B, T = to_int(*fh.readline().split(' '))

print(' '.join(['1' for _ in range(B)]))
heights = [1] * B

def get_movement(turn, i):
    if turn > A:
        return 0

    target_balloons_per_alt = B / A
    if i < target_balloons_per_alt * (turn + 1):
        return 0
    return 1


def get_possible_moves(height):
    if height == 0:
        return [1]
    moves = []
    if height > 1:
        moves.append(-1)
    if height < A:
        moves.append(1)
    return moves


def get_random_movement(turn, i):
    movement = random.choice(get_possible_moves(heights[i]))
    heights[i] += movement
    return movement

for turn in range(T - 1):
    print(' '.join([str(get_random_movement(turn, i)) for i in range(B)]))
