from main import board_size


class Candy:
    REGULAR, STRIPE_UP, STRIPE_SIDES, WRAP, WRAP_EXPLODE, COLOR_BOMB = 1, 2, 3, 4, 5, 6
    STRIPE_SCORE, WRAP_SCORE, COLOR_BOMB_SCORE = 120, 200, 200
    RED, BLUE, YELLOW, GREEN, PURPLE, ORANGE = 1, 2, 3, 4, 5, 6

    def __init__(self, color, location):
        self.color = color
        self.location = location
        self.delete = False

    def explode(self, board):
        board[self.location[0], self.location[1]].delete = True


# directions for row (left and right) and column (up and down)
DIRECTIONS = [[(0, 1), (0, -1)],
              [(1, 0), (-1, 0)]]


class Striped(Candy):
    def __init__(self, color, location, directions):
        Candy.__init__(self, color, location)
        self.directions = directions

    def explode(self, board):
        Candy.explode(self, board)
        # delete the entire direction (row or column)
        for direction in self.directions:
            row = direction[0]
            col = direction[1]
            while 0 <= self.location[0] + row < board_size and 0 <= self.location[1] + col < board_size:
                board[self.location[0] + row, self.location[1] + col].delete = True
                row += direction[0]
                col += direction[1]


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

    def explode(self, board):
        # iterate over candies to delete
        for candy in Wrapped.explosion_template:
            if 0 <= self.location[0] + candy[0] < board_size and 0 <= self.location[1] + candy[1] < board_size:
                board[self.location[0] + candy[0], self.location[1] + candy[1]].delete = True