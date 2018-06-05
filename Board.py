from __future__ import print_function
from random import randint
import numpy
from Candy import *
from Move import Move


class Board:
    DEFAULT_NUM_OF_CANDIES = 6
    DEFAULT_HEIGHT = 9
    DEFAULT_WIDTH = 9
    DEFAULT_STRIKE = 3
    NO_SCORE = 0
    STRIPED, CHOCOLATE = 4, 5

    def __init__(self, num_of_candies=DEFAULT_NUM_OF_CANDIES, height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH):
        """
        this function create new game board
        """
        self.height = height
        self.width = width
        self.num_of_candies = num_of_candies
        self.score = 0
        self.board = None
        self.initialize_board(num_of_candies, width, height)

    def initialize_board(self, num_of_candies, width, height):
        """
        this function initialize new board with random candies.
        """
        new_board = numpy.zeros(shape=(height, width), dtype=object)
        for row in range(height):
            for col in range(width):
                new_board[row][col] = Candy(randint(0, num_of_candies - 1),
                                            (row, col))  # in randint the edges are inclusive
        self.board = new_board

    def check_row_matches(self, row, strike_length=DEFAULT_STRIKE):
        """
        :param row: the row of want to check
        :param strike_length: the length of the strikes you want
        :return:  list of tuple describe the the strikes in length of 3 or more in the row
        """
        length, strike_start, strike_end = 1, 0, 0
        list_of_matches = []
        for col in range(self.width):
            if col == self.width - 1 or self.board[row, col].color != self.board[row, col + 1].color or self.board[row][col].empty:
                if length >= strike_length:
                    list_of_matches.append((strike_start, strike_end))
                length = 1
                strike_start = col + 1
            else:
                length += 1
                strike_end = col + 1
        return list_of_matches

    def check_col_matches(self, col, strike_length=DEFAULT_STRIKE):
        """
        :param col: the col of want to check
         :param strike_length: the length of the strikes you want
        :return:  list of tuple describe the the strikes in length of 3 or more in the col
        """
        length, strike_start, strike_end = 1, 0, 0
        list_of_matches = []
        for row in range(self.height):
            if row == self.height - 1 or self.board[row][col].color != self.board[row + 1][col].color or \
                    self.board[row][col].empty:
                if length >= strike_length:
                    list_of_matches.append((strike_start, strike_end))
                length = 1
                strike_start = row + 1
            else:
                length += 1
                strike_end = row + 1
        return list_of_matches

    def mark_candies_to_explode(self, last_move=Move((-1, -1), (-1, -1), True)):
        """
        this function mark all the candies in the board that need to be exploded and also create all the special
        candies in the board
        :param last_move: the last move

        :return the socre the initial marking accord to + the number of each type of special candies created
        """
        striped_counter = 0
        wrapped_counter = 0
        chocolate_counter = 0
        score = Board.NO_SCORE
        ##############
        # ROW CHECK
        ##############
        for row in range(self.height):
            for tuple_indices in self.check_row_matches(row):
                length = tuple_indices[1] - tuple_indices[0] + 1
                for col_index in range(length):
                    self.board[row][col_index + tuple_indices[0]].mark = True
                    score += 20
                if length == board.STRIPED:  # stripe
                    striped_counter += 1
                    # this is a four streak - each candy awards 30 points instead of 20
                    score += 40
                    if row == last_move.start[0] or row == last_move.end[0]:
                        if tuple_indices[1] >= last_move.start[1] >= tuple_indices[0]:
                            self.board[row][last_move.start[1]] = Striped(self.board[row][last_move.start[1]].color, (row, last_move.start[1]),
                                                                          DIRECTIONS[VERT])  # ""
                        elif tuple_indices[1] >= last_move.end[1] >= tuple_indices[0]:  # the last move cause this streak
                            self.board[row][last_move.end[1]] = Striped(self.board[row][last_move.end[1]].color, (row, last_move.end[1]),
                                                                        DIRECTIONS[VERT])

                elif length == board.CHOCOLATE:  # color bomb
                    chocolate_counter += 1
                    # this is a five streak - each candy awards 40 points instead of 20
                    score += 100
                    if row == last_move.start[0] or row == last_move.end[0]:
                        if tuple_indices[1] >= last_move.start[1] >= tuple_indices[0]:
                            self.board[row][last_move.start[1]] = Chocolate((row, last_move.start[1]))  # ""
                        elif tuple_indices[1] >= last_move.end[1] >= tuple_indices[0]:  # the last move cause this strike
                            self.board[row][last_move.start[1]] = Chocolate((row, last_move.end[1]))

        ##############
        # COLUMN CHECK
        ##############
        for col in range(self.width):
            for tuple_indices in self.check_col_matches(col):
                length = tuple_indices[1] - tuple_indices[0] + 1
                for row_index in range(length):
                    if self.board[row_index + tuple_indices[0], col].mark:  # *or*its stripe - how to check?: #this is wrap
                        wrapped_counter += 1
                        self.board[row_index, col] = Wrapped(self.board[row_index, col].color, REGULAR, 1)
                    else:
                        self.board[row_index + tuple_indices[0]][col].mark = True

                if length == board.STRIPED:  # stripe
                    striped_counter += 1
                    if col == last_move.start[1] or col == last_move.end[1]:
                        if tuple_indices[1] >= last_move.start[0] >= tuple_indices[0]:
                            if self.board[last_move.start[0]][col].mark:  # is not un marked wrap:
                                self.board[last_move.start[0]][col] = Striped(self.board[last_move.start[0], col].color, (last_move.start[0], col),
                                                                              DIRECTIONS[HORZ])  # ""
                        elif tuple_indices[1] >= last_move.end[0] >= tuple_indices[0]:  # the last move cause this strike
                            if self.board[last_move.end[0]][col].mark:  # is not un marked wrap:
                                self.board[last_move.end[0]][col] = Striped(self.board[last_move.end[0], col].color, (last_move.end[0], col),
                                                                            DIRECTIONS[HORZ])  # with the direction of the last move direction, remove the mark!

                elif length == board.CHOCOLATE:  # color bomb
                    chocolate_counter += 1
                    if col == last_move.start[1] or col == last_move.end[1]:
                        if tuple_indices[1] >= last_move.start[0] >= tuple_indices[0]:
                            self.board[last_move.start[0]][col] = Chocolate((last_move.start[0], col))
                        elif tuple_indices[1] >= last_move.end[0] >= tuple_indices[0]:  # the last move cause this strike
                            self.board[last_move.start[0]][col] = Chocolate((last_move.start[0], col))  # with the direction of the last move direction, remove the mark!

        special_counters = (striped_counter, wrapped_counter, chocolate_counter)
        return score, special_counters

    def print_board(self):
        for row in range(board.height):
            for col in range(board.width):
                print(" ", self.board[row][col], end="")
            print()

    def in_board(self, location):
        """
        :param location: a 2d coordinate
        :return: True if it is a valid coordinate on board
        """
        return 0 <= location[0] < self.height and 0 <= location[1] < self.width

    def get_adjacent(self, location):
        """
        :param location: a coordinate in board
        :return all adjacent locations to given location
        """
        adjacent_loc = [(location[0] - 1, location[1]), (location[0] + 1, location[1]), (location[0], location[1] - 1), (location[0] - 1, location[1] + 1)]

        for adjacent in adjacent_loc:
            if not self.in_board(adjacent):
                adjacent_loc.remove(adjacent)

        return adjacent_loc

    # this function is part of board class
    def possible_moves(self):
        horizontal_moves = []
        vertical_moves = []
        ########################
        # check horizontal moves
        ########################
        for row in range(self.height):
            for col in range(self.width - 1):
                self.make_move((row, col), (row, col + 1))  # make move only for checking for matching
                if row_matches(row):
                    horizontal_moves.append(Move((row, col), (row, col + 1), HORZ))
                self.make_move((row, col), (row, col + 1))  # return to the original board by commit the move again
        ########################
        # check vertical moves
        ########################
        for col in range(self.width):
            for row in range(self.height - 1):
                self.make_move((row, col), (row + 1, col))  # make move only for checking for matching
                if col_matches(col):
                    vertical_moves.append(Move((row, col), (row + 1, col), VERT))
                self.make_move((row, col), (row + 1, col))  # return to the original board by commit the move again

        return horizontal_moves, vertical_moves


    def cascade(self):
        for col in range(self.width):
            for row in range(self.height - 1, -1, -1):
                col_is_empty = False
                if self.board[(row, col)].empty:
                    tmp_row = row  # we don't want to override the original row
                    while self.board[(tmp_row, col)].empty:
                        if tmp_row == 0:  # this is the higher candy in the col
                            col_is_empty = True
                            break
                        tmp_row -= 1
                    if col_is_empty:
                        break
                    else:
                        self.make_move((row, col), (tmp_row, col))


def main():
    board = Board()
    board.mark_candies_to_explode()
    board.print_board()
    print("rows:")
    for row in range(board.height):
        print(board.check_row_matches(row))
    print("cols:")
    for col in range(board.width):
        print(board.check_col_matches(col))

if __name__ == '__main__':
    main()
