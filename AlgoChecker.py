from heuristic_player import HeuristicPlayer
import Board

class AlgoChecker:
    @staticmethod
    def checkHeuristic(list_of_hueristics_tuples):
        pass
        board = Board.Board()
        board.print_board()
        for heuristic_tuple in list_of_hueristics_tuples:
            heuristic_player = HeuristicPlayer(heuristic_tuple)
            results_data = board.play_game_with_random(heuristic_player,True)
