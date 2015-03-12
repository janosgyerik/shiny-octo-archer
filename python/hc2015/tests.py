import unittest

# memo: keyboard shortcuts in PyCharm:
#   run all tests:      Control Shift R
#   run single test:    inside the test method body, Control Shift R
#   re-run last:        Control R

import solver


class TestSolverExample(unittest.TestCase):
    def test_find_leader_6_8_4_6_8_6_6(self):
        self.assertEquals(6, solver.find_leader([6, 8, 4, 6, 8, 6, 6]))

    def test_find_leader_6_8_6(self):
        self.assertEquals(6, solver.find_leader([6, 8, 6]))

    def test_find_leader_6_6(self):
        self.assertEquals(6, solver.find_leader([6, 6]))

    def test_find_leader_6_7_7_7_6(self):
        self.assertEquals(7, solver.find_leader([6, 7, 7, 7, 6]))

    def test_find_leader_6_7_7_6(self):
        self.assertEquals(None, solver.find_leader([6, 7, 7, 6]))

    def test_find_leader_6_7_8(self):
        self.assertEquals(None, solver.find_leader([6, 7, 8]))

    def test_find_leader_6_7(self):
        self.assertEquals(None, solver.find_leader([6, 7]))

    def test_find_leader_6(self):
        self.assertEquals(6, solver.find_leader([6]))

    def test_find_leader_empty(self):
        self.assertEquals(None, solver.find_leader([]))


class TestSolver(unittest.TestCase):
    def test_find_leader_6_8_4_6_8_6_6(self):
        pass


if __name__ == '__main__':
    unittest.main()
