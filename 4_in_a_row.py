import math
import random
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
ROW_COUNT = 6
COL_COUNT = 7
OPPONENT = 2
TURN = 1
BIG_NUMBER = 999999

CELL_SIZE = 80
PIECE_RADIUS = int(CELL_SIZE / 2 - 4)
SCREEN_WIDTH = COL_COUNT * CELL_SIZE
SCREEN_HEIGHT = (ROW_COUNT + 1) * CELL_SIZE
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

COLORS = {__EMPTY__: pygame.color.THECOLORS['white'],
          __PLAYER_ONE__: pygame.color.THECOLORS['red'],
          __PLAYER_TWO__: pygame.color.THECOLORS['yellow'],
          __COMPUTER__: pygame.color.THECOLORS['green']}

BEST_COL = random.randrange(COL_COUNT)


def log(msg: any, error_msg: bool = False, end_line: bool = True) -> None:
    """
    Utility function for improved logging.\n
    :param msg: any arbitrary message to be logged
    :param error_msg: whether the message comes from an error
    :param end_line: false if no new line should be added at end of log
    :return: none
    """
    if not error_msg:
        print(f'[4InaRow]: {msg}', end=None if end_line else '', flush=True)
    else:
        print("""[4InaRow]: ERROR Log:
        {errLog}""".format(errLog='\n\t\t'.join(traceback.format_exc().split('\n'))),
              end=None if end_line else '',
              flush=True)


def init() -> None:
    """
    Initialization function for parsing and validating command line arguments.\n
    :return: none
    """
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
        pygame.display.set_caption("Connect Four")
        if ROW_COUNT < 4 or ROW_COUNT > 9 or COL_COUNT < 4 or COL_COUNT > 9:
            log("Rows and columns numbers must be between 6 and 9")
            exit(-1)
    except TypeError:
        log("Rows and columns numbers must be integers")
        log('', error_msg=True)
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


def init_board(rows: int, cols: int) -> np.ndarray:
    """
    Initialize the game board as a 0-filled matrix\n
    :param rows: number of rows
    :param cols:  number of columns
    :return: a 0-filled numpy 'rows' x 'columns' numpy matrix
    """
    return np.zeros((rows, cols))


def find_first_empty(board: np.ndarray, col: int) -> int:
    """
    Finds the first empty row in which a piece should fall\n
    :param board: the game board
    :param col: the column in which the piece falls
    :return: the row in which the piece will stop
    """
    first_empty = ROW_COUNT - 1
    for row in range(ROW_COUNT - 1):
        if board[row + 1][col] != 0:
            first_empty = row
            break

    return first_empty


def place_piece(board: np.ndarray, row: int, col: int, player: int) -> None:
    """
    Places a piece in a specific slot\n
    :param board: the game board
    :param row: chosen row
    :param col: chosen column
    :param player: current player
    :return: None
    """
    board[row][col] = player


def is_full_col(board: np.ndarray, col: int) -> bool:
    """
    Checks whether a column is full\n
    :param board: the game board
    :param col: the column to be checked
    :return: True if the column is full else False
    """
    return board[0][col] != __EMPTY__


def is_valid_move(board: np.ndarray, row: int, col: int) -> bool:
    """
    Checks if a move is valid\n
    :param board: the game board
    :param row: the chosen row
    :param col: the chosen column
    :return: True if the move can be made, False otherwise
    """
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


def place_piece_onefunc(board: np.ndarray, col: int, player: int) -> bool:
    """
    Utility function to place a piece in a specific column in a single line.
    It includes move validation, finding the first empty row and placing the piece.\n
    :param board: the game board
    :param col: chosen column
    :param player: current player
    :return: True if the piece was placed, False if not
    """
    if col >= COL_COUNT:
        log(f"Chosen column out of range: {col}")
        return False

    first_empty = ROW_COUNT - 1
    for row in range(ROW_COUNT - 1):
        if board[row + 1][col] != 0:
            first_empty = row
            break

    if first_empty < 0 or first_empty >= ROW_COUNT:
        log(f"Row out of range: {first_empty}")
        return False

    if board[first_empty][col] != 0:
        log(f"Column is already full! ({col})")
        return False

    board[first_empty][col] = player
    return True


