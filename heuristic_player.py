import copy
import random

from uncertainty_exception import UncertaintyException

from Board import Board

score_coeff, stripe_coeff, wrapped_coeff, chocolate_coeff, uncertainty_factor, low_factor = 0.5, 1, 2, 3, 0.5, 0


class HeuristicPlayer:
    def __init__(self):
        self.base_board = None
        self.best_move = None

    def get_board(self, game_board):
        self.base_board = Board(board_to_copy=game_board)
        self.base_board.print_board()

    def get_best_move(self):
        if self.best_move:
            return self.best_move

        moves = self.base_board.possible_moves()
        move = random.choice(moves)
        print 'Instead doing: ' + str(move)
        return move

    def evaluate_move(self, move, board):
        board.make_move(move.start, move.end)
        board.turn_function(move)

        return board.evaluate_turn(score_coeff, stripe_coeff, wrapped_coeff, chocolate_coeff, uncertainty_factor) + \
               max(move.start[0], move.end[0]) * low_factor

    def choose_move(self):
        max_move = None
        max_value = 0
        for move in self.base_board.possible_moves():
            move_board = copy.deepcopy(self.base_board)
            move_board.reset_param()
            try:
                output = self.evaluate_move(move, move_board)
                if output > max_value:
                    max_move = move
                    max_value = output

            except UncertaintyException:
                print('Uncertainty raised at move: ' + str(move))

        self.best_move = max_move
        print 'Best move is: ' + str(self.best_move)
