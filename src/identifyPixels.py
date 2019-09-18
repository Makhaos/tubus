import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

indexArray_x = list()
indexArray_y = list()
indexArray_x_black = list()
indexArray_y_black = list()


def rgb2GrayScale(imageFile):
    #img = Image.open(imageFile).convert("L")
    img = Image.fromarray(imageFile)
    arr = np.asarray(img)
    return arr


def getLightPixelsRatio(arr, pixelValue):
    indiciesBright = np.where(arr >= pixelValue)
    indexArray_x = indiciesBright[1]
    indexArray_y = indiciesBright[0]
    indiciesDark = np.where(arr < pixelValue)
    indexArray_x_black = indiciesDark[1]
    indexArray_y_black = indiciesDark[0]
    return indexArray_x, indexArray_y, indexArray_x_black, indexArray_y_black


def calculateSpread(indexArray_y_black, indexArray_x_black):
    variance_y = np.var(indexArray_y_black)
    variance_x = np.var(indexArray_x_black)
    print('varX: ' + str(int(np.round(variance_y))) + ', varY: ' + str(int(np.round(variance_x))))
    return int(np.round(variance_x)), int(np.round(variance_y))


def plotPixels(indexArray_x_black, indexArray_y_black, indexArray_x, indexArray_y, imageFile):
    plt.scatter(indexArray_y, indexArray_x, c='yellow', s=0.1)
    plt.scatter(indexArray_y_black, indexArray_x_black, c='black', s=0.1)
    variance_x, variance_y = calculateSpread(indexArray_y_black, indexArray_x_black)
    string = 'varX: ' + str(variance_y) + ' ' + 'varY: ' + str(variance_x)
    plt.text(-50, 700, string, fontsize=8)
    plt.text(-50, -100, imageFile.split('/')[-1], fontsize=8)
    plt.show()


def main(res):
    arr = rgb2GrayScale(res)
    arr = arr[:, 50:][:, :-50]
    indexArray_x, indexArray_y, indexArray_x_black, indexArray_y_black = getLightPixelsRatio(arr, 40)
    # plotPixels(indexArray_x_black, indexArray_y_black, indexArray_x, indexArray_y, imageFile)
    variance_x, variance_y = calculateSpread(indexArray_y_black, indexArray_x_black)
    return variance_x, variance_x


if __name__ == '__main__':
    main()
