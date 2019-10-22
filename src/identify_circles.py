import cv2
import circle_fit as cf
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import os
import common.utils as utils
import src.color_detection as cd
root = utils.get_project_root()


class Images:
    def __init__(self, video_name):
        self.res_image_folder_name = os.path.join(str(root), 'data','frames', video_name, 'res')
        self.image_folder_name = os.path.join(str(root), 'data', 'frames',video_name, 'raw')
        self.scatter_image_folder_name = os.path.join(str(root), 'data', 'frames', video_name, 'scatter')
        self.circle_image_folder_name = os.path.join(str(root), 'data', 'frames', video_name, 'circles')
    pixel_value = 20


class ScatterImages(Images):
    scatter_image_folder_name = str()
    black_pixels_position = list()

    @staticmethod
    def get_bright_and_dark_pixels(grayscale_image_array, pixel_value):  # Returns the bright and the dark pixels
        indices_bright = np.where(grayscale_image_array >= pixel_value)
        index_array_x = indices_bright[1]
        index_array_y = indices_bright[0]
        indices_dark = np.where(grayscale_image_array < pixel_value)
        index_array_x_black = indices_dark[1]
        index_array_y_black = indices_dark[0]
        return index_array_x, index_array_y, index_array_x_black, index_array_y_black

    def get_res(self, yellow_low, yellow_high):  # Creates images with bitmap and writes them to res folder
        yellow_low_str = '_'.join([str(i) for i in yellow_low])
        yellow_high_str = '_'.join([str(i) for i in yellow_high])
        res_folder_name = os.path.join(self.res_image_folder_name+yellow_low_str+'__' + yellow_high_str)
        cd.ColorDetector(self.image_folder_name, res_folder_name).detect_yellow(yellow_low, yellow_high)

    def get_scatter_plot(self):  # Plots scatter plots and writes them to scatter folder
        os.makedirs(self.scatter_image_folder_name, exist_ok=True)
        image_number = 0
        for image_name, image_path in utils.folder_reader(self.res_image_folder_name):
            image_read = cv2.imread(os.path.join(image_path, image_name))
            img = Image.fromarray(image_read).convert("L")
            grayscale_image_array = np.asarray(img)
            index_array_x_yellow, index_array_y_yellow, black_x_position, black_y_position = \
                ScatterImages.get_bright_and_dark_pixels(grayscale_image_array, Images.pixel_value)
            plt.imshow(image_read)
            plt.scatter(black_x_position, black_y_position, c='black')
            plt.savefig(os.path.join(self.scatter_image_folder_name, image_name))
            plt.close()
            ScatterImages.black_pixels_position.append([image_number, black_x_position, black_y_position])
            print('Image number: ', image_number)
            image_number += 1


class EdgeDetection(Images):
    list_of_contour_lists = list()
    contours = list()
    total_contour_list = list()
    updated_contour_list = list()

    def get_edges(self): # Identifies the edges in the image
        contour_list = list()
        scatter_image_folder_name = self.scatter_image_folder_name
        os.makedirs(scatter_image_folder_name, exist_ok=True)
        EdgeDetection.total_contour_list = list()
        for image_name, image_path in utils.folder_reader(scatter_image_folder_name):
            raw_image = cv2.imread(os.path.join(image_path, image_name))
            bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
            edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
            contours, _ = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
                area = cv2.contourArea(contour)
                if len(approx) > 8 and area > 25:
                    contour_list.append(contour)
            updated_contour_list = list()
            for item in contour_list:
                if item.shape[0] > 30:
                    updated_contour_list.append(item)
            EdgeDetection.total_contour_list.append(updated_contour_list)
            contour_list = list()


class CirclePosition(Images):
    features_selected_circle = list()
    circle_features = list()
    image_number_and_argmax = list()

    def get_valid_radii(self):  # Creates circles from contours and accepts a certain interval for circles radius
        cont = EdgeDetection.total_contour_list
        valid_circles_list_total = list()
        valid_circles_list = list()

        for image_number, image in enumerate(cont):
            for contours in image:
                x_center, y_center, radius, _ = cf.least_squares_circle(contours[:, 0])
                if 30 < radius < 200:
                    valid_circles_list.append([image_number, x_center, y_center, radius])
            valid_circles_list_total.append(valid_circles_list)
            valid_circles_list = list()
            CirclePosition.circle_features = valid_circles_list_total

    def count_pixels_in_circle(self):  # Counts the black pixels within each valid circle
        n_black_pixels_list = list()
        index_for_most_black_pixel = list()
        for item in CirclePosition.circle_features:
            for image_number, x_center, y_center, radius in item:
                distance = np.sqrt((ScatterImages.black_pixels_position[image_number][1] - x_center) ** 2 + (
                        ScatterImages.black_pixels_position[image_number][2] - y_center) ** 2)
                bool_array = distance <= radius
                n_black_pixels = np.count_nonzero(bool_array == True)
                n_black_pixels_list.append(n_black_pixels)
                if not n_black_pixels_list:
                    index_for_most_black_pixel = [image_number, False]
                else:
                    index_for_most_black_pixel = [image_number, np.argmax(n_black_pixels_list)]
            n_black_pixels_list = list()
            CirclePosition.image_number_and_argmax.append(index_for_most_black_pixel)
        for image_number_and_idx, features in zip(CirclePosition.image_number_and_argmax[1:],
                                                  CirclePosition.circle_features[1:]):
            if not features:
                CirclePosition.features_selected_circle.append([image_number_and_idx[0], False])
            else:
                CirclePosition.features_selected_circle.append(features[image_number_and_idx[1]])
        CirclePosition.image_number_and_argmax = list()
        CirclePosition.circle_features = list()

    def plot_circles_on_raw_image(self):  # Plots the circle on the raw image
        xunit = list()
        yunit = list()
        found_circle = True
        os.makedirs(self.circle_image_folder_name, exist_ok=True)
        image_count = -1
        for image_name, image_path in utils.folder_reader(self.image_folder_name):
            image_count += 1
            image_read = plt.imread(os.path.join(image_path, image_name))
            for item in CirclePosition.features_selected_circle:
                if item[0] == image_count:
                    if item[1]:
                        number_of_points = np.linspace(0, 2 * np.pi, 200)
                        xunit = item[3] * np.cos(number_of_points) + item[1]
                        yunit = item[3] * np.sin(number_of_points) + item[2]
                    else:
                        found_circle = False
            if not found_circle:
                plt.imshow(image_read)
                plt.text(50, 50, 'No Circle Found')
                plt.savefig(os.path.join(self.circle_image_folder_name, image_name))
            else:
                plt.imshow(image_read)
                plt.plot(xunit, yunit)
                plt.savefig(os.path.join(self.circle_image_folder_name, image_name))
            plt.close()
            found_circle = True



def main():
    video_name = 'T20190823155414'
    yellow_low = [14, 25, 25]
    yellow_high = [30, 255, 255]
    scatter_images = ScatterImages(video_name)
    scatter_images.get_res(yellow_low, yellow_high)
    scatter_images.get_scatter_plot()
    edge_detection = EdgeDetection(video_name)
    edge_detection.get_edges()
    circle_pos = CirclePosition(video_name)
    circle_pos.get_valid_radii()
    circle_pos.count_pixels_in_circle()
    circle_pos.plot_circles_on_raw_image()


if __name__ == '__main__':
    main()