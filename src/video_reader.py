import os
import sys


def videos_reader(folder_path):
    videos_list = []
    root_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            with open(os.path.join(root, file), "r") as auto:
                root_list.append(root)
                videos_list.append(file)
    return videos_list, root_list
