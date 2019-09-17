import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

indexArray_x = list()
indexArray_y = list()
indexArray_x_black = list()
indexArray_y_black = list()


def rgb2GrayScale(imageFile):
    img = Image.open(imageFile).convert("L")
    arr = np.asarray(img)
    return arr


def getLightPixelsRatio(arr):
    totalNumberOfPixels = np.size(arr)
    countLightPixels = 0
    for n, i in enumerate(arr):  # numberOfRows
        for n1, j in enumerate(i):  # numberOfCols
            if j > 20:
                countLightPixels += 1
                indexArray_x.append([n])
                indexArray_y.append([n1])
            else:
                indexArray_x_black.append([n])
                indexArray_y_black.append([n1])
    return countLightPixels / totalNumberOfPixels, indexArray_x, indexArray_y, indexArray_x_black, indexArray_y_black


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



def main(imageFile):
    arr = rgb2GrayScale(imageFile)
    arr = arr[:, 50:][:, :-50]
    ratio, indexArray_x, indexArray_y, indexArray_x_black, indexArray_y_black = getLightPixelsRatio(arr)
    plotPixels(indexArray_x_black, indexArray_y_black, indexArray_x, indexArray_y, imageFile)


if __name__ == '__main__':
    main()
