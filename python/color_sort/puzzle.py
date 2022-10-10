import os
from color import Color, ColorBox
from collections import defaultdict
from tube import Tube


purple = Color.purple
blue   = Color.blue
teal   = Color.teal
pink   = Color.pink
grey   = Color.grey
orange = Color.orange
lblue  = Color.light_blue
red    = Color.red
lg     = Color.light_green
green  = Color.green
yellow = Color.yellow
fusia  = Color.fusia


class Puzzle:

    def __init__(self, tubes=[], ignore_color_check=False):
        empty = []
        self.tubes = []
        c_count = defaultdict(int)
        for t in tubes:
            if t.is_empty():
                empty.append(t)
            else:
                self.tubes.append(t)
                for c in t.colors:
                    c_count[c.color] += c.count

        for c, val in c_count.items():
            if (val % 4) != 0:
                if not ignore_color_check:
                    raise Exception("missing {}, got {}".format(c, val))

        for t in empty:
            self.tubes.append(t)

    def is_empty(self):
        return len(self.tubes) == 0

    def solved(self):
        return all([t.solved() for t in self.tubes])

    def copy(self):
        return Puzzle([t.copy() for t in self.tubes])

    def pop(self):
        if self.is_empty():
            return None

        return self.tubes.pop(0)

    def push(self, tube):
        self.tubes.insert(0, tube)

    def push_back(self, tube):
        self.tubes.append(tube)

    def dump(self):
        lines = []
        for t in sorted(self.tubes, key=lambda x: x.tid):
            vals = t.dump().split('\n')
            vals.append(' {0:02d} '.format(t.tid))
            lines.append(vals)

        for x in range(len(lines[0])):
            for line in lines:
                log_nn(line[x])
            log()


def log(msg=''):
    if 'DEBUG_SOLVE' in os.environ:
        print(msg)


def log_nn(msg):
    if 'DEBUG_SOLVE' in os.environ:
        print(msg, end='')


def solve(puzzle, count, path):
    if count < 0:
        raise Exception

    if puzzle.solved():
        log('solved on %d' % count)
        return True, puzzle, path

    if puzzle.is_empty():
        return False, puzzle, path

    log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    puzzle.dump()

    p = puzzle.copy()

    for curr_tube in p.tubes:
        if curr_tube.is_empty():
            continue

        curr_color = curr_tube.pop()
        # For every other tube in the puzzle
        for candidate in p.tubes:
            # skip the current tube
            if candidate.tid == curr_tube.tid:
                continue
           
            # No point in moving into an empty tube if it will leave the current tube empty
            if candidate.is_empty() and curr_tube.is_empty():
                continue

            # Check if the top color from the current tube fits in the candidate tube
            if candidate.fits(curr_color):
                # Keep track of the candidate colors so we can restore them if the recursion doesn't succeed
                candidate_colors = candidate.copy_colors()
                # It fits, so pour it into the candidate tube
                candidate.push(curr_color)
                
                path.append((curr_tube.tid, candidate.tid))

                # And recurse to solve
                solved, the_puzzle, the_path = solve(p, count - 1, path)
                if solved:
                    return solved, the_puzzle, the_path
                
                # We couldn't find a solution, reset the candidate back to how it was before
                candidate.colors = candidate_colors
                path.pop()

        # We couldn't find a spot for this color box, return it to the current tube
        curr_tube.push(curr_color)

    return False, p, path


if __name__ == '__main__':
    tubes = [
        Tube([teal, blue, blue, purple], tid=1),
        Tube([blue, purple, grey, fusia], tid=2),
        Tube([grey, purple, pink, pink], tid=3),
        Tube([green, orange, pink, lblue], tid=4),
        Tube([lblue, fusia, green, yellow], tid=5),
        Tube([lg, lg, lblue, yellow], tid=6),
        Tube([purple, blue, yellow, green], tid=7),
        Tube([red, orange, teal, yellow], tid=8),
        Tube([lg, grey, orange, teal], tid=9),
        Tube([pink, fusia, fusia, teal], tid=10),
        Tube([red, red, lg, lblue], tid=11),
        Tube([grey, orange, red, green], tid=12),
        Tube(tid=13),
        Tube(tid=14),
    ]
    p = Puzzle(tubes)

    solved, the_puzzle, the_path = solve(p, 50, [])
    if solved:
        print('====================================================')
        the_puzzle.dump()
        for p in the_path:
            print('{:0>2} -> {:0>2}'.format(p[0], p[1]))
