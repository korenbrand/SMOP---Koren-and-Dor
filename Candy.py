from main import board_size

# the score that regular candies exploding from special explosion receive
BASE_SCORE = 60

class Candy:
    REGULAR, STRIPE_UP, STRIPE_SIDES, WRAP, WRAP_EXPLODE, COLOR_BOMB = 1, 2, 3, 4, 5, 6
    STRIPE_SCORE, WRAP_SCORE, COLOR_BOMB_SCORE = 120, 200, 200
    RED, BLUE, YELLOW, GREEN, PURPLE, ORANGE, NO_COLOR = 1, 2, 3, 4, 5, 6, -1

    def __init__(self, color, location):
        self.color = color
        self.location = location
        self.empty = False
        self.mark = False

    def explode(self, board):
        board[self.location[0], self.location[1]].delete = True
        # if this exploded not from a streak but from a special candy, add EXPLODED_SCORE to total score
        return BASE_SCORE

VERT, HORZ = 1, 0
# directions for row (left and right) and column (up and down)
DIRECTIONS = [[(0, 1), (0, -1)],
              [(1, 0), (-1, 0)]]

class Striped(Candy):

    def __init__(self, color, location, directions):
        Candy.__init__(self, color, location)
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

REGULAR, BIG = 0, 1

class Wrapped(Candy):
    explosion_template = [[(-1, -1), (-1, 0), (-1, 1),
                           (0, -1), (0, 1),
                           (1, -1), (1, 0), (1, 1)],
                          [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2),
                           (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2),
                           (0, -2), (0, -1), (0, 1), (0, 2),
                           (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
                           (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]]

    def __init__(self, color, location, size):
        Candy.__init__(self, color, location)
        self.explosion_candies = Wrapped.explosion_template[size]
        self.secondExplosion = False

    def explode(self, board):
        score = BASE_SCORE
        # iterate over candies to mark
        for candy in Wrapped.explosion_template:
            if 0 <= self.location[0] + candy[0] < board_size and 0 <= self.location[1] + candy[1] < board_size and \
                    board[self.location[0] + candy[0], self.location[1] + candy[1]] and \
                    board[self.location[0] + candy[0], self.location[1] + candy[1]].mark == False:
                score += board[self.location[0] + candy[0], self.location[1] + candy[1]].explode()

        # if this is the second explosion - mark the wrapped candy for deletion
        if self.secondExplosion:
            board[self.location].delete = True
        self.secondExplosion = True
        return score


class Chocolate(Candy):
    def __init__(self, location):
        Candy.__init__(self, Candy.NO_COLOR, location)

    def explode(self, board, color):
        score = Candy.explode(self, board)
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row,col] and board[row, col] == color and board[row,col].mark ==  False:
                    score += board[row, col].explode(board)

        return score
