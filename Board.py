from random import randint
import numpy
import Candy


class Board:
    DEFAULT_NUM_OF_CANDIES = 6
    DEFAULT_HEIGHT = 9
    DEFAULT_WIDTH = 9
    DEFAULT_STRIKE = 3

    def __init__(self, num_of_candies=DEFAULT_NUM_OF_CANDIES, height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH):
        """
        this function create new game board
        """
        self.height = height
        self.width = width
        self.num_of_candies = num_of_candies
        self.score = 0
        self.initialize_board(num_of_candies, width, height)

    def initialize_board(self, num_of_candies, width, height):
        """
        this function initialize new board with random candies.
        """
        new_board = numpy.zeros(shape=(height, width))
        for row in range(height):
            for col in range(width):
                new_board[row][col] = Candy.Candy(randint(0, (num_of_candies - 1,1),1))  # in randint the edges are inclusive
        self.board = new_board

    def check_row_matches(self, row):
        """
        :param row: the row of want to check
        :return:  list of tuple describe the the strikes in length of 3 or more in the row
        """
        length, strike_start, strike_end = 1, 0, 0
        list_of_matches = []
        for col in range(self.width):
            if col == self.width - 1 or self.board[row][col] != self.board[row][col + 1]:
                if length >= 3:
                    list_of_matches.append((strike_start, strike_end))
                length = 1
                strike_start = col + 1
            else:
                length += 1
                strike_end = col + 1
        return list_of_matches

    def check_col_matches(self, col, strike_length = DEFAULT_STRIKE):
        """
        :param col: the col of want to check
        :return:  list of tuple describe the the strikes in length of 3 or more in the col
        """
        length, strike_start, strike_end = 1, 0, 0
        list_of_matches = []
        for row in range(self.height):
            if row == self.height - 1 or self.board[row][col] != self.board[row + 1][col]:
                if length >= length:
                    list_of_matches.append((strike_start, strike_end))
                length = 1
                strike_start = row + 1
            else:
                length += 1
                strike_end = row + 1
        return list_of_matches

    def update_board(self):
        row_matches = []
        col_matches = []
        for row in range(board.height):


        for col in range(board.width):
            col_matches.append(self.check_col_matches(col))




board = Board()

print board.board[0][0]
print board.board
print "rows:"
for row in range(board.height):
    print(board.check_row_matches(row))
print "cols:"
for col in range(board.width):
    print(board.check_col_matches(col))