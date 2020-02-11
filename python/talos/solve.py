from copy import (
    copy,
    deepcopy
)
from shapes import (
    LeftZed,
    RightZed,
    LeftEll,
    RightEll,
    Tee,
    Square,
    Rectangle,
    print_board,
    print_shape,
    mycopy
)


def shape_start_pos(shape):
    count = 0
    for idx, v in enumerate(shape[0]):
        if v == '*':
            count += 1
        if (count - 1) != idx:
            break

    return count


def shape_fits_on_board_at_pos(board, shape, startRow=0, startCol=0):
    shape_width = len(shape[0])
    startCol = startCol - shape_start_pos(shape)

    # Boundary Check
    shape_len = len(shape)
    if shape_len + startRow > len(board):
        return False
    if shape_width + startCol > len(board[0]):
        return False

    for row in range(len(board)):
        if row < startRow:
            continue

        for col in range(len(board[0])):
            if col < startCol:
                continue

            shape_row = row - startRow
            shape_col = col - startCol
            try:
                new_board_value = shape[shape_row][shape_col]
                if new_board_value != '*' and board[row][col] != '*':
                    return False
            except IndexError:
                continue

    return True


def is_solved(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == '*':
                return False

    return True


def add_shape_to_board_at_pos_if_fits(board, shape, startRow=0, startCol=0):
    num_rows = len(board)
    num_cols = len(board[0])

    if not shape_fits_on_board_at_pos(board, shape, startRow=startRow, startCol=startCol):
        return False

    startCol = startCol - shape_start_pos(shape)
    for row in range(num_rows):
        if row < startRow:
            continue

        for col in range(num_cols):
            if col < startCol:
                continue

            try:
                new_board_value = shape[row - startRow][col - startCol]
                if new_board_value == '*':
                    continue
            except IndexError:
                break

            board[row][col] = new_board_value

    return True


def solve(board, shapes, num_rows, num_cols, i):
    if not shapes:
        if is_solved(board):
            return board
        else:
            return False

    for row in range(num_rows):
        for col in range(num_cols):
            if board[row][col] != '*':
                continue

            for shape in sorted(shapes, key=lambda s: s.name):
                for rotation in shape.rotations():
                    originalBoard = mycopy(board)
                    if add_shape_to_board_at_pos_if_fits(board, rotation, startRow=row, startCol=col):
                        shapesCopy = shapes - set([shape])
                        solved = solve(board, shapesCopy, num_rows, num_cols, i + 1)
                        if not solved:
                            board = originalBoard
                        else:
                            return solved
            else:
                return False


def prep():
    # board size
    num_rows = 7
    num_cols = 8

    shape_defs = [
        # shape, quantity
        (RightEll, 1),
        (LeftEll,  1),
        (Square,   4),
        (LeftZed,  1),
        (RightZed, 1),
        (Rectangle,2),
        (Tee,      4),
    ]

    shapes = []
    for s, c in shape_defs:
        for _ in range(c):
            shapes.append(s())

    board = []
    for row in range(num_rows):
        board.append(['*'] * num_cols)
    b = solve(board, set(shapes), num_rows, num_cols, 0)
    if b:
        print_board(b)


if __name__ == '__main__':
    prep()
