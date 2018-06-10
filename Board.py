from __future__ import print_function
from random import randint
import numpy as np
from Candy import *
from Move import Move


class Board:
    DEFAULT_NUM_OF_CANDIES = 6
    DEFAULT_HEIGHT = 9
    DEFAULT_WIDTH = 9
    DEFAULT_STRIKE = 3
    NO_SCORE = 0
    STRIPED, CHOCOLATE = 4, 5
    NONE_MOVE = Move((-1, -1), (-1, -2), True)

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

    @staticmethod
    def access_key(x, dictionary):
        for key in dictionary.keys():
            if type(key) == int:
                if x == key:
                    return key
            elif x in key:
                return key

    @staticmethod
    def get_candy(candy_number, location):
        translation_dict = {(0, 2, 4, 6, 8, 10): Candy, (1, 3, 5, 7, 9, 11): HorizontalStriped,
                            (13, 14, 15, 16, 17, 18): VerticalStriped, 12: Chocolate,
                            (19, 20, 21, 22, 23, 24): Wrapped, -1: 'special'}
        translation_color = {(0, 1, 13, 19): 0, (2, 3, 14, 20): 1, (4, 5, 15, 21): 2, (6, 7, 18, 22): 3, (8, 9, 16, 23): 4, (10, 11, 17, 24): 5, 12: 6}

        key = Board.access_key(candy_number, translation_dict)
        color_key = Board.access_key(candy_number, translation_color)

        return translation_dict[key](color=translation_color[color_key], location=location)

    def interpret_board(self, numbers_board):
        # initialize the new board
        board = np.ndarray(numbers_board.shape, dtype=object)
        self.height, self.width = board.shape

        for row in range(numbers_board.shape[0]):
            for col in range(numbers_board.shape[1]):
                board[row, col] = Board.get_candy(numbers_board[row, col], (row, col))

        self.board = board

    def initialize_board(self, num_of_candies, width, height):
        """
        this function initialize new board with random candies.
        """
        new_board = np.zeros(shape=(height, width), dtype=object)
        for row in range(height):
            for col in range(width):
                new_board[row][col] = Candy(randint(0, num_of_candies - 1), (row, col))  # in randint the edges are inclusive
        self.board = new_board

    def is_empty(self, location):
        return self.board[location].empty or isinstance(self.board[location], UnknownCandy)

    def check_row_matches(self, row, strike_length=DEFAULT_STRIKE):
        """
        :param row: the row of want to check
        :param strike_length: the length of the strikes you want
        :return:  list of tuple describe the the strikes in length of 3 or more in the row
        """
        length, strike_start, strike_end = 1, 0, 0
        list_of_matches = []
        for col in range(self.width):
            if col == self.width - 1 or self.board[row, col].color != self.board[row, col + 1].color or self.is_empty((row,col + 1)) or self.is_empty((row,col)):
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
            if row == self.height - 1 or self.board[row][col].color != self.board[row + 1][col].color or self.is_empty((row+1,col)) or self.is_empty((row,col)):
                if length >= strike_length:
                    list_of_matches.append((strike_start, strike_end))
                length = 1
                strike_start = row + 1
            else:
                length += 1
                strike_end = row + 1
        return list_of_matches

    def mark_candies_to_explode(self, last_move=NONE_MOVE):
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
                if length == Board.STRIPED:  # stripe
                    striped_counter += 1
                    score += 60
                    # todo estimate the score that will yield from this candy
                    if row == last_move.start[0] or row == last_move.end[0]:
                        if tuple_indices[1] >= last_move.start[1] >= tuple_indices[0]:
                            self.board[row][last_move.start[1]] = VerticalStriped(self.board[row][last_move.start[1]].color, (row, last_move.start[1]))  # ""
                        elif tuple_indices[1] >= last_move.end[1] >= tuple_indices[0]:  # the last move cause this streak
                            self.board[row][last_move.end[1]] = Striped(self.board[row][last_move.end[1]].color, (row, last_move.end[1]),
                                                                        DIRECTIONS[VERT])

                elif length >= Board.CHOCOLATE:  # color bomb
                    chocolate_counter += 1
                    # this is a five streak - each candy awards 40 points instead of 20
                    score += 120
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
                    candy = self.board[row_index + tuple_indices[0], col]
                    # check for wrap
                    if candy.mark or (isinstance(candy, Striped) and not candy.mark and 0 < col < self.width - 1 and self.board[row_index + tuple_indices[0], col - 1].mark and self.board[
                        row_index + tuple_indices[0], col - 1].color == candy.color and self.board[row_index + tuple_indices[0], col + 1].mark and self.board[
                                          row_index + tuple_indices[0], col + 1].color == candy.color):
                        # if this is an wrap structure, even it also strip structure, make wrap
                        if isinstance(candy, Striped):
                            striped_counter -= 1
                            score -= 60
                        wrapped_counter += 1
                        score += 120
                        self.board[row_index + tuple_indices[0], col] = Wrapped(self.board[row_index + tuple_indices[0], col].color, (row_index + tuple_indices[0], col))
                    else:
                        candy.mark = True

                if length == Board.STRIPED:  # stripe
                    striped_counter += 1
                    score += 60
                    if col == last_move.start[1] or col == last_move.end[1]:
                        if tuple_indices[1] >= last_move.start[0] >= tuple_indices[0]:
                            if self.board[last_move.start[0]][col].mark:  # is not un marked wrap:
                                self.board[last_move.start[0]][col] = HorizontalStriped(self.board[last_move.start[0], col].color, (last_move.start[0], col))  # ""
                        elif tuple_indices[1] >= last_move.end[0] >= tuple_indices[0]:  # the last move cause this strike
                            if self.board[last_move.end[0]][col].mark:  # is not un marked wrap:
                                self.board[last_move.end[0]][col] = Striped(self.board[last_move.end[0], col].color, (last_move.end[0], col),
                                                                            DIRECTIONS[HORZ])  # with the direction of the last move direction, remove the mark!
                    else:
                        self.board[tuple_indices[1]][col] = Striped(self.board[tuple_indices[1]][col].color, (tuple_indices[1], col), DIRECTIONS[VERT])

                elif length == Board.CHOCOLATE:  # color bomb
                    chocolate_counter += 1
                    if col == last_move.start[1] or col == last_move.end[1]:
                        if tuple_indices[1] >= last_move.start[0] >= tuple_indices[0]:
                            self.board[last_move.start[0]][col] = Chocolate((last_move.start[0], col))
                        elif tuple_indices[1] >= last_move.end[0] >= tuple_indices[0]:  # the last move cause this strike
                            self.board[last_move.start[0]][col] = Chocolate((last_move.start[0], col))  # with the direction of the last move direction, remove the mark!

        special_counters = (striped_counter, wrapped_counter, chocolate_counter)

        if last_move != Board.NONE_MOVE:
            if isinstance(self.board[last_move.start], Special):
                score += self.board[last_move.start].swipe_explosion(self.board, last_move.end)
            if isinstance(self.board[last_move.end], Special):
                score += self.board[last_move.end].swipe_explosion(self.board, last_move.start)
        return score, special_counters

    def print_board(self):
        print()
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col].empty:
                    print('{:16}'.format("Empty"), end="")
                else:
                    print(self.board[row][col], end="")
            print()
        print("The score of the board is: ", self.score)

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
        possible_moves = []
        ########################
        # check horizontal moves
        ########################
        for row in range(self.height):
            for col in range(self.width - 1):

                self.make_move((row, col), (row, col + 1))  # make move only for checking for matching
                if self.check_row_matches(row) or self.check_col_matches(col) or self.check_col_matches(
                        col + 1) or (isinstance(self.board[row, col], Special) and isinstance(self.board[row, col + 1], Special)) or \
                        isinstance(self.board[row, col], Chocolate) or isinstance(self.board[row, col + 1], Chocolate):
                    possible_moves.append(Move((row, col), (row, col + 1), HORZ))
                self.make_move((row, col), (row, col + 1))  # return to the original board by commit the move again
        ########################
        # check vertical moves
        ########################
        for col in range(self.width):
            for row in range(self.height - 1):
                self.make_move((row, col), (row + 1, col))  # make move only for checking for matching
                if self.check_col_matches(col) or self.check_row_matches(row) or self.check_row_matches(
                        row + 1) or (isinstance(self.board[row, col], Special) and isinstance(self.board[row + 1, col], Special)) or \
                        isinstance(self.board[row, col], Chocolate) or isinstance(self.board[row + 1, col], Chocolate):
                    possible_moves.append(Move((row, col), (row + 1, col), VERT))
                self.make_move((row, col), (row + 1, col))  # return to the original board by commit the move again
        return possible_moves

    def print_possible_moves(self):
        possible_moves = self.possible_moves()
        print("possible moves:")
        for move_num, move in enumerate(possible_moves):
            print("move number " + str(move_num) + ": ", move)

    def make_move(self, start_tup, end_tup):
        tmp = self.board[start_tup]
        self.board[start_tup] = self.board[end_tup]
        self.board[start_tup].location = start_tup  # we also need to update the location
        self.board[end_tup] = tmp
        self.board[end_tup].location = end_tup

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

    def print_matches(self):
        print()
        print("rows:")
        for row in range(self.height):
            if self.check_row_matches(row):
                print(str(row), " ", self.check_row_matches(row))
        print("cols:")
        for col in range(self.width):
            if self.check_col_matches(col):
                print(str(col), " ", self.check_col_matches(col))

    def explosions(self):
        score = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row, col].mark and not self.board[row, col].empty:
                    score += self.board[row, col].explode(self.board)

        return score

    def turn_chunk(self, move):
        score = self.mark_candies_to_explode(move)[0]
        # self.print_board()
        score += self.explosions()
        self.cascade()
        self.reset_next_round()

        return score

    def turn_function(self, move=NONE_MOVE):
        score = self.turn_chunk(move)
        chain_score = self.turn_chunk(move)

        while chain_score > 0:
            score += chain_score
            chain_score = self.turn_chunk(move)
        self.score += score
        return score

    def reset_next_round(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row, col].empty:
                    self.board[row, col] = UnknownCandy((row, col))

    def play_a_game(self, detailed_game=False):  # flag if you want detailed game
        if detailed_game:
            self.print_board()
        self.turn_function()
        while True:
            self.print_board()
            possible_moves = self.possible_moves()
            if not possible_moves:
                print("no more possible moves")
                pass
                exit(0)
            self.print_possible_moves()
            x = raw_input("insert number of move")
            board.make_move(possible_moves[int(x)].start, possible_moves[int(x)].end)
            if detailed_game:
                board.print_board()
                raw_input()
            board.turn_function(Move(possible_moves[int(x)].start, possible_moves[int(x)].end, True))

    @staticmethod
    def play_game_from_existing_board(board):
        new_board = Board(board.shape[0], board.shape[1])
        new_board.interpret_board(board)
        new_board.play_a_game()


