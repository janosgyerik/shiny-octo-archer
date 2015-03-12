def find_leader(arr):
    """
    Let us consider a sequence a0, a1, ..., an-1
    The leader of this sequence is the element whose value occurs more than n times.
    :param arr: the sequence
    :return: leader if exists, or else None
    """
    size = 0
    candidate = None
    for num in arr:
        if size == 0:
            candidate = num
            size = 1
        elif candidate == num:
            size += 1
        else:
            size -= 1

    if size > 0:
        if arr.count(candidate) > len(arr) // 2:
            return candidate

    return None


def main():
    pass
    # data = parse_input('inputs/small.txt')
    # data = parse_input('inputs/large.txt')
    # data = parse_input('inputs/other.txt')
    #
    # commands = solve(data)
    # output = apply_commands(commands)
    #
    # write_output(output, 'outputs/output-small.txt')
    # write_commands(commands, 'outputs/commands.txt')


if __name__ == '__main__':
    main()
