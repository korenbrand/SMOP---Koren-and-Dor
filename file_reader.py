import numpy as np
import matplotlib.pyplot as plt


TYPE = 0
SCORE_H = 1
STRIPE_H = 2
WRAP_H = 3
CHOC_H = 4
SCORE = 5


def plot(x, y, title, xlab='Heuristic', ylab='Avg. score per turn', type=None):
    y = np.array([float(line[1]) for line in y])
    print y
    y.sort()
    x.sort()
    if type:
        plt.plot(x, y, type)
    else:
        plt.plot(x,y)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.show()


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
            score_h.append(float(weights[0]))
            stripe_h.append(float(weights[1]))
            wrap_h.append(float(weights[2]))
            choc_h.append(float(weights[3]))

            results = chunks[2].split(',')
            avg_score.append(float(results[0]))
            stripe_c.append(float(results[1]))
            wrap_c.append(float(results[2]))
            choc_c.append(float(results[3]))

        return np.array([types, score_h, stripe_h, wrap_h, choc_h, avg_score, stripe_c, wrap_c, choc_c])


out_dir = 'C:\\Users\\Koren\\Documents\\SMOP\\'
data = read_file(out_dir + 'Stripe variance check.txt')
print(data[SCORE])
plot(x=data[STRIPE_H], y=data[SCORE], title="Stripe's weight vs Avg. score", xlab='Stripe weight value')
data = read_file(out_dir + 'Wrap variance check.txt')
plot(data[WRAP_H], data[SCORE], "Wrap's weight vs Avg. score", 'Stripe weight value')
data = read_file(out_dir + 'Chocolate variance check.txt')
plot(data[CHOC_H], data[SCORE], "Chocolate's weight vs Avg. score", 'Stripe weight value')
