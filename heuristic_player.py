import copy
import random

from uncertainty_exception import UncertaintyException

from Board import Board


# score_coeff, stripe_coeff, wrapped_coeff, chocolate_coeff = 2, 1, 1, 2
# uncertainty_factor, low_factor, layer_factor = 0, 0, 0
"""
Simple parameters: score, stripe, wrapped, chocolate, low(height factor)
Advanced parameters: Simple parameters, layer(recursion depth), uncertainty
"""


class HeuristicPlayer:
    def __init__(self, params):
        self.base_board = None
        self.best_move = None
        self.params = params[:-1]
        self.low_factor = params[-1]

    def get_board(self, game_board):
        if isinstance(game_board, Board):
            self.base_board = game_board
        else:
            self.base_board = Board(board_to_copy=game_board)
        #self.base_board.print_board()

    def get_best_move(self):
        if self.best_move:
            return self.best_move

        moves = self.base_board.possible_moves()
        move = random.choice(moves)
        #print 'Instead doing: ' + str(move)
        return move

    @staticmethod
    def evaluate_move(move, board, params, low_factor):
        board.make_move(move.start, move.end)
        board.turn_function(move)

        return board.evaluate_turn(*params) + float((move.start[0] + move.end[0]) * low_factor) / 2

    def choose_move(self):
        max_move = None
        max_value = 0
        moves = self.base_board.possible_moves()

        if not moves:
            self.base_board.initialize_board()
            self.base_board.turn_function(with_unknowns=False)
            self.choose_move()

        for move in moves:
            move_board = copy.deepcopy(self.base_board)
            move_board.reset_param()

            output = self.evaluate_move(move, move_board, self.params, self.low_factor)
            if output > max_value:
                max_move = move
                max_value = output

        self.best_move = max_move
        # 'Best move is: ' + str(self.best_move)


class AdvancedHeuristicPlayer(HeuristicPlayer):
    def __init__(self, params):
        HeuristicPlayer.__init__(self, params[:-2])
        self.layer_factor = params[-2]
        self.uncertainty_factor = params[-1]

    def choose_move(self):
        max_move = None
        max_value = 0
        for move in self.base_board.possible_moves():
            move_board = copy.deepcopy(self.base_board)
            move_board.reset_param()

            output = self.evaluate_move(move, move_board, self.params,
                                        self.low_factor) + \
                     AdvancedHeuristicPlayer.choose_move_helper(move_board, self.params,
                                                                self.low_factor, self.layer_factor,
                                                                self.uncertainty_factor)
            if output > max_value:
                max_move = move
                max_value = output

        self.best_move = max_move
        #print 'Best move is: ' + str(self.best_move)

    @staticmethod
    def choose_move_helper(board, params, lower_factor, layer_factor, uncertainty_factor):
        if board.unknown_prec > uncertainty_factor:
            return 0

        max_value = 0
        for move in board.possible_moves():
            move_board = copy.deepcopy(board)
            move_board.reset_param()

            output = AdvancedHeuristicPlayer.evaluate_move(move, move_board, params, lower_factor) + \
                     AdvancedHeuristicPlayer.choose_move_helper(move_board, params, lower_factor, layer_factor,
                                                                uncertainty_factor)
            if output > max_value:
                max_value = output

        return layer_factor * max_value


def main():
    pass


if __name__ == '__main__':
    main()
