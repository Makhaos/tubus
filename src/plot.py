import matplotlib.pyplot as plt
import numpy as np


def plot_list(l):
    plt.figure()
    y = l
    x = np.arange(0, len(l), 1)
    plt.xticks(np.arange(0, len(l), step=2))

    plt.plot(x, y, color='green', linestyle='dashed', linewidth=3,
             marker='o', markerfacecolor='blue', markersize=8)
    for x, y in zip(x, y):
        plt.text(x, y, str(x), color="red", fontsize=6)
    plt.grid()
    plt.show()
