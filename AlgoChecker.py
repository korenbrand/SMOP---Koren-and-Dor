from heuristic_player import HeuristicPlayer, AdvancedHeuristicPlayer
import Board
import numpy as np
<<<<<<< HEAD
=======

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
>>>>>>> bla-branch


class AlgoChecker:
    @staticmethod
    #    @timelimit(266)
    def check_heuristic(list_of_hueristics_tuples, num_of_runs, is_advanced, filename):
        pass
<<<<<<< HEAD
        board = Board.Board()
        # board.print_board()
        with open(filename + ".txt", "a") as results_file:
            # the name of the file is the name of the first heuristics tuple
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
                for heuristica in heuristic_tuple:
                    results_file.write("," + str(heuristica))
                results_file.write("#")
                results_file.write(str(results_data[0]))
                for result in results_data[1:]:
                    results_file.write("," + str(result))
                results_file.write("\n")


output_dir = "C:\\Users\\Koren\\Documents\\SMOP\\"

for x in np.arange(0, 2.01, 0.05):
    print "value: " + str(x)
    AlgoChecker.checkHeuristic([(0.01, 1, 2, 3, 0)], 2500, False, output_dir + "check score calibration")
=======
        board = Board.Board(height=9, width=9)
        # board.print_board()
        for heuristic_tuple in list_of_hueristics_tuples:
            if not is_advanced:
                heuristic_player = HeuristicPlayer(heuristic_tuple)
            else:
                heuristic_player = AdvancedHeuristicPlayer(heuristic_tuple)
            results_data = board.play_game_with_random(heuristic_player, num_of_runs=num_of_runs, detailed=False)

        with open(filename + ".txt", "a") as results_file:
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


# for i in range(10,110,10) :
#    a = open("C:/Users/t8374100/Desktop/results for different hurestics/convergence2.txt", "a")
#    a.write(str(i) + ": ")
#    a.close()
#    AlgoChecker.check_heuristic([(1, 2, 3, 4, 1)], i, False, "convergence2")
# for i in range(100,1100,100) :
#    a = open("C:/Users/t8374100/Desktop/results for different hurestics/convergence2.txt", "a")
#    a.write(str(i) + ": ")
#    a.close()
#    AlgoChecker.check_heuristic([(1, 2, 3, 4, 1)], i, False, "convergence2")
# for i in range (4000, 5500, 500):
#    a = open("C:/Users/t8374100/Desktop/results for different hurestics/convergence2.txt", "a")
#    a.write(str(i) + ": ")
#    a.close()
"""
AlgoChecker.check_heuristic([(0,0,0,0,0)],2500, False,"[0,0,0,0,0]")
for i in range(1, 7, 1):
    for j in range(1, 7, 1):
        for k in range(1, 7, 1):
            try:
                AlgoChecker.check_heuristic([(0.01, i, j, k, 0)], 2500, False, "checker")
                break
            except:
                print ("timeout")
                continue


for a in range (2):
    for b in range(2):
        for c in range(2):
            for d in range (2):
                for e in range(2):
                    AlgoChecker.check_heuristic([(a, b, c, d, e)], 2500, False, "BinaryCheck")
"""

output_dir = r"C:/Users/Koren/Documents/SMOP/"
test_night_one_stop = (1, 2.5, 8.5, 7, 0)
for x in np.arange(-3, 5, 0.5):
            start = time.time()
            test_name = "Stripe variance check"
            print test_name
            AlgoChecker.check_heuristic([(1, 3 + x, 7, 7, 0)], 2500, False, output_dir + test_name)
            end = time.time()
            print 'time: ' + str(end - start)

for x in np.arange(-5, 5, 0.5):
            start = time.time()
            test_name = "Wrap variance check"
            print test_name
            AlgoChecker.check_heuristic([(1, 3, 7 + x, 7, 0)], 2500, False, output_dir + test_name)
            end = time.time()
            print 'time: ' + str(end - start)

for x in np.arange(-5, 5, 0.5):
            start = time.time()
            test_name = "Chocolate variance check"
            print test_name
            AlgoChecker.check_heuristic([(1, 3, 7, 7 + x, 0)], 2500, False, output_dir + test_name)
            end = time.time()
            print 'time: ' + str(end - start)
>>>>>>> bla-branch
