from pathlib import Path
import re
import os
import numpy as np
from PIL import Image

ALLOWED_EXTENSIONS = {'.avi', '.mov', '.flv', '.mp4', '.AVI'}


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent


def folder_reader(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in sorted(files, key=natural_keys):
            with open(os.path.join(root, file), "r") as auto:
                yield file, root


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    """
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def rgb_2_gray_scale(image_file):
    img = Image.open(image_file).convert("L")
    arr = np.asarray(img)
    return arr


def progress_bar_subroutine(data, total):
    dict_of_percentages = {}
    blur_percentage = 0
    no_blur_percentage = 0
    counter = 0
    if data[str(0)] == 'blur':
        blur_bool = True
    else:
        blur_bool = False
    for index in range(total):
        if data[str(index)] == 'blur':
            blur_percentage = blur_percentage + 100 / total
            if not blur_bool:
                dict_of_percentages[str(counter)] = {str(round(no_blur_percentage)): 'no_blur'}
                no_blur_percentage = 0
                counter += 1
            blur_bool = 'blur'
        if data[str(index)] == 'no_blur':
            no_blur_percentage = no_blur_percentage + 100 / total
            if blur_bool:
                dict_of_percentages[str(counter)] = {str(round(blur_percentage)): 'blur'}
                blur_percentage = 0
                counter += 1
            blur_bool = False
        if index == total - 1:
            if blur_bool:
                dict_of_percentages[str(counter)] = {str(round(blur_percentage)): 'blur'}
            if not blur_bool:
                dict_of_percentages[str(counter)] = {str(round(no_blur_percentage)): 'no_blur'}
    return dict_of_percentages
