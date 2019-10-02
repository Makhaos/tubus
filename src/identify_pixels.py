import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import utils
import csv
import math
import sys

indexArray_x = list()
indexArray_y = list()
indexArray_x_black = list()
indexArray_y_black = list()


def rgb_2_gray_scale(imageFile):
    img = Image.open(imageFile).convert("L")
    arr = np.asarray(img)
    return arr


def get_bright_and_dark_pixels(arr, pixelValue):
    indiciesBright = np.where(arr >= pixelValue)
    indexArray_x = indiciesBright[1]
    indexArray_y = indiciesBright[0]
    indiciesDark = np.where(arr < pixelValue)
    indexArray_x_black = indiciesDark[1]
    indexArray_y_black = indiciesDark[0]
    return indexArray_x, indexArray_y, indexArray_x_black, indexArray_y_black


def calculate_spread(indexArray_y_black, indexArray_x_black):
    variance_y = np.var(indexArray_x_black)
    variance_x = np.var(indexArray_y_black)
    if math.isnan(variance_y):
        variance_y = 0
    if math.isnan(variance_x):
        variance_x = 0
    print('varX: ' + str(int(np.round(variance_y))) + ', varY: ' + str(int(np.round(variance_x))))
    return int(np.round(variance_x)), int(np.round(variance_y))


def plot_pixels(indexArray_x_black, indexArray_y_black, indexArray_x, indexArray_y, imageFile):
    plt.scatter(indexArray_y, indexArray_x, c='yellow', s=0.1)
    plt.scatter(indexArray_y_black, indexArray_x_black, c='black', s=0.1)
    variance_x, variance_y = calculate_spread(indexArray_y_black, indexArray_x_black)
    string = 'varX: ' + str(variance_y) + ' ' + 'varY: ' + str(variance_x)
    plt.text(-50, 700, string, fontsize=8)
    plt.text(-50, -100, imageFile.split('/')[-1], fontsize=8)
    plt.show()


def write_plot_data_2_csv(variance, images_folder, index_of_variance_data):
    complete_name = images_folder.split('/')[-1] + '.csv'
    if index_of_variance_data == 1:
        with open(complete_name, 'w') as fout1:
            fout1.write('x,y \n')
            fout1.write(str(-6) + ',' + str(0) + '\n')
            fout1.write(str(-5) + ',' + str(0) + '\n')
            fout1.write(str(-4) + ',' + str(0) + '\n')
            fout1.write(str(-3) + ',' + str(0) + '\n')
            fout1.write(str(-2) + ',' + str(0) + '\n')
            fout1.write(str(-1) + ',' + str(0) + '\n')
            fout1.write(str(0) + ',' + str(0) + '\n')
        with open(complete_name, 'a') as fout:
            fout.write(str(index_of_variance_data) + ',' + str(variance) + '\n')
            print(index_of_variance_data)
    else:
        with open(complete_name, 'a') as fout:
            fout.write(str(index_of_variance_data) + ',' + str(variance) + '\n')
            print(index_of_variance_data)


def main(images_folder):
    variance_list = []
    index_of_variance_data = 0
    for image_name, image_path in utils.folder_reader(images_folder):
        print(image_name)
        index_of_variance_data = index_of_variance_data + 1
        arr = rgb_2_gray_scale(image_path + '/' + image_name)
        arr = arr[:, 50:][:, :-50]
        indexArray_x, indexArray_y, indexArray_x_black, indexArray_y_black = get_bright_and_dark_pixels(arr, 40)
        # plot_pixels(indexArray_x_black, indexArray_y_black, indexArray_x, indexArray_y, imageFile)
        variance_x, variance_y = calculate_spread(indexArray_y_black, indexArray_x_black)
        variance = variance_x + variance_y
        write_plot_data_2_csv(variance, images_folder, index_of_variance_data)
        variance_list.append(variance)

    return variance_list
