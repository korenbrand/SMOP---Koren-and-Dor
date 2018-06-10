from uncertainty_exception import *

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
    COLOR_DICT = {0: 'Blue', 1: 'Green', 2: 'Orange', 3: 'Purple', 4: 'Red', 5: 'Yellow', 6: 'Chocolate', 7: 'Super', \
                  -1: 'UNKNOWN'}
    NO_COLOR = 6
    SUPER_STRIPED_COLOR = 7
    UNKNOWN = -1

    def __init__(self, color, location):
        self.color = color
        self.location = location
        self.mark = False
        self.empty = False

    def explode(self, board, color=None):
        board[self.location].color = Candy.UNKNOWN
        self.mark = False
        if board[self.location].empty:
            return 0
        board[self.location].empty = True
        return BASE_SCORE

    def swipe_explosion(self, board, swipe_loc):
        """
        :param board: current game board
        :param swipe_loc: the location of the other candy being swiped
        :return: score of the special swipe move
        """
        if self.color == Candy.UNKNOWN:
            return 0
        if isinstance(board[swipe_loc], Chocolate):
            return board[swipe_loc].explode(board, self.color)

    def __str__(self):
        if self.mark:
            mark = "X"
        else:
            mark = ""
        description = '{:16}'.format(Candy.COLOR_DICT[self.color] + mark)
        return description


class UnknownCandy(Candy):
    def __init__(self, location):
        Candy.__init__(self, Candy.UNKNOWN, location)


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

    def explode(self, board, color=None):
        score = 0
        Candy.explode(self, board)
        # mark the entire direction (row or column)
        for direction in self.directions:
            row = direction[0]
            col = direction[1]
            while 0 <= self.location[0] + row < board.shape[0] and 0 <= self.location[1] + col < board.shape[1] and \
                    board[self.location[0] + row, self.location[1] + col]:
                temp_score = 0
                if not board[self.location[0] + row, self.location[1] + col].empty:
                    temp_score = board[self.location[0] + row, self.location[1] + col].explode(board, color=self.color)
                if temp_score == BASE_SCORE:
                    temp_score = SPECIAL_SCORE
                score += temp_score

                row += direction[0]
                col += direction[1]

        return score

    def swipe_explosion(self, board, swipe_loc):
        """
        :param board: current game board
        :param swipe_loc: the location of the other candy being swiped
        :return: score of the special swipe move
        """
        other = board[swipe_loc]

        if isinstance(other, Chocolate):
            return other.swipe_explosion(board, self.location)

        elif isinstance(other, Striped):
            board[self.location].mark = True

            if isinstance(self, HorizontalStriped):
                board[swipe_loc] = VerticalStriped(other.color, other.location)
                board[swipe_loc].mark = True

            else:
                board[swipe_loc] = HorizontalStriped(other.color, swipe_loc)
                board[swipe_loc].mark = True

        elif isinstance(other, Wrapped):
            board[swipe_loc] = Candy(other.color, swipe_loc)
            board[swipe_loc].mark = True
            board[swipe_loc] = SuperStriped(swipe_loc)

        return 0


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

    def __init__(self, color, location, size=REGULAR):
        Special.__init__(self, color, location)
        self.secondExplosion = False
        self.size = size

    def explode(self, board, color=None):
        score = 0
        # iterate over candies to mark
        for candy in Wrapped.explosion_template[self.size]:
            if 0 <= self.location[0] + candy[0] < board.shape[0] and 0 <= self.location[1] + candy[1] < board.shape[1] and not \
                    board[self.location[0] + candy[0], self.location[1] + candy[1]].empty and not \
                    board[self.location[0] + candy[0], self.location[1] + candy[1]].mark:
                temp_score = board[self.location[0] + candy[0], self.location[1] + candy[1]].explode(board, color=self.color)
                if temp_score>BASE_SCORE: # the explosion cause second special explosions
                    score += temp_score

        self.mark = True
        # if this is the second explosion - mark the wrapped candy for deletion
        if self.secondExplosion:
            Candy.explode(self, board)
        self.secondExplosion = True

        return 540 + score

    def __str__(self):
        return 'W ' + Candy.__str__(self)

    def swipe_explosion(self, board, swipe_loc):
        """
        :param board: current game board
        :param swipe_loc: the location of the other candy being swiped
        :return: score of the special swipe move
        """

        other = board[swipe_loc]
        if isinstance(other, Chocolate):
            return other.swipe_explosion(board, self.location)

        elif isinstance(other, Striped):
            board[swipe_loc] = Candy(other.color, swipe_loc)
            board[swipe_loc].mark = True
            board[self.location] = SuperStriped(self.location)

        elif isinstance(other, Wrapped):
            board[swipe_loc].mark = True
            board[self.location].mark = True

        return 0


class Chocolate(Special):
    def __init__(self, location, color=Candy.NO_COLOR):
        Special.__init__(self, color, location)

    def explode(self, board, color=0):
        Candy.explode(self, board)
        score = 0
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row, col].color == color and not board[row, col].empty and not board[row, col].mark:
                    temp_score = board[row, col].explode(board)
                    if temp_score == BASE_SCORE:
                        temp_score = SPECIAL_SCORE
                    score += temp_score

        return score

    def clear_board(self, board):
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                board[row, col] = UnknownCandy((row, col))

        return (board.shape[0] + 1) * (board.shape[1] + 1) * SPECIAL_SCORE - 2 * SPECIAL_SCORE

    @staticmethod
    def make_special(board, color, special_type):
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row, col].color == color and not board[row, col].empty and not board[row, col].mark:
                    board[row, col] = special_type(color, (row, col))
                    board[row, col].mark = True

    def swipe_explosion(self, board, swipe_loc):
        """
        :param board: current game board
        :param swipe_loc: the location of the other candy being swiped
        :return: score of the special swipe move
        """
        other = board[swipe_loc]

        if isinstance(other, UnknownCandy):
            raise ChocolateWithUnknown()

        if isinstance(other, Chocolate):
            return self.clear_board(board)

        else:
            board[self.location].mark = True

            if isinstance(other, Wrapped):
                raise WrappedChocolateException()

            elif isinstance(other, VerticalStriped):
                Chocolate.make_special(board, other.color, VerticalStriped)
            elif isinstance(other, HorizontalStriped):
                Chocolate.make_special(board, other.color, HorizontalStriped)

            return self.explode(board, other.color)


class SuperStriped(Special):
    def __init__(self, location):
        Special.__init__(self, Candy.SUPER_STRIPED_COLOR, location)
        self.mark = True

    def explode(self, board, color=None):
        score = 0
        Candy.explode(self, board)
        for row_offset in range(-1, 2):
            for col_offset in range(-1, 2):
                for directions in DIRECTIONS:
                    for direction in directions:
                        row = direction[0] + row_offset
                        col = direction[1] + col_offset
                        while 0 <= self.location[0] + row < board.shape[0] and 0 <= self.location[1] + col < \
                                board.shape[1] and board[self.location[0] + row, self.location[1] + col]:
                            temp_score = 0
                            if not board[self.location[0] + row, self.location[1] + col].empty:
                                temp_score = board[self.location[0] + row, self.location[1] + col].explode(board)
                            if temp_score == BASE_SCORE:
                                temp_score = SPECIAL_SCORE
                            score += temp_score

                            row += direction[0]
                            col += direction[1]
        score -= 480
        return score
