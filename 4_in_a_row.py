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


ROW_COUNT = 4
COL_COUNT = 5


def log(msg, errorMsg = False, endLine=True):
    if not errorMsg:
        print(f'[4InaRow]: {msg}', end=None if endLine else '', flush=True)
    else:
        print("""[4InaRow]: ERROR Log:
        {errLog}""".format(errLog = '\n\t\t'.join(traceback.format_exc().split('\n'))),
                           end=None if endLine else '',
                           flush=True)


def init_board(rows, cols):
    return np.zeros((rows, cols))


def find_first_empty(board, col):
    first_empty = ROW_COUNT - 1
    for row in range(ROW_COUNT - 1):
        if board[row + 1][col] != 0:
            first_empty = row
            break

    return first_empty


def place_piece(board, row, col, player):
    board[row][col] = player


def is_valid_move(board, row, col):
    if col >= COL_COUNT:
        log("Chosen column out of range")
        return False

    if row < 0 or row >= ROW_COUNT:
        log("Row out of range")
        return False

    if board[row + 1][col] != 0:
        log("Trying to levitate a piece")
        return False

    return True


def place_piece_onefunc(board, col, player):
    if col >= COL_COUNT:
        log("Chosen column out of range")
        return False

    first_empty = ROW_COUNT - 1
    for row in range(ROW_COUNT - 1):
        if board[row + 1][col] != 0:
            first_empty = row
            break

    if first_empty < 0 or first_empty >= ROW_COUNT:
        log("Row out of range")
        return False

    if board[first_empty][col] != 0:
        log("Column is already full!")
        return False

    board[first_empty][col] = player
    return True


def is_draw(board) -> bool:
    if any([True if 0 in board[i] else False for i in range(ROW_COUNT)]):
        return False
    return True


def is_win_horizontally(board, player):
    for row in board:
        for col_iter in range(len(row) - 3):
            if all([piece == player
                    for piece in [row[col_iter + seq_iter] for seq_iter in range(4)]]):
                return True

    return False


def is_win_diag(board, player):
    for row_iter in range(3, len(board)):
        for col_iter in range(len(board[0]) - 3):
            if all([piece == player
                    for piece in [board[row_iter - seq_iter][col_iter + seq_iter] for seq_iter in range(4)]]):
                return True

    return False


def is_win(board, player) -> bool:
    # horizontally and vertically
    # diagonals => range(3, ROW_COUNT) ---- range(COL_COUNT - 3)
    if is_win_horizontally(board, player) \
       or is_win_horizontally(np.transpose(board), player) \
       or is_win_diag(board, player) \
       or is_win_diag(np.flipud(board), player):
        return True

    return False


def game_loop(board, player1, player2):
    turn = player1

    while True:
        print(board)
        log(f"Player {turn}'s turn!")
        chosen_col = int(input("Choose a column: "))
        if not place_piece_onefunc(board, chosen_col, turn):
            continue
        if is_win(board, turn):
            print(board)
            log(f"Player {turn} won!")
            break
        if is_draw(board):
            print(board)
            log("Draw!")
            break
        turn = player1 if turn == player2 else player2


if __name__ == '__main__':
    board = init_board(ROW_COUNT, COL_COUNT)
    game_loop(board, 1, 2)
    # board = np.flip(board)
    # print(board)
    # place_piece_onefunc(board, 0, 2)
    # place_piece_onefunc(board, 0, 2)
    # place_piece_onefunc(board, 1, 1)
    # place_piece_onefunc(board, 1, 1)
    # place_piece_onefunc(board, 0, 1)
    # place_piece_onefunc(board, 4, 1)
    # place_piece_onefunc(board, 3, 1)
    # place_piece_onefunc(board, 2, 2)
    # place_piece_onefunc(board, 2, 1)
    # place_piece_onefunc(board, 3, 2)
    # place_piece_onefunc(board, 3, 1)
    # place_piece_onefunc(board, 4, 1)
    # place_piece_onefunc(board, 4, 2)
    # place_piece_onefunc(board, 1, 1)
    # place_piece_onefunc(board, 0, 1)


    # print(board)
    # print(is_draw(board))
    # print(board)
    # print(is_win(board, 1))
    # print(np.flipud(board))
