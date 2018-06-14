import numpy as np
import matplotlib.pyplot as plt


TYPE = 0
SCORE_H = 1
STRIPE_H = 2
WRAP_H = 3
CHOC_H = 4
SWIPE_H = 5
SCORE = 6

# advanced params
ADVANCED_SCORE = 8


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
            return np.array([types, score_h, stripe_h, wrap_h, choc_h, swipe_h, layer_h, uncertainty_h, avg_score, stripe_c, wrap_c, choc_c])

        return np.array([types, score_h, stripe_h, wrap_h, choc_h, swipe_h, layer_h, uncertainty_h, avg_score, stripe_c, wrap_c, choc_c])


out_dir = 'C:\\Users\\Koren\\Documents\\SMOP\\'
data = read_file("C:/Users/t8374100/Desktop/results for different hurestics/now_for_real.txt")

plt.plot(data[STRIPE_H], data[SCORE], '.', label='Stripe')
plt.plot(data[WRAP_H], data[SCORE], '.', label='Wrap')
plt.plot(data[CHOC_H], data[SCORE], '.', label='Chocolate')

plt.show()