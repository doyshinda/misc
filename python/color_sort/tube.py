from color import Color, ColorBox
import itertools


MAX_SIZE = 4


gen_tid = itertools.count()

class FullException(Exception):
    pass


class EmptyException(Exception):
    pass


class Tube:
    def __init__(self, colors=[], tid=0):
        self.colors = []
        if tid == 0:
            tid = next(gen_tid)

        self.tid = tid

        if len(colors) > 0:
            last_color = ColorBox(colors[0])
            for c in colors[1:]:
                if last_color.color == c:
                    last_color.count += 1
                else:
                    self.colors.insert(0, last_color)
                    last_color = ColorBox(c)

            self.colors.insert(0, last_color)

    def __eq__(self, other):
        return self.colors == other.colors and self.tid == other.tid

    @staticmethod
    def fill_with(color, num=4, tid=0):
        t = Tube(tid=tid)
        for _ in range(num):
            t.push(color)

        return t

    def is_empty(self):
        return len(self.colors) == 0

    def peek(self):
        if self.is_empty():
            raise EmptyException

        return self.colors[-1]

    def pop(self):
        if self.is_empty():
            return

        return self.colors.pop()

    def copy(self):
        t = Tube(tid=self.tid)
        t.colors = self.copy_colors()
        return t

    def copy_colors(self):
        return [ColorBox(c.color, count=c.count) for c in self.colors]

    def push(self, color):
        if self.is_full():
            raise FullException()

        if isinstance(color, Color):
            color = ColorBox(color)

        if self.is_empty() or self.peek().color != color.color:
            self.colors.append(color)
            return

        if self.peek().count + color.count > MAX_SIZE:
            raise FullException

        self.peek().count += color.count

    def size(self):
        return sum([c.count for c in self.colors])

    def is_full(self):
        return self.size() == MAX_SIZE

    def solved(self):
        if self.is_empty():
            return True

        if not self.is_full():
            return False

        first = self.colors[0]
        return all([c == first for c in self.colors])

    def fits(self, color):
        if self.is_full():
            return False

        if self.is_empty():
            return True

        if isinstance(color, Color):
            color = ColorBox(color)

        p = self.peek()
        if p.color == color.color:
            if self.size() + color.count <= MAX_SIZE:
                return True

        return False

    def dump(self):
        val = ''
        for c in reversed(self.colors):
            val += c.dump()
        
        val += ' -- '
        got = len(val.split('\n'))
        want = 6
        prefix = ''
        for _ in range(want - got):
            prefix += '|  |\n'

        return prefix + val
