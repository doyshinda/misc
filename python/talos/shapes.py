from copy import copy
from collections import defaultdict


LETTER_IDS = 'ABCDEFGHIJKLNOPSTUVWXYZQMRabcdefghijklmnopqrstuvwxyz'
LETTER_ITER = iter(LETTER_IDS)


def make_unique_shape(shape):
    name = next(LETTER_ITER)

    new_shape = []
    for row in shape:
        new_row = []
        for col in row:
            if col == '*':
                new_row.append('*')
            else:
                new_row.append(name)

        new_shape.append(new_row)

    return name, new_shape


class Shape(object):
    def __init__(self, shape):
        name, shape = make_unique_shape(shape)
        self.name = name
        self._shape = shape
        self._rotate90 = list(zip(*self._shape[::-1]))
        self._rotate180 = list(zip(*self._rotate90[::-1]))
        self._rotate270 = list(zip(*self._rotate180[::-1]))

    def rotations(self):
        raise NotImplementedError()

    @property
    def shape(self):
        return self._shape

    def __eq__(self, other):
        return other and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.name, self.name))


############
# 'Z' Shapes
############
class Zed(Shape):

    def rotations(self):
        return [self._shape, self._rotate90]


class LeftZed(Zed):

    def __init__(self):
        super(LeftZed, self).__init__(
            [
                ['z', 'z', '*'],
                ['*', 'z', 'z'],
            ]
        )


class RightZed(Zed):

    def __init__(self):
        super(RightZed, self).__init__(
            [
                ['*', 'z', 'z'],
                ['z', 'z', '*'],
            ]
        )


############
# 'L' Shapes
############
class Ell(Shape):

    def rotations(self):
        return [self._shape, self._rotate90, self._rotate180, self._rotate270]


class LeftEll(Ell):
    def __init__(self):
        super(LeftEll, self).__init__(
            [
                ['*', 'l'],
                ['*', 'l'],
                ['l', 'l']
            ]
        )


class RightEll(Ell):
    def __init__(self):
        super(RightEll, self).__init__(
            [
                ['l', '*'],
                ['l', '*'],
                ['l', 'l']
            ]
        )


############
# 'T' Shapes
############
class Tee(Shape):

    def __init__(self):
        shape = [
            ['t', 't', 't'],
            ['*', 't', '*']
        ]
        super(Tee, self).__init__(shape)

    def rotations(self):
        return [self._shape, self._rotate90, self._rotate180, self._rotate270]


############
# Square Shapes
############
class Square(Shape):

    def __init__(self):
        shape = [
            ['s', 's'],
            ['s', 's']
        ]
        super(Square, self).__init__(shape)

    def rotations(self):
        return [self._shape]


############
# Rectangle Shapes
############
class Rectangle(Shape):

    def __init__(self):
        shape = [
            ['r', 'r', 'r', 'r'],
        ]
        super(Rectangle, self).__init__(shape)

    def rotations(self):
        return [self._shape, self._rotate90]


def print_board(board):
    print('-' * len(board[0]))
    for row in board:
        print(''.join(row))


def print_shape(board):
    for row in board:
        print(''.join(row))


def print_shape_on_board_at_pos(board, shape, startRow=0, startCol=0):
    num_rows = len(board)
    num_cols = len(board[0])

    print('-' * num_cols)
    for row in range(num_rows):
        if row < startRow:
            row_str = '*' * num_cols
        else:
            row_str = ''
            for col in range(num_cols):
                if col < startCol:
                    row_str += '*'
                else:
                    try:
                        row_str += shape[row - startRow][col - startCol]
                    except IndexError:
                        row_str += '*'

        print(row_str)


def mycopy(board):
    return [copy(r) for r in board]
