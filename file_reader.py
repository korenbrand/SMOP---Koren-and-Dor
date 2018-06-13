import numpy as np
import matplotlib.pyplot as plt


TYPE = 0
SCORE_H = 1
STRIPE_H = 2
WRAP_H = 3
CHOC_H = 4
SCORE = 5

def read_file(path):
    with open(path, 'r') as file:
        types = []
        score_h = []
        stripe_h = []
        wrap_h = []
        choc_h = []
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

            results = chunks[2].split(',')
            avg_score.append(results[0])
            stripe_c.append(results[1])
            wrap_c.append(results[2])
            choc_c.append(results[3][:-1])

        return np.array([types, score_h, stripe_h, wrap_h, choc_h, avg_score, stripe_c, wrap_c, choc_c])


out_dir = 'C:\\Users\\Koren\\Documents\\SMOP\\'
data = read_file(out_dir + 'test night 1.txt')

plt.plot(data[STRIPE_H], data[SCORE], '.', label='Stripe')
plt.plot(data[WRAP_H], data[SCORE], '.', label='Wrap')
plt.plot(data[CHOC_H], data[SCORE], '.', label='Chocolate')

plt.show()


def plot(x, y, title, xlab, ylab='Avg. score per turn', type=None):
    x = np.array([float(x2) for x2 in x])
    y = np.array([float(y2) for y2 in y])

    y = y[x.argsort()]
    x.sort()

    if type:
        plt.plot(x, y, type)
    else:
        plt.plot(x, y)
        
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.show()