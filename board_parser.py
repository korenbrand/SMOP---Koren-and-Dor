from main import board_dict
from Candy import *
import numpy as np

board_dict = {0: 'blue       ', 1: 's_h_blue   ', 2: 'green      ', 3: 's_h_green  ', 4: 'orange     ',
              5: 's_h_orange ',
              6: 'purple     ', 7: 's_h_purple ', 8: 'red        ', 9: 's_h_red    ', 10: 'yellow   ',
              11: 's_h_yellow ',
              12: 'chocolate', 13: 's_v_blue   ', 14: 's_v_green  ', 15: 's_v_orange ', 16: 's_v_red    ',
              17: 's_v_yellow ', 18: 's_v_purple ', 19: 'blue_wrapped', 20: 'green_wrapped', 21: 'orange_wrapped',
              22: 'purple_wrapped', 23: 'red_wrapped', 24: 'yellow_wrapped', -1: 'empty    '}

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
                        (19, 20, 21, 22, 23, 24): Wrapped, -1: EmptyCandy}
    key = Board.access_key(candy_number, translation_dict)

    return translation_dict[key](color=candy_number, location=location)

def interpret_board(self, numbers_board):
    # initialize the new board
    board = np.ndarray(numbers_board.shape, dtype=object)
    print(board.shape)

    for row in range(numbers_board.shape[0]):
        for col in range(numbers_board.shape[1]):
            print(board_dict[numbers_board[row, col]])
            board[row, col] = Board.get_candy(numbers_board[row, col], [row, col])

    self.board = board


test_board = np.array([[1,2,3],[4,5,6]])
board = interpret_board(test_board)