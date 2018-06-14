from heuristic_player import HeuristicPlayer, AdvancedHeuristicPlayer
import Board
import numpy as np
import threading
import sys
import time


class TimeoutError(Exception): pass


def timelimit(timeout):
    def internal(function):
        def internal2(*args, **kw):
            class Calculator(threading.Thread):
                def __init__(self):
                    threading.Thread.__init__(self)
                    self.result = None
                    self.error = None

                def run(self):
                    try:
                        self.result = function(*args, **kw)
                    except:
                        self.error = sys.exc_info()[0]

            c = Calculator()
            c.start()
            c.join(timeout)
            if c.isAlive():
                raise TimeoutError
            if c.error:
                raise c.error
            return c.result

        return internal2

    return internal


class AlgoChecker:
    @staticmethod
    def check_heuristic(list_of_hueristics_tuples, num_of_runs, is_advanced, filename):
        board = Board.Board(height=9, width=9)
        # board.print_board()
        results_file = open("C:/Users/t8374100/Desktop/results for different hurestics/" + filename + ".txt", "a")
        for heuristic_tuple in list_of_hueristics_tuples:
            if not is_advanced:
                heuristic_player = HeuristicPlayer(heuristic_tuple)
            else:
                heuristic_player = AdvancedHeuristicPlayer(heuristic_tuple)

            results_data = board.play_game_with_random(heuristic_player, num_of_runs=num_of_runs, detailed=False)


            # the name of the file is the name of the first heuristics tuple
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
                results_file.write("," + str(result))
            results_file.write("\n")



for t in range(9):
    for y in np.arange(0,1,0.1):
        AlgoChecker.check_heuristic([(0.2,3,7,9,t,y,0.5)],1000,True,"now_for_real")

