import unittest

from color import Color
from puzzle import Puzzle, solve
from tube import Tube

class PuzzleTest(unittest.TestCase):

    def test_solved_empty(self):
        p = Puzzle()
        self.assertTrue(p.is_empty())
        self.assertTrue(p.solved())

    def test_solved_all_solved(self):
        tubes = []
        for c in [Color.blue, Color.red, Color.green, Color.orange]:
            tubes.append(Tube.fill_with(c))

        p = Puzzle(tubes)
        self.assertTrue(p.solved())

    def test_solved_one_tube(self):
        tubes = [
            Tube(),
            Tube.fill_with(Color.red),
            Tube(),
        ]
        p = Puzzle(tubes)
        self.assertTrue(p.solved())

    def test_solved_partial(self):
        tubes = []
        for c in [Color.blue, Color.red, Color.green, Color.orange]:
            tubes.append(Tube.fill_with(c))

        t = Tube.fill_with(Color.fusia, 3)
        tubes.append(t)

        p = Puzzle(tubes, ignore_color_check=True)
        self.assertFalse(p.solved())

    def test_copy(self):
        tubes = [
            Tube(),
            Tube(),
        ]
        for c in [Color.blue, Color.red, Color.green, Color.orange]:
            tubes.append(Tube.fill_with(c))

        p = Puzzle(tubes)
        self.assertTrue(p.tubes[-1].is_empty())
        self.assertTrue(p.tubes[-2].is_empty())

        c = p.copy()
        self.assertNotEqual(id(c), id(p))

        for idx, t in enumerate(p.tubes):
            self.assertNotEqual(id(t), id(c.tubes[idx]))

        p.pop()
        self.assertEqual(len(p.tubes), len(c.tubes) - 1)

    def test_solve_super_simple(self):
        tubes = [
            Tube([Color.red]),
            Tube.fill_with(Color.red, 3),
        ]
        p = Puzzle(tubes)
        s, z, t = solve(p, 2, [])
        self.assertTrue(s)

    def test_solve_simple_two_empty(self):
        tubes = [
            Tube(tid=1),
            Tube(tid=2),
            Tube([Color.red], tid=3),
            Tube.fill_with(Color.red, 3, tid=4),
        ]
        p = Puzzle(tubes)
        s, z, t = solve(p, 4, [])
        self.assertTrue(s)

    def test_solve_simple_two_colors(self):
        tubes = [
            Tube.fill_with(Color.green, 3),
            Tube.fill_with(Color.red, 3),
            Tube(),
            Tube(),
            Tube([Color.green]),
            Tube([Color.red]),
        ]
        p = Puzzle(tubes)
        s, z, t = solve(p, 5, [])
        self.assertTrue(s)

    def test_solve_simple_two_full_colors(self):
        tubes = [
            Tube([Color.orange, Color.purple, Color.orange, Color.purple], tid=1),
            Tube([Color.purple, Color.orange, Color.purple, Color.orange], tid=2),
            Tube(tid=3),
        ]
        p = Puzzle(tubes)
        s, z, t = solve(p, 7, [])
        self.assertTrue(s)

    def test_solve_simple_three_full_colors(self):
        tubes = [
            Tube([Color.purple, Color.red, Color.orange, Color.purple]),
            Tube([Color.purple, Color.red, Color.orange, Color.orange]),
            Tube([Color.red, Color.orange, Color.purple, Color.red]),
            Tube(),
            Tube(),
        ]
        p = Puzzle(tubes)
        s, z, t = solve(p, 11, [])
        self.assertTrue(s)

    def test_solve_seven_full_colors(self):
        tubes = [
            Tube([Color.purple, Color.teal, Color.purple, Color.pink]),
            Tube([Color.red, Color.pink, Color.grey, Color.orange]),
            Tube([Color.teal, Color.light_blue, Color.light_blue, Color.purple]),
            Tube([Color.teal, Color.orange, Color.orange, Color.pink]),
            Tube([Color.red, Color.teal, Color.grey, Color.grey]),
            Tube([Color.light_blue, Color.light_blue, Color.red, Color.purple]),
            Tube([Color.grey, Color.orange, Color.pink, Color.red]),
            Tube(),
            Tube(),
        ]
        p = Puzzle(tubes)
        s, z, t = solve(p, 25, [])
        self.assertTrue(s)


if __name__ == '__main__':
    unittest.main()
