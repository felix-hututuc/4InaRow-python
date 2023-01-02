import math
import os
import subprocess
import sys
import time
import traceback

try:
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])

    import numpy as np

try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame', '--pre'])

    import pygame

__EMPTY__ = 0
__PLAYER_ONE__ = 1
__PLAYER_TWO__ = 2
__COMPUTER__ = 3
ROW_COUNT = 4
COL_COUNT = 5
OPPONENT = 2
TURN = 1

CELL_SIZE = 75
PIECE_RADIUS = int(CELL_SIZE / 2 - 4)
SCREEN_WIDTH = COL_COUNT * CELL_SIZE
SCREEN_HEIGHT = (ROW_COUNT + 1) * CELL_SIZE
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

COLORS = {__EMPTY__: pygame.color.THECOLORS['white'],
          __PLAYER_ONE__: pygame.color.THECOLORS['red'],
          __PLAYER_TWO__: pygame.color.THECOLORS['yellow'],
          __COMPUTER__: pygame.color.THECOLORS['green']}


def log(msg, errorMsg = False, endLine=True):
    if not errorMsg:
        print(f'[4InaRow]: {msg}', end=None if endLine else '', flush=True)
    else:
        print("""[4InaRow]: ERROR Log:
        {errLog}""".format(errLog = '\n\t\t'.join(traceback.format_exc().split('\n'))),
                           end=None if endLine else '',
                           flush=True)


def init():
    global ROW_COUNT
    global COL_COUNT
    global OPPONENT
    global TURN
    global SCREEN_HEIGHT
    global SCREEN_WIDTH
    global SCREEN

    if len(sys.argv) < 5:
        log("Wrong number of arguments!")
        log("Template: python 4_in_a_row.py <OPPONENT_type> <no_rows> <no_cols> <first_player>")
        exit(-1)

    if sys.argv[1].lower() == 'player':
        OPPONENT = __PLAYER_TWO__
    elif sys.argv[1].lower() == 'computer':
        OPPONENT = __COMPUTER__
    else:
        log("Wrong OPPONENT type. Options: player / computer")
        exit(-1)

    try:
        ROW_COUNT = int(sys.argv[2])
        COL_COUNT = int(sys.argv[3])
        SCREEN_WIDTH = COL_COUNT * CELL_SIZE
        SCREEN_HEIGHT = (ROW_COUNT + 1) * CELL_SIZE
        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        if ROW_COUNT < 4 or ROW_COUNT > 9 or COL_COUNT < 4 or COL_COUNT > 9:
            log("Rows and collumns numbers must be between 6 and 9")
            exit(-1)
    except TypeError:
        log("Rows and collumns numbers must be integers")
        log('', errorMsg=True)
        exit(-1)

    if sys.argv[4].lower() == "player1":
        TURN = __PLAYER_ONE__
    elif sys.argv[4].lower() == "player2":
        TURN = __PLAYER_TWO__
    elif sys.argv[4].lower() == "computer":
        TURN = __COMPUTER__
    else:
        log("Wrong argument for first player! Options: player1 / player2 / computer")
        exit(-1)

    if OPPONENT == __PLAYER_TWO__ and TURN == __COMPUTER__ \
       or OPPONENT == __COMPUTER__ and TURN == __PLAYER_TWO__:
       log("Mismatch of OPPONENT and first player!")
       exit(-1)


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


def draw_board(board):
    for it_col in range(COL_COUNT):
        for it_row in range(ROW_COUNT):
            pygame.draw.rect(SCREEN,
                             pygame.color.THECOLORS['blue'],
                             (it_col * CELL_SIZE,
                              it_row * CELL_SIZE + CELL_SIZE,
                              CELL_SIZE,
                              CELL_SIZE))

            pygame.draw.circle(SCREEN,
                               COLORS[board[it_row][it_col]],
                               (int(it_col * CELL_SIZE + CELL_SIZE / 2),
                                int(it_row * CELL_SIZE + CELL_SIZE + CELL_SIZE / 2)),
                               PIECE_RADIUS)

    pygame.display.update()


def display_diff_choice():
    font = pygame.font.SysFont("verdana", int(SCREEN_WIDTH / 15), True)
    pygame.time.wait(300)
    pygame.draw.rect(SCREEN,
                     pygame.color.THECOLORS['cyan'],
                     (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    label = font.render("Choose a difficulty:", True, pygame.color.THECOLORS['black'])
    SCREEN.blit(label, (SCREEN_WIDTH / 7, SCREEN_HEIGHT / 8))

    pygame.draw.ellipse(SCREEN,
                        pygame.color.THECOLORS['green'],
                        (SCREEN_WIDTH / 7, 3 * SCREEN_HEIGHT / 8))

    pygame.display.update()
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()
        # pygame.time.wait(10)


def display_end_screen(winner, is_draw: bool = False):
    if winner == __PLAYER_ONE__:
        winner_str = 'Player one'
    elif winner == __PLAYER_TWO__:
        winner_str = 'Player two'
    else:
        winner_str = 'Computer'

    font = pygame.font.SysFont("verdana", int(SCREEN_WIDTH / 15), True)
    pygame.time.wait(300)
    pygame.draw.rect(SCREEN,
                     pygame.color.THECOLORS['black'],
                     (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    if is_draw:
        label = font.render(f"Draw!", True, COLORS[__EMPTY__])
    else:
        label = font.render(f"{winner_str} won!", True, COLORS[winner])
    SCREEN.blit(label, (SCREEN_WIDTH / 5, 2.7 * SCREEN_HEIGHT / 7))
    pygame.display.update()

    start_time = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()
        if time.time() - start_time >= 5:
            sys.exit()


def game_loop(board):
    global TURN

    display_diff_choice()
    draw_board(board)

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                x_pos = event.pos[0]

                pygame.draw.rect(SCREEN,
                                 pygame.color.THECOLORS['black'],
                                 (0, 0, SCREEN_WIDTH, CELL_SIZE))

                x_pos = PIECE_RADIUS if x_pos < PIECE_RADIUS else \
                        SCREEN_WIDTH - PIECE_RADIUS if x_pos > SCREEN_WIDTH - PIECE_RADIUS else \
                        x_pos

                pygame.draw.circle(SCREEN,
                                   COLORS[TURN],
                                   (x_pos, int(CELL_SIZE / 2)),
                                   PIECE_RADIUS)

                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]

                column = int(math.floor(x_pos / CELL_SIZE))

                pygame.draw.rect(SCREEN,
                                 pygame.color.THECOLORS['black'],
                                 (0, 0, SCREEN_WIDTH, CELL_SIZE))

                x_pos = PIECE_RADIUS if x_pos < PIECE_RADIUS else \
                        SCREEN_WIDTH - PIECE_RADIUS if x_pos > SCREEN_WIDTH - PIECE_RADIUS else \
                        x_pos

                pygame.draw.circle(SCREEN,
                                   COLORS[OPPONENT],
                                   (x_pos, int(CELL_SIZE / 2)),
                                   PIECE_RADIUS)

                pygame.display.update()

                if not place_piece_onefunc(board, column, TURN):
                    continue
                else:
                    print(board)
                    draw_board(board)

                if is_win(board, TURN) or is_draw(board):
                    print(board)
                    draw_board(board)
                    display_end_screen(TURN, is_draw(board))

                TURN = __PLAYER_ONE__ if TURN == OPPONENT else OPPONENT


if __name__ == '__main__':
    init()
    pygame.init()
    board = init_board(ROW_COUNT, COL_COUNT)
    game_loop(board)
