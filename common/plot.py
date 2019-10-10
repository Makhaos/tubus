import matplotlib.pyplot as plt
import numpy as np
import common.utils as utils
import os


def plot_list(l, video_name, plot_name):
    root = utils.get_project_root()
    plt.figure()
    x = np.arange(0, len(l), 1)
    plt.xticks(np.arange(0, len(l), step=2))
    plt.plot(x, l, color='green', linestyle='dashed', linewidth=3,
             marker='o', markerfacecolor='blue', markersize=8)
    for x, y in zip(x, l):
        plt.text(x, y, str(x), color="red", fontsize=6)
    plt.grid()
    os.makedirs(os.path.join(str(root), 'data', 'files', video_name), exist_ok=True)
    plt.savefig(os.path.join(str(root), 'data', 'files', video_name, plot_name + '.png'))
