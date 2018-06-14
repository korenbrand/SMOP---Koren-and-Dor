import numpy as np
import matplotlib.pyplot as plt


TYPE = 0
SCORE_H = 1
STRIPE_H = 2
WRAP_H = 3
CHOC_H = 4
SWIPE_H = 5
SCORE = 6
STRIPE_C = 7
WRAP_C = 8
CHOc_C = 9
LAYER_H = 6
UNCERTAINTY_H = 7
ADVANCE_SCORE = 8
ADVANCE_STRIPE_C = 9
ADVANCE_WRAP_C = 10
ADVANCE_CHOC_C = 11


def read_file(path):
    with open(path, 'r') as file:
        types = []
        score_h = []
        stripe_h = []
        wrap_h = []
        choc_h = []
        swipe_h = []
        layer_h = []
        uncertainty_h = []
        avg_score = []
        stripe_c = []
        wrap_c = []
        choc_c = []

        for line in file:
            chunks = line.split('#')
            types.append(chunks[0])

            weights = chunks[1].split(',')
            score_h.append(weights[0])
            stripe_h.append(weights[1])
            wrap_h.append(weights[2])
            choc_h.append(weights[3])
            swipe_h.append(weights[4])

            if len(weights) == 7:
                layer_h.append(weights[5])
                uncertainty_h.append(weights[6])

            results = chunks[2].split(',')
            avg_score.append(results[0])
            stripe_c.append(results[1])
            wrap_c.append(results[2])
            choc_c.append(results[3][:-1])
        if len(weights) == 7:
            return np.array([types, score_h, stripe_h, wrap_h, choc_h, swipe_h, layer_h, uncertainty_h, avg_score,
                             stripe_c, wrap_c, choc_c])

        return np.array([types, score_h, stripe_h, wrap_h, choc_h, avg_score, stripe_c, wrap_c, choc_c])


out_dir = 'C:\\Users\\Koren\\Documents\\SMOP\\'
data = read_file(out_dir + 'test night 1.txt')


def plot(x, y, title, xlab, ylab='Avg. score per turn', chart_style=None, resolution=500):
    x = np.array([float(x2) for x2 in x])
    y = np.array([float(y2) for y2 in y])

    y = y[x.argsort()]
    x.sort()

    max_index = y.argmax()
    print 'Max: ' +str((x[max_index], y[max_index]))

    plt.figure(dpi=500)

    if chart_style:
        plt.plot(x, y, chart_style)
    else:
        plt.plot(x, y)

    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.show()


data = read_file(out_dir + 'Advance swipe test.txt')
plot(data[SWIPE_H], data[ADVANCE_SCORE], "Avg. score vs. swipe heuristic's weight", xlab='Swipe heuristic value')