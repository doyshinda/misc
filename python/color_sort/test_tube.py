import unittest

from color import Color, ColorBox
from tube import Tube, FullException, EmptyException


class TubeTest(unittest.TestCase):

    def test_is_empty(self):
        t = Tube()
        self.assertTrue(t.is_empty())

    def test_tid(self):
        t = Tube(tid=1)
        self.assertEqual(t.tid, 1)

    def test_peek(self):
        t = Tube()
        with self.assertRaises(EmptyException):
            t.peek()

        t = Tube([Color.red, Color.blue])
        self.assertEqual(t.peek(), ColorBox(Color.red))

    def test_pop(self):
        t = Tube([Color.red, Color.blue])
        self.assertEqual(t.pop(), ColorBox(Color.red))

    def test_push(self):
        t = Tube([Color.red, Color.blue])
        t.push(ColorBox(Color.green))
        self.assertEqual(t.peek(), ColorBox(Color.green))

    def test_push_multiple_colors(self):
        t = Tube([Color.red, Color.blue])
        t.push(ColorBox(Color.red))
        self.assertEqual(t.peek(), ColorBox(Color.red, count=2))

        t.push(ColorBox(Color.red))
        self.assertEqual(t.peek(), ColorBox(Color.red, count=3))

        with self.assertRaises(FullException):
            t.push(ColorBox(Color.red))

    def test_is_full(self):
        t = Tube()
        self.assertFalse(t.is_full())
        for c in [Color.red, Color.blue, Color.green]:
            t.push(c)
            self.assertFalse(t.is_full())

        t.push(Color.orange)
        self.assertTrue(t.is_full())

        with self.assertRaises(FullException):
            t.push(Color.blue)

    def test_solved(self):
        t = Tube()
        self.assertTrue(t.solved())
        for c in [Color.red, Color.blue, Color.green]:
            t.push(c)
            self.assertFalse(t.solved())

        t.push(Color.orange)
        self.assertFalse(t.solved())

        t = Tube([Color.red, Color.red, Color.red])
        self.assertFalse(t.solved())

        t.push(Color.blue)
        self.assertFalse(t.solved())
        t.pop()

        t.push(Color.red)
        self.assertTrue(t.solved())

    def test_fits_and_size(self):
        t = Tube()
        self.assertTrue(t.fits(Color.red))

        t = Tube.fill_with(Color.blue)
        self.assertFalse(t.fits(Color.blue))
        self.assertEqual(t.size(), 4)

        # pop removes all 4 boxes of the blue color
        t.pop()
        self.assertEqual(t.size(), 0)
        self.assertTrue(t.fits(Color.red))

        t.push(Color.red)
        self.assertFalse(t.fits(Color.blue))
        self.assertEqual(t.size(), 1)

        t.push(Color.red)
        self.assertEqual(t.size(), 2)
        t.push(Color.red)
        self.assertEqual(t.size(), 3)
        t.push(Color.red)
        self.assertEqual(t.size(), 4)

        with self.assertRaises(FullException):
            t.push(Color.red)

        self.assertEqual(t.size(), 4)

    def test_equal(self):
        t1 = Tube(tid=1)
        t2 = Tube(tid=1)
        self.assertEqual(t2, t1)

        t1.push(Color.red)
        self.assertNotEqual(t1, t2)

        t1 = Tube(tid=1)
        t2 = Tube(tid=2)
        self.assertNotEqual(t1, t2)

        t1 = Tube([Color.red])
        t2 = Tube([Color.blue])
        self.assertNotEqual(t1, t2)

        t1 = Tube.fill_with(Color.orange)
        t2 = Tube.fill_with(Color.orange)
        t1.tid = 100
        t2.tid = 100
        self.assertEqual(t1, t2)

        t1.pop()
        self.assertNotEqual(t1, t2)

        t2.pop()
        self.assertEqual(t1, t2)


if __name__ == '__main__':
    unittest.main()
