from docInheritDecorator import DocInherit

# Black > White because these are also used as rewards and for scoring.
BLACK = 1
WHITE = -1
EMPTY = 1e-3

LABEL_WIN = BLACK
LABEL_LOSS = WHITE
LABEL_DRAW = EMPTY

BOARD_SIZE = 3
WIN_LINE_LENGTH = 3

EVALUATION_GAMES = 40


def get_color_from_player_number(code):
    if code == BLACK:
        return "Black"
    if code == WHITE:
        return "White"
    return "Empty"
