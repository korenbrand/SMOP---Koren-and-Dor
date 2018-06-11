import copy
from uncertainty_exception import UncertaintyException

from Board import Board

score_coeff, stripe_coeff, wrapped_coeff, chocolate_coeff, uncertainty_factor = 0, 0, 0, 0, 0


class heuristic_player:
    def __init__(self, game_board):
        self.base_board = Board(board_to_copy=game_board)
        self.best_move = None

    def choose_move(self):
        max_move = None
        max_value = 0
        for move in self.base_board.possible_moves():
            move_board = copy.deepcopy(self.base_board)
            move_board.reset_param()
            try:
                move_board.make_move(move)
                move_board.turn_function(move)

                output = move_board.evaluate_turn(score_coeff, stripe_coeff, wrapped_coeff, chocolate_coeff,
                                                  uncertainty_factor)
                if output > max_value:
                    max_move = move
                    max_value = output

            except UncertaintyException:
                print('Uncertainty raised at move: ' + move)

        self.best_move = max_move
