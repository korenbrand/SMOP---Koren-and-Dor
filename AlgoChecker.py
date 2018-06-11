from heuristic_player import HeuristicPlayer
import Board


class AlgoChecker:
    @staticmethod
    def checkHeuristic(list_of_hueristics_tuples,num_of_runs):
        pass
        board = Board.Board()
        board.print_board()
        for heuristic_tuple in list_of_hueristics_tuples:
            heuristic_player = HeuristicPlayer(heuristic_tuple)
            results_data = board.play_game_with_random(heuristic_player, num_of_runs=num_of_runs, detailed=True)
            results_file = open("C:/Users/t8374100/Desktop/results for different hurestics" + "/" + str(heuristic_tuple), "w")
            results_file.write(str(*results_data))


player = HeuristicPlayer((0, 0, 0, 1, 0, 0))
board = Board.Board()
board.print_board()
board.play_game_with_random(player,num_of_runs=1000)
