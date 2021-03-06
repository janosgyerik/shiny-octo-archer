def count_painted_within_square(prefix_sums, row, col, size):
    if row + size > len(prefix_sums):
        return 0
    if col + size > len(prefix_sums[0]):
        return 0

    count = 0
    for offset in range(size):
        count += prefix_sums[row + offset][col + size] - prefix_sums[row + offset][col]

    return count


def find_suitable_rows(prefix_sums, limit):
    return [(r, row) for r, row in enumerate(prefix_sums) if row and row[-1] >= limit]


def get_prefix_sums(listStr):
    prefixRows = []
    for st in listStr:
        prefixs = (len(st) + 1) * [0]
        bt = map(int, map(lambda c: c, st))
        total = 0
        for i in range(len(bt)):
            total += bt[i]
            prefixs[i + 1] = total
        prefixRows.append(prefixs)
    return prefixRows


def parseInput(listStr):
    lstStr = []
    for st in listStr:
        newSt = []
        chars = map(lambda c: c, st)
        for c in chars:
            if c == '.':
                newSt.append('0')
            else:
                newSt.append('1')
        lstStr.append(''.join(newSt))
    return lstStr


def get_cells_to_paint(facade):
    cells = set()
    for r, row in enumerate(facade):
        for c, col in enumerate(row):
            if col == '1':
                cells.add((r, c))
    return cells


def remove_painted_cells(cells_to_paint, row, col, brush_size):
    for i in range(brush_size):
        for j in range(brush_size):
            r = row + i
            c = col + j
            cell = (r, c)
            if cell in cells_to_paint:
                cells_to_paint.remove((r, c))


def get_blanks_within_square(facade, row, col, brush_size):
    cells = []
    for i in range(brush_size):
        for j in range(brush_size):
            r = row + i
            c = col + j
            value = facade[r][c]
            if value == '0':
                cells.append((r, c))
    return cells


def replaceInRange(src, first, last, character):
    slice = ''.join((last - first + 1) * [character])
    return src[:first] + slice + src[last + 1:]


def apply_commands(facade, commands):
    for command in commands:
        # paint
        if command[0]:
            size = 2 * command[3]
            r_start = command[1] - size / 2
            r_end = command[1] + size / 2
            c_start = command[2] - size / 2
            c_end = command[2] + size / 2
            for r in range(r_start, r_end + 1):
                row = facade[r]
                facade[r] = replaceInRange(row, c_start, c_end, '1')
        else:  # erase
            r = command[1]
            c = command[2]
            facade[r] = replaceInRange(facade[r], c, c, '0')
    return facade


def write_commands(commands, path):
    with open(path, 'w') as fh:
        fh.write('{}\n'.format(len(commands)))
        for command in commands:
            if command[0]:
                fh.write('PAINTSQ {} {} {}\n'.format(*command[1:]))
            else:
                fh.write('ERASECELL {} {}\n'.format(*command[1:3]))


def find_suitable_cols(row_prefix_sums, brush_size, min_painted):
    cols = []
    for col in range(len(row_prefix_sums) - brush_size):
        if row_prefix_sums[col + brush_size] - row_prefix_sums[col] >= min_painted:
            cols.append(col)
    return cols


def paint(path_to_file, numOfRows, numOfCols):
    fo = open(path_to_file, "r+")
    numOfLines = int(fo.readline())
    Matrix = [[0 for x in range(numOfRows)] for x in range(numOfCols)]
    for i in range(numOfLines):

        str1 = fo.readline()
        strings = str1.split()
        if (strings[0] == "PAINTSQ"):
            row_lower = int(strings[1]) - int(strings[3])
            row_upper = int(strings[1]) + int(strings[3])
            col_lower = int(strings[2]) - int(strings[3])
            col_upper = int(strings[2]) + int(strings[3])

            for j in range(row_lower, row_upper):
                for k in range(col_lower, col_upper):
                    Matrix[i, j] = 1


        else:
            Matrix[strings[1], strings[2]] = 0
    fo.close()

    #### Change this file
    fo2 = open("/home/felixledem/Programming/Google/painted.txt", "w")
    for i in range(716):
        for j in range(1522):
            if Matrix[i][j] == 0:
                fo2.write(".")
            else:
                fo2.write("#")
        fo2.write("\n")
    return 0


def read_facade(path_to_file):
    fo = open(path_to_file, "r+")
    string = fo.readline().split()
    lstStr = []
    for i in range(int(string[0])):
        lstStr.append(fo.readline().strip())
    fo.close()
    return lstStr


def create_blank_facade(row, col):
    facade = []
    for i in range(row):
        facade.append(''.join(col * ['0']))
    return facade


def write_facade(facade, path):
    f = open(path, 'w')
    f.write('{} {}\n'.format(len(facade), len(facade[0])))
    for row in facade:
        nrow = row.replace('0', '.')
        nrow = nrow.replace('1', '#')
        f.write(nrow + '\n')
    f.close()


def print_commands(commands):
    print('\n'.join([' '.join([str(s) for s in x]) for x in commands]))


def generate_commands(facade, brush_size, suitable_row_limit, suitable_col_limit):
    prefix_sums = get_prefix_sums(facade)
    cells_to_paint = get_cells_to_paint(facade)

    paint_commands = []
    erase_commands = set()

    worth_using_brush_limit = brush_size * brush_size // 2 + 2

    for r, row in find_suitable_rows(prefix_sums, suitable_row_limit):
        for col in find_suitable_cols(row, brush_size, suitable_col_limit):
            if count_painted_within_square(prefix_sums, r, col, brush_size) > worth_using_brush_limit:
                real_brush_size = brush_size // 2
                paint_commands.append([True, r + real_brush_size, col + real_brush_size, real_brush_size])

                remove_painted_cells(cells_to_paint, r, col, brush_size)

                for r2, c in get_blanks_within_square(facade, r, col, brush_size):
                    erase_commands.add((False, r2, c, None))

    for row, col in cells_to_paint:
        paint_commands.append([True, row, col, 0])

    return paint_commands + list(erase_commands)


def main():
    listStr = read_facade('inputs/small.txt')
    # listStr = read_facade('inputs/doodle.txt')
    facade = parseInput(listStr)
    # commands = generate_commands(facade, 31, 31, 31)  # 147879
    commands = generate_commands(facade, 3, 3, 3)  # 170445
    # commands = generate_commands(facade, 5, 5, 5)  # 170899
    # commands = generate_commands(facade, 7, 7, 7)  # 167394
    # commands = generate_commands(facade, 17, 17, 17)  # 155689
    # commands = generate_commands(facade, 117, 117, 117)  # 183245
    # commands = generate_commands(facade, 57, 57, 57)  # 172837
    # commands = generate_commands(facade, 33, 33, 33)  # 147881
    # commands = generate_commands(facade, 29, 29, 29)  # 148198
    # print_commands(commands)

    # note: points to paint in the big example: 185309
    print(len(commands))

    facade = create_blank_facade(len(listStr), len(listStr[0]))
    apply_commands(facade, commands)

    write_facade(facade, 'outputs/facade.txt')
    write_commands(commands, 'outputs/commands.txt')


if __name__ == '__main__':
    main()