def is_draw(board: np.ndarray) -> bool:
    """
    Checks if the game board is in a draw state i.e. the board is filled\n
    :param board: the game board
    :return: True if the game is a draw
    """
    if any([True if 0 in board[i] else False for i in range(ROW_COUNT)]):
        return False
    return True


def is_win_horizontally(board: np.ndarray, player: int) -> bool:
    """
    Checks if there are any winning 4-piece horizontal intervals on the board for the chosen player\n
    :param board: the game board
    :param player: the chosen player
    :return: True if the chosen player has won
    """
    for row in board:
        for col_iter in range(len(row) - 3):
            if all([piece == player
                    for piece in [row[col_iter + seq_iter] for seq_iter in range(4)]]):
                return True

    return False


def is_win_diag(board: np.ndarray, player: int) -> bool:
    """
    Checks if there are any winning 4-piece upper-diagonal intervals
    on the board for the chosen player.\n
    :param board: the game board
    :param player: the chosen player
    :return: True if the chosen player has won, else False
    """
    for row_iter in range(3, len(board)):
        for col_iter in range(len(board[0]) - 3):
            if all([piece == player
                    for piece in [board[row_iter - seq_iter][col_iter + seq_iter] for seq_iter in range(4)]]):
                return True

    return False


def is_win(board: np.ndarray, player: int) -> bool:
    """
    Checks if the player has won.\n

    The function which checks for horizontal wins
    is also used for vertical wins by transposing the board.\n

    Similarly, the function which checks for upper-diagonal wins
    is also used for lower-diagonal wins by flipping the board upside down.\n
    :param board: the game board
    :param player: the chosen player
    :return: True if the player has won, else False
    """
    if is_win_horizontally(board, player) \
            or is_win_horizontally(np.transpose(board), player) \
            or is_win_diag(board, player) \
            or is_win_diag(np.flipud(board), player):
        return True

    return False


def draw_board(board: np.ndarray) -> None:
    """
    Draws the game board on the screen.\n
    The function initially fills the board with a blue rectangle,
    then draws each circle and colours it based on the existing piece/empty spot\n
    This function is called after each update of the board.\n
    :param board: the game board
    :return: None
    """
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


