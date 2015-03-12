import unittest

# memo: keyboard shortcuts in PyCharm:
# run all tests:      Control Shift R
# run single test:    inside the test method body, Control Shift R
#   re-run last:        Control R

import solver
from solver import Server


class TestSolver(unittest.TestCase):
    def test_get_server_rank(self):
        s1, s2, s3 = Server(10, 10), Server(10, 2), Server(10, 5)
        servers = [s1, s2, s3]
        expected = [s2, s3, s1]
        self.assertEquals(expected, solver.get_server_rank(servers))

    def test_parse_input(self):
        pools_num, rows, servers = solver.parse_input('inputs/small.txt')
        self.assertEquals(2, pools_num)
        self.assertEquals(2, len(rows))

    def test_get_available_slot(self):
        row = solver.Row(8)
        row.mark_unavailable(0)
        row.mark_unavailable(2)
        print row.get_available_slot(4)


if __name__ == '__main__':
    unittest.main()
