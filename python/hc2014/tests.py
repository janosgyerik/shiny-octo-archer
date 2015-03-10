import unittest

import facade


class TestFacade(unittest.TestCase):
    def test_count_painted_within_square(self):
        self.assertEquals(0, facade.count_painted_within_square([[]], 3, 3, 10))
        self.assertEquals(9, facade.count_painted_within_square([[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]], 0, 0, 3))
        self.assertEquals(7, facade.count_painted_within_square([[0, 1, 2, 3], [0, 1, 2, 3], [0, 0, 1, 1]], 0, 0, 3))

    def test_find_suitable_rows(self):
        self.assertEquals([], facade.find_suitable_rows([[]], 3))
        self.assertEquals([(0, [0, 1, 2, 3]), (1, [0, 1, 2, 3])],
                          facade.find_suitable_rows([[0, 1, 2, 3], [0, 1, 2, 3], [0, 0, 1, 1]], 3))
        self.assertEquals([(0, [0, 1, 2, 3])],
                          facade.find_suitable_rows([[0, 1, 2, 3], [0, 1, 2, 2], [0, 0, 1, 1]], 3))

    def test_prefix_sums(self):
        self.assertEquals([[0, 1, 2, 3]], facade.get_prefix_sums(['111']))
        self.assertEquals([[0, 1, 2, 2]], facade.get_prefix_sums(['110']))
        self.assertEquals([[0, 0, 1, 1]], facade.get_prefix_sums(['010']))
        self.assertEquals([[0, 0, 0, 0]], facade.get_prefix_sums(['000']))

    def test_parseInput(self):
        self.assertEquals(['00001111', '11111111', '0000', '00001011'],
                          facade.parseInput(['....####', '########', '....', '....#.##']))

    def test_get_cells_to_paint(self):
        self.assertEquals(set(), facade.get_cells_to_paint(['000']))
        self.assertEquals(set(), facade.get_cells_to_paint(['000', '000', '000']))
        self.assertEquals({(2, 1)}, facade.get_cells_to_paint(['000', '000', '010']))
        self.assertEquals({(1, 0), (1, 1), (2, 1)}, facade.get_cells_to_paint(['000', '110', '010']))

    def test_remove_painted_cells(self):
        cells_to_paint0 = {(1, 0), (1, 1), (2, 1)}

        cells_to_paint = set(cells_to_paint0)
        facade.remove_painted_cells(cells_to_paint, 0, 0, 3)
        self.assertEquals(set(), cells_to_paint)

        cells_to_paint = set(cells_to_paint0)
        facade.remove_painted_cells(cells_to_paint, 1, 1, 3)
        self.assertEquals({(1, 0)}, cells_to_paint)

        cells_to_paint = set(cells_to_paint0)
        facade.remove_painted_cells(cells_to_paint, 2, 1, 3)
        self.assertEquals({(1, 0), (1, 1)}, cells_to_paint)

        cells_to_paint = set(cells_to_paint0)
        facade.remove_painted_cells(cells_to_paint, 1, 2, 3)
        self.assertEquals(cells_to_paint0, cells_to_paint)

    def test_get_blanks_within_square(self):
        self.assertEquals([(0, 0), (0, 1), (0, 2), (2, 0), (2, 2)],
                          facade.get_blanks_within_square(['000', '111', '010'], 0, 0, 3))
        self.assertEquals([(0, 0), (2, 0)], facade.get_blanks_within_square(['011', '111', '011'], 0, 0, 3))
        self.assertEquals([], facade.get_blanks_within_square(['0111', '1111', '0111', '1111'], 1, 1, 3))
        self.assertEquals([(3, 3)], facade.get_blanks_within_square(['0111', '1111', '0111', '1110'], 1, 1, 3))

    def test_apply_commands(self):
        commands = [[True, 2, 2, 1], [False, 2, 2, None]]
        data = [''.join(4 * ['0']), ''.join(4 * ['0']), ''.join(4 * ['0']), ''.join(4 * ['0']), ''.join(4 * ['0'])]
        self.assertEquals(['0000', '0111', '0101', '0111', '0000'], facade.apply_commands(data, commands))

        commands = [[True, 2, 2, 2], [False, 1, 1, None], [False, 1, 2, None], [False, 1, 3, None], [False, 4, 0, None],
                    [False, 4, 1, None]]
        data = [''.join(7 * ['0']), ''.join(7 * ['0']), ''.join(7 * ['0']), ''.join(7 * ['0']), ''.join(7 * ['0']),
                ''.join(7 * ['0'])]
        self.assertEquals(['1111100', '1000100', '1111100', '1111100', '0011100', '0000000'],
                          facade.apply_commands(data, commands))

    def test_find_suitable_cols(self):
        self.assertEquals([0], facade.find_suitable_cols([0, 1, 2, 3], 3, 3))
        self.assertEquals([], facade.find_suitable_cols([0, 1, 2, 3], 2, 3))
        self.assertEquals([3], facade.find_suitable_cols([0, 1, 1, 1, 2, 2, 3, 4, 4, 4], 4, 3))
        self.assertEquals([0, 4, 5], facade.find_suitable_cols([0, 1, 2, 3, 3, 3, 4, 5, 6, 6], 4, 3))

    def test_create_blank_facade(self):
        self.assertEquals(['0' * 5] * 4, facade.create_blank_facade(4, 5))
        self.assertEquals(['0' * 5] * 5, facade.create_blank_facade(5, 5))
        self.assertEquals(['0' * 8] * 7, facade.create_blank_facade(7, 8))

    def test_write_facade(self):
        pass
        # write_facade(create_blank_facade(1000, 1000), 'output.txt')

    def test_small_example(self):
        data = [
            '0010000',
            '0011100',
            '0010100',
            '0011100',
            '0000100'
        ]
        prefix_sums = facade.get_prefix_sums(data)
        self.assertEquals(
            [[0, 0, 0, 1, 1, 1, 1, 1],
             [0, 0, 0, 1, 2, 3, 3, 3],
             [0, 0, 0, 1, 1, 2, 2, 2],
             [0, 0, 0, 1, 2, 3, 3, 3],
             [0, 0, 0, 0, 0, 1, 1, 1]], prefix_sums)

        brush_size = 3
        suitable_row_limit = 3
        suitable_col_limit = 3

        suitable_rows = facade.find_suitable_rows(prefix_sums, suitable_row_limit)
        self.assertEquals([(1, [0, 0, 0, 1, 2, 3, 3, 3]), (3, [0, 0, 0, 1, 2, 3, 3, 3])],
                          suitable_rows)

        suitable_cols1 = facade.find_suitable_cols(suitable_rows[0][1], brush_size, suitable_col_limit)
        self.assertEquals([2], suitable_cols1)
        suitable_cols2 = facade.find_suitable_cols(suitable_rows[1][1], brush_size, suitable_col_limit)
        self.assertEquals([2], suitable_cols2)

        commands = facade.generate_commands(data, brush_size, suitable_row_limit, suitable_col_limit)
        self.assertEquals([[True, 2, 3, 1], [True, 4, 4, 0], [True, 0, 2, 0], (False, 2, 3, None)], commands)


if __name__ == '__main__':
    unittest.main()