def display_diff_choice() -> None:
    """
    Displays the difficulty selection screen.\n
    :return: None
    """
    font = pygame.font.SysFont("verdana", int(SCREEN_WIDTH / 15), True)
    pygame.time.wait(300)
    pygame.draw.rect(SCREEN,
                     pygame.color.THECOLORS['cyan'],
                     (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    label = font.render("Choose a difficulty:", True, pygame.color.THECOLORS['black'])
    SCREEN.blit(label, (SCREEN_WIDTH / 7, SCREEN_HEIGHT / 8))

    pygame.draw.ellipse(SCREEN,
                        pygame.color.THECOLORS['green'],
                        (SCREEN_WIDTH / 7, 2 * SCREEN_HEIGHT / 8, 5 * SCREEN_WIDTH / 7, 1.5 * SCREEN_HEIGHT / 8))

    label = font.render("EASY", True, pygame.color.THECOLORS['black'])
    SCREEN.blit(label, (2.8 * SCREEN_WIDTH / 7, 2.45 * SCREEN_HEIGHT / 8))

    pygame.draw.ellipse(SCREEN,
                        pygame.color.THECOLORS['yellow'],
                        (SCREEN_WIDTH / 7, 4 * SCREEN_HEIGHT / 8, 5 * SCREEN_WIDTH / 7, 1.5 * SCREEN_HEIGHT / 8))

    label = font.render("MEDIUM", True, pygame.color.THECOLORS['black'])
    SCREEN.blit(label, (2.4 * SCREEN_WIDTH / 7, 4.45 * SCREEN_HEIGHT / 8))

    pygame.draw.ellipse(SCREEN,
                        pygame.color.THECOLORS['red'],
                        (SCREEN_WIDTH / 7, 6 * SCREEN_HEIGHT / 8, 5 * SCREEN_WIDTH / 7, 1.5 * SCREEN_HEIGHT / 8))

    label = font.render("HARD", True, pygame.color.THECOLORS['black'])
    SCREEN.blit(label, (2.8 * SCREEN_WIDTH / 7, 6.45 * SCREEN_HEIGHT / 8))

    pygame.display.update()


def get_difficulty() -> int:
    """
    Gets the selected difficulty level based on the mouse click position\n
    :return: the difficulty level (0 - easy, 1 - medium, 2 - hard)
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]
                y_pos = event.pos[1]

                if not (SCREEN_WIDTH / 7 <= x_pos <= 5 * SCREEN_WIDTH / 7):
                    continue

                if 2 * SCREEN_HEIGHT / 8 <= y_pos <= 3.5 * SCREEN_HEIGHT / 8:
                    return 0

                if 4 * SCREEN_HEIGHT / 8 <= y_pos <= 5.5 * SCREEN_HEIGHT / 8:
                    return 1

                if 6 * SCREEN_HEIGHT / 8 <= y_pos <= 7.5 * SCREEN_HEIGHT / 8:
                    return 2


def display_end_screen(winner: int, is_draw: bool = False) -> None:
    """
    Displays the end screen, showing the winner / draw.\n
    Represents the end point of the application.\n
    It automatically closes after 5 seconds or after a mouse click.\n
    :param winner: the winner of the game or None if the game ended in a draw
    :param is_draw: flag for a draw game
    :return: exits the application
    """
    if winner == __PLAYER_ONE__:
        winner_str = 'Player one'
    elif winner == __PLAYER_TWO__:
        winner_str = 'Player two'
    else:
        winner_str = 'Computer'

    # create the end game message and display it
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

    # start a 5 seconds timer to close the app
    # check for any mouse click events to close the app sooner
    start_time = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()
        if time.time() - start_time >= 5:
            sys.exit()


def draw_header(x_pos: int, color: pygame.color.Color) -> None:
    """
    Draws the header of the game app (the black bar where the "floating" piece moves"\n
    Is called at every update of the header i.e. at every mouse movement.\n
    :param x_pos: position of the "floating" piece
    :param color: color of the "floating" piece
    :return: displays the header
    """
    pygame.draw.rect(SCREEN,
                     pygame.color.THECOLORS['black'],
                     (0, 0, SCREEN_WIDTH, CELL_SIZE))

    # prevent the floating piece from going out of screen
    x_pos = PIECE_RADIUS if x_pos < PIECE_RADIUS else \
        SCREEN_WIDTH - PIECE_RADIUS if x_pos > SCREEN_WIDTH - PIECE_RADIUS else \
            x_pos

    pygame.draw.circle(SCREEN,
                       color,
                       (x_pos, int(CELL_SIZE / 2)),
                       PIECE_RADIUS)

    pygame.display.update()


def evaluate_interval(interval: list[int], player: int) -> int:
    """
    Evaluate the score of a position interval of length four for the current player.\n
    :param interval: list of four consecutive positions from the board
    :param player: current player
    :return: total score of the interval
    """
    score = 0

    opponent = __PLAYER_ONE__ if player == __COMPUTER__ else __COMPUTER__

    if interval.count(player) == 4:
        score += BIG_NUMBER
    elif interval.count(player) == 3 and interval.count(__EMPTY__) == 1:
        score += 5
    elif interval.count(player) == 2 and interval.count(__EMPTY__) == 2:
        score += 2

    if interval.count(opponent) == 4:
        score -= BIG_NUMBER
    elif interval.count(opponent) == 3 and interval.count(__EMPTY__) == 1:
        score -= 10
    elif interval.count(opponent) == 2 and interval.count(__EMPTY__) == 2:
        score -= 2

    return score


def score_horizontally(board: np.ndarray, player: int) -> int:
    """
    Evaluates all legal horizontal intervals of four positions on the board
    by calling the `evaluate_interval` function for each one.\n
    Can be used to score vertical intervals by transposing the board first.\n
    :param board: game board
    :param player: current player
    :return: the total score of the current state of the game board from all horizontal intervals
    """
    score = 0
    for row in board:
        for col_index in range(COL_COUNT - 3):
            interval = list(row[col_index: col_index + 4])
            score += evaluate_interval(interval, player)

    return score


def score_diagonally(board: np.ndarray, player: int) -> int:
    """
    Evaluates all legal lower diagonal intervals of four positions on the board
    by calling the `evaluate_interval` function for each one.\n
    Can be used to score upper diagonal intervals by flipping the board upside-down first.\n
    :param board: game board
    :param player: current player
    :return: the total score of the current state of the game board from all lower diagonal intervals
    """
    score = 0
    for row_iter in range(3, ROW_COUNT):
        for col_iter in range(COL_COUNT - 3):
            interval = [board[row_iter - seq_iter][col_iter + seq_iter] for seq_iter in range(4)]
            score += evaluate_interval(interval, player)

    return score


def score_center(board: np.ndarray, player: int) -> int:
    """
    Evaluates the center column based on the number of player pieces on it.\n
    :param board: game board
    :param player: current player
    :return: score of the center column
    """
    center_col = list(np.transpose(board)[COL_COUNT // 2])
    center_count = center_col.count(player)
    score = center_count * 3

    return score


def score_state(board: np.ndarray, player: int) -> int:
    """
    Calculates the entire score of a game board state.\n
    :param board: game board
    :param player: current player
    :return: full score of the board state
    """
    score = 0

    score += score_horizontally(board, player) \
             + score_horizontally(np.transpose(board), player) \
             + score_diagonally(board, player) \
             + score_diagonally(np.flipud(board), player) \
             + score_center(board, player)

    return score


def get_valid_cols(board: np.ndarray) -> list[int]:
    """
    Finds all columns which are not full.\n
    :param board: game board
    :return: list of valid columns
    """
    return [col for col in range(COL_COUNT) if not is_full_col(board, col)]


def is_end_state(board: np.ndarray) -> bool:
    """
    Checks whether the board is in an end state i.e. either player has won or draw\n
    :param board: game board
    :return: true if the board is in an end state, else false
    """
    return is_win(board, __COMPUTER__) or is_win(board, __PLAYER_ONE__) or is_draw(board)


def revert_move(board: np.ndarray, row: int, col: int) -> None:
    """
    Reverts a previously made move i.e. sets the position `(row, col)` as empty.\n
    :param board: game board
    :param row: move row
    :param col: move column
    :return: None
    """
    board[row][col] = __EMPTY__


def minimax_alphabeta(board: np.ndarray, depth: int, alpha: float, beta: float, maximizing_player: bool, player: int):
    """
    Implementation of the minimax algorithm with specified depth and alpha-beta pruning.\n
    The algorithm sets the global variable `BEST_COL` to the best next move found and returns the score of that move.\n
    :param board: game board
    :param depth: maximum depth for the search tree
    :param alpha: minimum score to find
    :param beta: maximum score to find
    :param maximizing_player: True if on a maximizing level in the tree, False on minimizing
    :param player: current player
    :return: the score of the best next move found
    """
    global BEST_COL
    opponent = __PLAYER_ONE__ if player == __COMPUTER__ else __COMPUTER__
    if is_end_state(board):
        if is_draw(board):
            return 0
        if is_win(board, player):
            return BIG_NUMBER
        return -BIG_NUMBER

    if depth == 0:
        return score_state(board, player)

    valid_cols = get_valid_cols(board)
    if maximizing_player:
        score = -math.inf
        for col in valid_cols:
            row = find_first_empty(board, col)
            place_piece(board, row, col, player)
            new_score = minimax_alphabeta(board, depth - 1, alpha, beta, False, player)
            revert_move(board, row, col)

            if new_score > score:
                score = new_score
                alpha = max(alpha, score)

                BEST_COL = col

                if alpha >= beta:
                    break

        return score
    else:
        score = math.inf
        for col in valid_cols:
            row = find_first_empty(board, col)
            place_piece(board, row, col, opponent)
            score = minimax_alphabeta(board, depth - 1, alpha, beta, True, player)
            revert_move(board, row, col)
            # if new_score < score:
            #     score = new_score

            beta = min(beta, score)
            if alpha >= beta:
                break

        return score


def negamax(board: np.ndarray, depth: int, player: int, alpha: float, beta: float, maximizing: int):
    """
    Implementation of the negamax algorithm with specified depth and alpha-beta pruning.\n
    The algorithm sets the global variable `BEST_COL` to the best next move found and returns the score of that move.\n
    :param board: game board
    :param depth: maximum depth for the search tree
    :param player: current player
    :param alpha: minimum score to find
    :param beta: maximum score to find
    :param maximizing: 1 if trying to maximize, -1 for minimizing (negating score)
    :return: the score of the best next move found
    """

    global BEST_COL

    # order in which to check the next possible moves in the AI algorithms
    column_order = [math.floor(COL_COUNT / 2 + (1 - 2 * (i % 2)) * (i + 1) / 2) for i in range(COL_COUNT - 1)]
    opponent = __PLAYER_ONE__ if player == __COMPUTER__ else __COMPUTER__

    if is_draw(board):
        return 0

    if depth == 0:
        return maximizing * score_state(board, player)

    valid_cols = get_valid_cols(board)

    # check if there is any direct next move to win the game
    for col in valid_cols:
        row = find_first_empty(board, col)
        place_piece(board, row, col, player)
        if is_win(board, player):
            revert_move(board, row, col)
            BEST_COL = col
            return maximizing * BIG_NUMBER
        revert_move(board, row, col)

    best_score = -math.inf
    for col in column_order:
        if col not in valid_cols:
            continue
        row = find_first_empty(board, col)
        place_piece(board, row, col, opponent)
        score = -negamax(board, depth - 1, opponent, -beta, -alpha, -maximizing)
        revert_move(board, row, col)

        if score > best_score:
            best_score = score
            BEST_COL = col
        alpha = max(alpha, best_score)
        if alpha >= beta:
            break

    return best_score


def get_computer_move(board: np.ndarray, difficulty: int) -> int:
    """
    Get the next move for the computer player based on the difficulty level.\n
    :param board: game board
    :param difficulty: chosen difficulty level
    :return: column number for the move
    """
    global BEST_COL
    if difficulty == 0:
        pygame.time.wait(500)
        return random.randrange(COL_COUNT)
    if difficulty == 1:
        BEST_COL = random.randrange(COL_COUNT)
        # score = minimax_alphabeta(board, 3, -math.inf, math.inf, True, __COMPUTER__)
        score = negamax(board, 8, __COMPUTER__, -math.inf, math.inf, 1)
        return BEST_COL
    if difficulty == 2:
        BEST_COL = random.randrange(COL_COUNT)
        score = minimax_alphabeta(board, 5, -math.inf, math.inf, True, __COMPUTER__)
        return BEST_COL


def game_loop(board: np.ndarray) -> None:
    """
    Main game loop.\n
    :param board: game board
    :return: None
    """
    global TURN

    # display the difficulty selection screen
    diff = None
    if OPPONENT == __COMPUTER__:
        display_diff_choice()
        diff = get_difficulty()
        log(diff)

    # display the initial state of the board
    pygame.draw.rect(SCREEN,
                     pygame.color.THECOLORS['black'],
                     (0, 0, SCREEN_WIDTH, CELL_SIZE))
    draw_board(board)

    # if the computer makes the first move, do it before the start of the loop
    if OPPONENT == __COMPUTER__ and TURN == __COMPUTER__:
        computed_column = get_computer_move(board, diff)
        while not place_piece_onefunc(board, computed_column, OPPONENT):
            computed_column = get_computer_move(board, diff)
        else:
            pygame.time.wait(500)
            print(board)
            draw_board(board)
            TURN = __PLAYER_ONE__

    while True:  # start the loop

        for event in pygame.event.get():  # event handler

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                x_pos = event.pos[0]
                draw_header(x_pos, COLORS[TURN])

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = event.pos[0]

                column = int(math.floor(x_pos / CELL_SIZE))
                # global BEST_COL
                # BEST_COL = random.randrange(COL_COUNT)
                # negamax(board, 6, __PLAYER_ONE__, -math.inf, math.inf)
                # column = BEST_COL

                draw_header(x_pos, COLORS[OPPONENT])

                if not place_piece_onefunc(board, column, TURN):
                    continue
                else:
                    print(board)
                    draw_board(board)

                if is_win(board, TURN) or is_draw(board):
                    print(board)
                    draw_board(board)
                    display_end_screen(TURN, is_draw(board))

                if OPPONENT == __COMPUTER__:
                    computed_column = get_computer_move(board, diff)
                    while not place_piece_onefunc(board, computed_column, OPPONENT):
                        computed_column = get_computer_move(board, diff)
                    else:
                        print(board)
                        draw_board(board)

                    if is_win(board, OPPONENT) or is_draw(board):
                        print(board)
                        draw_board(board)
                        display_end_screen(OPPONENT, is_draw(board))
                else:
                    TURN = __PLAYER_ONE__ if TURN == OPPONENT else OPPONENT


if __name__ == '__main__':
    init()
    pygame.init()
    game_board = init_board(ROW_COUNT, COL_COUNT)

    game_loop(game_board)
