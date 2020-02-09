NAME_INDEX = {'name': 0}


class Card(object):

    def __init__(self, t1, t2, t3, t4):
        self._original_pos = [t1, t2, t3, t4]

        self._curr_pos = [t1, t2, t3, t4]
        self.name = NAME_INDEX['name']
        NAME_INDEX['name'] += 1

    def rotate(self, numtimes):
        self._curr_pos = self._original_pos[numtimes:] + self._original_pos[:numtimes]

    def reset(self):
        self._curr_pos = self._original_pos

    @property
    def top(self):
        return self._curr_pos[0]

    @property
    def right(self):
        return self._curr_pos[1]

    @property
    def bottom(self):
        return self._curr_pos[2]

    @property
    def left(self):
        return self._curr_pos[3]


rb = 'rb'
rh = 'rh'
yb = 'yb'
yh = 'yh'
bb = 'bb'
bh = 'bh'
gb = 'gb'
gh = 'gh'


MATCHES = {
    rh: rb,
    rb: rh,
    gh: gb,
    gb: gh,
    bh: bb,
    bb: bh,
    yh: yb,
    yb: yh,
}

CARDS = [
    Card(rb, bb, rh, gh),
    Card(rb, bb, yh, gh),
    Card(rb, gb, yh, bh),
    Card(yb, bb, gh, rh),
    Card(yb, gb, rh, bh),
    Card(yb, gb, rh, bh),
    Card(rb, yb, gh, bh),
    Card(yb, rb, bh, gh),
    Card(yb, rb, yh, bh),
]


BOARD = [
    [None, None, None],
    [None, None, None],
    [None, None, None],
]


def matches_up(row, col):
    if row == 0:
        return True

    above = BOARD[row - 1][col]
    card = BOARD[row][col]
    return above.bottom == MATCHES[card.top]


def matches_down(row, col):
    if row == len(BOARD) - 1:
        return True

    below = BOARD[row + 1][col]
    card = BOARD[row][col]

    if not below:
        return True

    return below.top == MATCHES[card.bottom]


def matches_left(row, col):
    if col == 0:
        return True

    left = BOARD[row][col - 1]
    card = BOARD[row][col]

    return card.left == MATCHES[left.right]


def matches_right(row, col):
    if col == len(BOARD[0]) - 1:
        return True

    card = BOARD[row][col]
    right = BOARD[row][col + 1]
    if not right:
        return True
    return card.right == MATCHES[right.left]


def fits(row, col):
    if not BOARD[row][col]:
        return False
    mup = matches_up(row, col)
    mdo = matches_down(row, col)
    mri = matches_right(row, col)
    mle = matches_left(row, col)
    return mup and mdo and mri and mle


def check_board():
    for i in range(len(BOARD)):
        for j in range(len(BOARD[0])):
            if not fits(i, j):
                return False

    print_board()
    return True


def print_board():
    print('Solution:')
    for row in BOARD:
        row_top_str = ''
        row_mid_str = ''
        row_bot_str = ''
        for val in row:
            row_top_str += '  %s  ' % val.top
            row_mid_str += '%s  %s' % (val.left, val.right)
            row_bot_str += '  %s  ' % val.bottom
        print(row_top_str)
        print(row_mid_str)
        print(row_bot_str)
    print('======================\n')


NOT_PRINTED = {'val': 3}


def solve(cards, row, col):

    if row == len(BOARD) and col == len(BOARD[0]):
        assert len(cards) == 0

    if not cards:
        if check_board():
            return True

    if row >= len(BOARD):
        return False

    for idx in range(len(cards)):
        card = cards[idx]

        remain = cards[:idx] + cards[idx + 1:]
        BOARD[row][col] = card

        next_row = row
        next_col = col + 1
        if next_col == len(BOARD[0]):
            next_row += 1
            next_col = 0

        for i in range(4):
            card.rotate(i)

            if not fits(row, col):
                continue

            solve(remain, next_row, next_col)

    BOARD[row][col] = None

    return False


solve(CARDS, 0, 0)