board = Board()
board.play_a_game(True)
#
# board = Board(height=6, width=5)
# board_to_copy = np.array([[0, 0, 8, 2, 8], [4, 20, 19, 6, 2], [0, 2, 10, 2, 2], [10, 4, 0, 2, 10], [0, 8, 0, 8, 2], [8, 0, 8, 0, 8]])
# board.interpret_board(board_to_copy)
# board.print_board()
# board.turn_function()
# while True:
#    board.print_board()
#    possible_moves = board.possible_moves()
#    if not possible_moves:
#        print("no more possible moves")
#        pass
#        exit(0)
#
#    board.print_possible_moves()
#    x = raw_input("insert number of move")
#    board.make_move(possible_moves[int(x)].start, possible_moves[int(x)].end)
#    board.print_board()
#    raw_input()
#    board.turn_function(Move(possible_moves[int(x)].start, possible_moves[int(x)].end, True))
#
# def main():
#    board = Board(height=3, width=5)111
#    board_to_copy = np.array([[2,0,4,0,4],[0,0,2,0,4],[2,4,0,4,4]])
#    board.interpret_board(board_to_copy)
#    board.print_board()
#    board.mark_candies_to_explode()
#    board.print_board()
#    board.print_matches()
#    board.explosions()
#    board.print_board()
#    board.print_matches()
#    board.cascade()
#    board.mark_candies_to_explode()
#    board.explosions()
#    board.cascade()
#    while True:
#        board.print_board()
#        possible_moves = board.possible_moves()
#        board.print_possible_moves()
#        x = raw_input("insert number of move")
#        board.make_move(possible_moves[int(x)].start, possible_moves[int(x)].end)
#        board.print_board()
#        raw_input()
#        board.mark_candies_to_explode(Move(possible_moves[int(x)].start, possible_moves[int(x)].end, True))
#        board.explosions()
#        board.cascade()


# if __name__ == '__main__':
