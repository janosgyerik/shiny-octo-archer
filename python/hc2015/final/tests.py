import unittest

# import solver
# from solver import Server

from solver import Balloon


class TestSolver(unittest.TestCase):
    def test_find_targets_within_range(self):
        radius = 3
        row = 4
        col = 5
        b = Balloon(-1, row, col, -1, None, 100, 100, radius)
        self.assertEquals((row, col), b.find_target_within_range([(row, col)]))
        self.assertEquals(None, b.find_target_within_range([(row, col + radius + 1)]))
        self.assertEquals(None, b.find_target_within_range([(row + radius + 1, col)]))
        self.assertEquals(None, b.find_target_within_range([(row - radius - 1, col)]))
        self.assertEquals(None, b.find_target_within_range([(row, col - radius - 1)]))
        self.assertEquals((row, col - radius), b.find_target_within_range([(row, col - radius)]))
        self.assertEquals((row + radius, col - radius), b.find_target_within_range([(row + radius, col - radius)]))


if __name__ == '__main__':
    unittest.main()
