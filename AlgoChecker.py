from heuristic_player import HeuristicPlayer, AdvancedHeuristicPlayer
import Board


class AlgoChecker:
    @staticmethod
    def checkHeuristic(list_of_hueristics_tuples, num_of_runs, is_advanced, filename):
        pass
        board = Board.Board()
        board.print_board()
        results_file = open("C:/Users/t8374100/Desktop/results for different hurestics" + "/" + filename + ".txt", "a")  # the name of the file is the name of the first heuristics tuple
        for heuristic_tuple in list_of_hueristics_tuples:
            if not is_advanced:
                heuristic_player = HeuristicPlayer(heuristic_tuple)
            else:
                heuristic_player = AdvancedHeuristicPlayer(heuristic_tuple)
            results_data = board.play_game_with_random(heuristic_player, num_of_runs=num_of_runs, detailed=False)
            if not is_advanced:
                results_file.write("S#")
            else:
                results_file.write("H#")
            results_file.write(str(heuristic_tuple[0]))
            for heuristica in heuristic_tuple[1:]:
                results_file.write("," + str(heuristica))
            results_file.write("#")
            results_file.write(str(results_data[0]))
            for result in results_data[1:]:
                results_file.write("," +str(result))
            results_file.write("\n")



AlgoChecker.checkHeuristic([(1, 1, 1, 1, 1)], 1000, False, "check")
AlgoChecker.checkHeuristic([(1, 1, 1, 1, 1)], 1500, False, "check")
AlgoChecker.checkHeuristic([(1, 1, 1, 1, 1)], 2000, False, "check")
AlgoChecker.checkHeuristic([(1, 1, 1, 1, 1)], 2500, False, "check")
AlgoChecker.checkHeuristic([(1, 1, 1, 1, 1)], 3000, False, "check")