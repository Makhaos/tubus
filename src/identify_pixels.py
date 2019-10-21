import numpy as np
from PIL import Image
import math
import os
import common.utils as utils
import sys
import warnings
root = utils.get_project_root()


class Variance:
    def __init__(self, image):
        self.image = image
        self.video_directory = os.path.split(os.path.split(image)[0])[0]
    pixel_value = 20
    variance = 0

    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    def create_rgb_from_grayscale(self):
        grayscale_image = Image.open(self.image).convert("L")
        grayscale_array = np.asarray(grayscale_image)
        self.grayscale_array = grayscale_array[:, 50:][:, :-50]

    def get_bright_and_dark_pixels(self):
        indices_dark = np.where(self.grayscale_array < Variance.pixel_value)
        self.index_array_x_black = indices_dark[1]
        self.index_array_y_black = indices_dark[0]

    def calculate_variance(self):
        variance_y = np.var(self.index_array_x_black)
        variance_x = np.var(self.index_array_y_black)
        if math.isnan(variance_y):
            variance_y = 0
        if math.isnan(variance_x):
            variance_x = 0
        Variance.variance = int(np.round(variance_x)) + int(np.round(variance_y))


class WritingCSV(Variance):

    def write_plot_data_2_csv(self, index_of_variance):
        complete_name = os.path.join(self.video_directory, 'variance.csv')
        if index_of_variance == 1:
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
                fout.write(str(index_of_variance) + ',' + str(Variance.variance) + '\n')

        else:
            with open(complete_name, 'a') as fout:
                fout.write(str(index_of_variance) + ',' + str(Variance.variance) + '\n')


def main():
    video_name = 'T20190823155414'
    raw_image_folder_name = os.path.join(str(root), 'data', video_name, 'raw')
    variance_index = 0
    for image_name, image_directory in utils.folder_reader(raw_image_folder_name):
        variance_index += 1
        image_name_path = os.path.join(image_directory, image_name)
        variance_image = Variance(image_name_path)
        variance_image.create_rgb_from_grayscale()
        variance_image.get_bright_and_dark_pixels()
        variance_image.calculate_variance()
        csv = WritingCSV(image_name_path)
        csv.write_plot_data_2_csv(variance_index)


if __name__ == "__main__":
    main()



