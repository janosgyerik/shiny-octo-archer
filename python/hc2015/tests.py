import unittest

import solver
from solver import Server


class TestSolver(unittest.TestCase):
    def test_get_server_rank(self):
        big_but_average, small_and_powerful, medium = Server(10, 10), Server(10, 2), Server(10, 5)
        servers = [big_but_average, small_and_powerful, medium]
        expected = [small_and_powerful, medium, big_but_average]
        self.assertEquals(expected, solver.servers_sorted_by_score(servers))

    def test_parse_input(self):
        pools, rows, servers = solver.parse_input('inputs/small.txt')
        self.assertEquals(2, len(pools))
        self.assertEquals(2, len(rows))
        self.assertEquals(5, len(servers))

    def test_get_available_slot(self):
        row = solver.Row(0, 8)
        row.mark_unavailable(0, 1)
        row.mark_unavailable(2, 1)
        self.assertEquals(3, row.get_available_slot(4))


if __name__ == '__main__':
    unittest.main()
