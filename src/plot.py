import matplotlib.pyplot as plt
import numpy as np
import utils
import os


def plot_list(l, video_name):
    root = utils.get_project_root()
    plt.figure()
    y = l
    x = np.arange(0, len(l), 1)
    plt.xticks(np.arange(0, len(l), step=2))
    plt.plot(x, y, color='green', linestyle='dashed', linewidth=3,
             marker='o', markerfacecolor='blue', markersize=8)
    for x, y in zip(x, y):
        plt.text(x, y, str(x), color="red", fontsize=6)
    plt.grid()
    os.makedirs(str(root) + '/data/files', exist_ok=True)
    plt.savefig(str(root) + '/data/files/' + video_name + '.png')
