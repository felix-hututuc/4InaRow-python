import os
import sys
import subprocess
import traceback

try:
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])

    import numpy as np


# try:
#     import pygame
# except ImportError:
#     subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame'])

#     import pygame


LINE_COUNT = 4
COLL_COUNT = 4


def log(msg, errorMsg = False, endLine=True):
    if not errorMsg:
        print(f'[4InaRow]: {msg}', end=None if endLine else '', flush=True)
    else:
        print("""[4InaRow]: ERROR Log:
        {errLog}""".format(errLog = '\n\t\t'.join(traceback.format_exc().split('\n'))),
                           end=None if endLine else '',
                           flush=True)


def init_board(rows, colls):
    return np.zeros((rows, colls))


def find_first_empty(board, coll):
    first_empty = LINE_COUNT - 1
    for row in range(LINE_COUNT - 1):
        if board[row + 1][coll] != 0:
            first_empty = row
            break

    return first_empty


def place_piece(board, row, coll, player):
    board[row][coll] = player


def is_valid_move(board, row, coll):
    if coll >= COLL_COUNT:
        log("Chosen collumn out of range")
        return False
    
    if row < 0 or row >= LINE_COUNT:
        log("Row out of range")
        return False

    if board[row + 1][coll] != 0:
        log("Trying to levitate a piece")
        return False

    return True


def place_piece_onefunc(board, coll, player):
    if coll >= COLL_COUNT:
        log("Chosen collumn out of range")
        return False

    first_empty = LINE_COUNT - 1
    for row in range(LINE_COUNT - 1):
        if board[row + 1][coll] != 0:
            first_empty = row
            break

    if first_empty < 0 or first_empty >= LINE_COUNT:
        log("Row out of range")
        return False

    board[first_empty][coll] = player
    return True


def is_draw(board) -> bool:
    if any([True if 0 in board[i] else False for i in range(LINE_COUNT)]):
        return False
    return True


def is_win_horizontally(board, player):
    for row in board:
        for coll_iter in range(COLL_COUNT - 3):
            if all([piece == player
                    for piece in [row[coll_iter + seq_iter] for seq_iter in range(4)]]):
                return True

    return False


def is_win(board, player) -> bool:

    # horizontally and vertically
    if is_win_horizontally(board, player) or is_win_horizontally(np.transpose(board), player):
        return True
    return False

    # diagonalls


if __name__ == '__main__':
    board = init_board(LINE_COUNT, COLL_COUNT)
    # board = np.flip(board)
    print(board)
    place_piece_onefunc(board, 0, 1)
    place_piece_onefunc(board, 0, 1)
    place_piece_onefunc(board, 1, 1)
    place_piece_onefunc(board, 1, 1)
    place_piece_onefunc(board, 0, 1)
    place_piece_onefunc(board, 0, 1)
    place_piece_onefunc(board, 3, 1)
    place_piece_onefunc(board, 2, 2)

    # board[1][1] = 1
    # board[0][1] = 1


    print(board)
    print(is_draw(board))
    print(board)
    print(is_win(board, 1))
