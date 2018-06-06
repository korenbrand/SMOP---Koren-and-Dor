from main import board_dict
board_size = 9

# the score that regular candies exploding from special explosion receive
BASE_SCORE = 60


class Candy:
    STRIPE_SCORE, WRAP_SCORE, COLOR_BOMB_SCORE = 120, 200, 200
    NO_COLOR = 12  # chocolate cookie key in dict
    EMPTY = -1

    def __init__(self, color, location):
        self.color = color
        self.location = location
        self.empty = False
        self.mark = False

    def explode(self, board):
        board[self.location[0], self.location[1]].empty = True
        # if this exploded not from a streak but from a special candy, add EXPLODED_SCORE to total score
        return BASE_SCORE

    def __str__(self):
        if self.mark:
            mark = " X"
        else:
            mark = ""
        description = '{:16}'.format(board_dict[self.color] + mark)
        return description


class EmptyCandy(Candy):
    def __init__(self, location):
        Candy(self, Candy.EMPTY, location)
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
        score = Candy.explode(self, board)
        # mark the entire direction (row or column)
        for direction in self.directions:
            row = direction[0]
            col = direction[1]
            while 0 <= self.location[0] + row < board_size and 0 <= self.location[1] + col < board_size and \
                    board[self.location[0] + row, self.location[1] + col] and \
                    board[self.location[0] + row, self.location[1] + col].mark == False:
                score += board[self.location[0] + row, self.location[1] + col].explode()
                row += direction[0]
                col += direction[1]

        return score


class VerticalStriped(Striped):
    def __init__(self, color, location):
        Striped.__init__(self, color, location, DIRECTIONS[VERT])


class HorizontalStriped(Striped):
    def __init__(self, color, location):
        Striped.__init__(self, color, location, DIRECTIONS[HORZ])


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
            if 0 <= self.location[0] + candy[0] < board_size and 0 <= self.location[1] + candy[1] < board_size and \
                    board[self.location[0] + candy[0], self.location[1] + candy[1]] and \
                    not board[self.location[0] + candy[0], self.location[1] + candy[1]].mark:
                score += board[self.location[0] + candy[0], self.location[1] + candy[1]].explode()

        # if this is the second explosion - mark the wrapped candy for deletion
        if self.secondExplosion:
            board[self.location].delete = True
        self.secondExplosion = True
        return score


class Chocolate(Special):
    def __init__(self, location, color=Candy.NO_COLOR):
        Special.__init__(self, color, location)

    def explode(self, board, color):
        score = Candy.explode(self, board)
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row, col] and board[row, col] == color and not board[row, col].mark:
                    score += board[row, col].explode(board)

        return score
