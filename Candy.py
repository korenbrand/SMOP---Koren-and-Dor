from random import randint

board_dict = {0: 'blue       ', 1: 's_h_blue   ', 2: 'green      ', 3: 's_h_green  ', 4: 'orange     ', 5: 's_h_orange ',
              6: 'purple     ', 7: 's_h_purple ', 8: 'red        ', 9: 's_h_red    ', 10: 'yellow   ', 11: 's_h_yellow ',
              12: 'chocolate', 13: 's_v_blue   ', 14: 's_v_green  ', 15: 's_v_orange ', 16: 's_v_red    ',
              17: 's_v_yellow ', 18: 's_v_purple ', 19: 'blue_wrapped', 20: 'green_wrapped', 21: 'orange_wrapped',
              22: 'purple_wrapped', 23: 'red_wrapped', 24: 'yellow_wrapped', -1: 'empty    '}

# the score that regular candies exploding from special explosion receive
BASE_SCORE = 20
SPECIAL_SCORE = 60


class Candy:
    STRIPE_SCORE, WRAP_SCORE, COLOR_BOMB_SCORE = 120, 200, 200
    COLOR_DICT = {0: 'Blue', 1: 'Green', 2: 'Orange', 3: 'Purple', 4: 'Red', 5: 'Yellow', 6: 'Chocolate', -1: 'EMPTY'}
    NO_COLOR = 6
    EMPTY = -1

    def __init__(self, color, location):
        self.color = color
        self.location = location
        self.mark = False
        self.empty = False

    def explode(self, board, special_explosion=False):
        board[self.location].color = Candy.EMPTY
        board[self.location].empty = True
        # if this exploded not from a streak but from a special candy, add SPECIAL_SCORE instead of BASE_SCORE
        if special_explosion:
            return SPECIAL_SCORE
        return BASE_SCORE

    def __str__(self):
        if self.mark:
            mark = "X"
        else:
            mark = ""
        description = '{:16}'.format(Candy.COLOR_DICT[self.color] + mark)
        return description


class EmptyCandy(Candy):
    def __init__(self, location):
        Candy.__init__(self, Candy.EMPTY, location)
        self.empty = True


VERT, HORZ = 1, 0
# directions for row (left and right) and column (up and down)
DIRECTIONS = [[(0, 1), (0, -1)],
              [(1, 0), (-1, 0)]]


class Special(Candy):
    def __init__(self, color, location):
        Candy.__init__(self, color, location)


class Striped(Special):
    def __init__(self, color, location, directions):
        Special.__init__(self, color, location)
        self.directions = directions

    def explode(self, board):
        score = Candy.explode(self, board, True)
        # mark the entire direction (row or column)
        for direction in self.directions:
            row = direction[0]
            col = direction[1]
            while 0 <= self.location[0] + row < board.shape[0] and 0 <= self.location[1] + col < board.shape[1] and \
                    board[self.location[0] + row, self.location[1] + col] and not \
                    board[self.location[0] + row, self.location[1] + col].mark:
                score += board[self.location[0] + row, self.location[1] + col].explode(board, True)
                row += direction[0]
                col += direction[1]

        return score


class VerticalStriped(Striped):
    def __init__(self, color, location):
        Striped.__init__(self, color, location, DIRECTIONS[VERT])

    def __str__(self):
        return 'V ' + Candy.__str__(self)


class HorizontalStriped(Striped):
    def __init__(self, color, location):
        Striped.__init__(self, color, location, DIRECTIONS[HORZ])

    def __str__(self):
        return 'H ' + Candy.__str__(self)


REGULAR, BIG = 0, 1


class Wrapped(Special):
    explosion_template = [[(-1, -1), (-1, 0), (-1, 1),
                           (0, -1), (0, 1),
                           (1, -1), (1, 0), (1, 1)],
                          [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
                           (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
                           (0, -2), (0, -1), (0, 1), (0, 2),
                           (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
                           (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]]

    def __init__(self, color, location):
        Special.__init__(self, color, location)
        self.secondExplosion = False

    def explode(self, board, size=0):
        score = BASE_SCORE
        # iterate over candies to mark
        for candy in Wrapped.explosion_template[size]:
            if 0 <= self.location[0] + candy[0] < board.shape[0] and 0 <= self.location[1] + candy[1] < board.shape[1] and \
                    board[self.location[0] + candy[0], self.location[1] + candy[1]] and \
                    not board[self.location[0] + candy[0], self.location[1] + candy[1]].mark:
                score += board[self.location[0] + candy[0], self.location[1] + candy[1]].explode(board, True)

        # if this is the second explosion - mark the wrapped candy for deletion
        if self.secondExplosion:
            Candy.explode(self, board)
        self.secondExplosion = True
        return score

    def __str__(self):
        return 'W ' + Candy.__str__(self)


class Chocolate(Special):
    def __init__(self, location, color=Candy.NO_COLOR):
        Special.__init__(self, color, location)

    def explode(self, board, color=2):
        Candy.explode(self, board)
        score = 0
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row, col].color == color:
                    score += board[row, col].explode(board,True)

        return score
