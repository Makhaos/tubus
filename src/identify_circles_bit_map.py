import cv2
import circle_fit as cf
from matplotlib import pyplot as plt
import numpy as np
from src import identify_pixels
from PIL import Image
import os
import time
import common.utils as utils
import src.color_detection as cd

start_time = time.time()
root = utils.get_project_root()
pos_and_radius_list = list()


class Images():
    def __init__(self, image_folder_name, res_image_folder_name):
        self.image_folder_name = image_folder_name
        self.res_image_folder_name = res_image_folder_name
    pixel_value = 20

class ScatterImages(Images):

    scatter_image_folder_name = str()
    index_array_x_black = list()
    index_array_y_black = list()

    def get_res(self, yellow_low, yellow_high):
        cd.ColorDetector(self.image_folder_name, self.res_image_folder_name).detect_yellow(yellow_low, yellow_high)

    def get_scatter_plot(self):
        scatter_image_folder_name = os.path.join(self.res_image_folder_name + 'scatter')
        ScatterImages.scatter_image_folder_name = scatter_image_folder_name
        os.makedirs(scatter_image_folder_name, exist_ok=True)
        c = 0
        for image_name, image_path in utils.folder_reader(self.res_image_folder_name):
            image_read = cv2.imread(os.path.join(image_path, image_name))
            img = Image.fromarray(image_read).convert("L")
            grayscale_image_array = np.asarray(img)
            index_array_x_yellow, index_array_y_yellow, index_array_x_black, index_array_y_black = identify_pixels.get_bright_and_dark_pixels(
                grayscale_image_array,
                Images.pixel_value)
            plt.scatter(index_array_x_black, index_array_y_black, c='red', marker=10)
            plt.savefig(os.path.join(scatter_image_folder_name, image_name))
            plt.close()
            c += 1
            print(c)

        return scatter_image_folder_name

class EdgeDetection(Images):
    contour_list = list()
    def get_edges(self):
        scatter_image_folder_name = ScatterImages.scatter_image_folder_name
        print(scatter_image_folder_name)
        for image_name, image_path in utils.folder_reader(scatter_image_folder_name):
            raw_image = cv2.imread(os.path.join(image_path, image_name))
            bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
            edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
            self.contours, _ = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def get_contours(self):
        contour_list = []
        for contour in self.contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            area = cv2.contourArea(contour)
            if len(approx) > 8 and area > 25:
                contour_list.append(contour)

        updated_contour_list = []
        for item in contour_list:
            if item.shape[0] > 30:
                updated_contour_list.append(item)
        EdgeDetection.contour_list = updated_contour_list


class CirclePosition(Images):

    index_for_most_black_pixel = int()
    def get_valid_radii(self):
        cont = EdgeDetection.contour_list
        radius_list = list()
        for item in cont:
            x_center, y_center, radius, _ = cf.least_squares_circle(item[:, 0])
            if 30 < radius < 150:
                radius_list.append([x_center, y_center, radius])
        self.position_and_radius = radius_list
        return self.position_and_radius


    ## HÄR ÄR JAG NÄR JAG GÅR HEM PÅ FREDAG
    def count_pixels_in_circle(self, black_x_position, black_y_position):
        n_black_pixels_list = list()
        for x_center, y_center, radius in self.position_and_radius:
            dist_sqrd = (black_x_position - x_center) ** 2 + (black_y_position - y_center) ** 2
            bool_array = dist_sqrd <= radius ** 2
            n_black_pixels = np.count_nonzero(bool_array == True)
            n_black_pixels_list.append(n_black_pixels)
            print('pixels', n_black_pixels)
        if not n_black_pixels_list:
            CirclePosition.index_for_most_black_pixel = False
        else:
            CirclePosition.index_for_most_black_pixel = np.argmax(n_black_pixels_list)


    def flip_orig_image(self):
        orig_image_read = cv2.imread(self)
        plt.close()
        orig_flipped = np.flipud(orig_image_read)
        return orig_flipped



image_folder_name = '/home/staffanbjorkdahl/PycharmProjects/tubus/data/frames/tempfile'
res_image_folder_name = os.path.join(str(root), 'data', 'frames', 'T20190823155414', 'res')


scatter_images = ScatterImages(image_folder_name, res_image_folder_name)
yellow_low = [14, 25, 25]
yellow_high = [30, 255, 255]
scatter_images.get_res(yellow_low, yellow_high)
scatter_images.get_scatter_plot()

edge_detection = EdgeDetection(image_folder_name, res_image_folder_name)
edge_detection.get_edges()
circle = CirclePosition(image_folder_name, res_image_folder_name)
circle.get_valid_radii()
# circle.count_pixels_in_circle()































def rgb_2_gray_scale(image_to_grayscale):
    img = Image.fromarray(image_to_grayscale).convert("L")
    arr = np.asarray(img)
    return arr


def count_pixels_in_circle(pos_and_radius, black_x, black_y):
    n_black_pixels_list = list()

    pixel = True
    for x, y, r in pos_and_radius:
        dist_sqrd = (black_x - x) ** 2 + (black_y - y) ** 2
        bool_array = dist_sqrd <= r ** 2
        n_black_pixels = np.count_nonzero(bool_array == True)
        n_black_pixels_list.append(n_black_pixels)
        print('pixels', n_black_pixels)
    if not n_black_pixels_list:
        pixel = False
        return pixel
    else:
        return np.argmax(n_black_pixels_list)


def create_grayscale_from_bitmap(image_path_name):
    image_to_grayscale = cv2.imread(image_path_name)
    arr = rgb_2_gray_scale(image_to_grayscale)
    arr = arr[70:-70, 70:-70]  # necessary??
    return arr


def save_scatter_plot_and_get_pixels(arr, pixel_value, image_path, image_name):
    index_array_x_yellow, index_array_y_yellow, index_array_x_black, index_array_y_black = identify_pixels.get_bright_and_dark_pixels(
        arr,
        pixel_value)
    os.makedirs(image_path, exist_ok=True)
    plt.close()
    plt.scatter(index_array_x_black, index_array_y_black, c='black')
    plt.scatter(index_array_x_yellow, index_array_y_yellow, c='yellow')
    plt.savefig(image_path + '/' + image_name)
    black_x = index_array_x_black
    black_y = index_array_y_black
    return black_x, black_y


def get_the_edges(image_path_name):
    print(image_path_name)
    raw_image = cv2.imread(image_path_name)
    bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
    contours, _ = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def put_contours_in_list(contours):
    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if len(approx) > 8 and area > 25:
            contour_list.append(contour)
    updated_contour_list = []
    for item in contour_list:
        if item.shape[0] > 30:
            updated_contour_list.append(item)
    return updated_contour_list


def winnow_radii(updated_contour_list):
    radius_list = list()
    for item in updated_contour_list:
        xc, yc, r, _ = cf.least_squares_circle(item[:, 0])
        if 30 < r < 150:
            radius_list.append([xc, yc, r])
    return radius_list


def flip_orig_image(input_image):
    orig_image_read = plt.imread(input_image)
    plt.close()
    orig_flipped = np.flipud(orig_image_read)
    return orig_flipped


def plot_circles_on_orig(index_most_black_pixels, pos_and_radius, input_image):
    if index_most_black_pixels is not False:
        number_of_points = np.linspace(0, 2 * np.pi, 200)
        xunit = pos_and_radius[index_most_black_pixels][2] * np.cos(number_of_points) + \
                pos_and_radius[index_most_black_pixels][0]
        yunit = pos_and_radius[index_most_black_pixels][2] * np.sin(number_of_points) + \
                pos_and_radius[index_most_black_pixels][1]
        orig_flipped = flip_orig_image(input_image)
        plt.imshow(orig_flipped)
        plt.plot(xunit, yunit)
        plt.axis('scaled')
        image_name = input_image.split('/')[-1]
        os.makedirs(str(root) + '/data/circle_folder/', exist_ok=True)
        print(str(root) + '/data/circle_folder/' + image_name)
        plt.savefig(str(root) + '/data/circle_folder/' + image_name)

        return pos_and_radius
    else:
        plt.close()

        orig_flipped = flip_orig_image(input_image)
        plt.imshow(orig_flipped)
        plt.text(300, 50, "No circle found", size=20, rotation=20.,
                 ha="center", va="center",
                 bbox=dict(boxstyle="round",
                           ec=(1., 0.5, 0.5),
                           fc=(1., 0.8, 0.8),
                           )
                 )
        image_name = input_image.split('/')[-1]
        plt.savefig(str(root) + '/data/circle_folder/' + image_name)
        print('image shape', orig_flipped.shape)
        return 0


def remove_temp_jpgs():
    os.remove(str(root) + '/data/tempPicture.jpg')
    os.remove(str(root) + '/data/tempPicture2.jpg')
    os.remove(str(root) + '/data/tempPicture3.jpg')


def get_distance_from_center_of_frame(position):
    if position == 0:
        return 350
    else:
        y_center_frame = 232
        x_center_frame = 320
        position = position[0][0:2]
        print(position)
        print(np.sqrt((y_center_frame - position[1]) ** 2 + (x_center_frame - position[0]) ** 2))
        print((480 / 2 - 237) ** 2 + (640 / 2 - 277) ** 2)
        print((np.sqrt(((480 / 2) - 277) ** 2 + ((640 / 2) - 237) ** 2)))
        return np.sqrt((y_center_frame - position[1]) ** 2 + (x_center_frame - position[0]) ** 2)


def main(images_folder, images_folder_res):
    pixel_value = 20
    pos_and_radius_list = list()
    index_of_variance_data = 0
    for image_name, image_path in utils.folder_reader(images_folder_res):
        print(image_name)
        arr = create_grayscale_from_bitmap(image_path + '/' + image_name)
        black_x, black_y = save_scatter_plot_and_get_pixels(arr, pixel_value,
                                                            str(root) + '/data/frames/res_for_circles/black_yellow',
                                                            image_name)  # TODO Dirty solution
        contours = get_the_edges(str(root) + '/data/frames/res_for_circles/black_yellow/' + image_name)
        updated_contour_list = put_contours_in_list(contours)
        pos_and_radius = winnow_radii(updated_contour_list)
        index_most_black_pixels = count_pixels_in_circle(pos_and_radius, black_x, black_y)
        position = plot_circles_on_orig(index_most_black_pixels, pos_and_radius, images_folder + '/' + image_name)

        distance_from_center = get_distance_from_center_of_frame(position)
        pos_and_radius_list.append(position)
        index_of_variance_data = index_of_variance_data + 1
        identify_pixels.write_plot_data_2_csv(distance_from_center, images_folder, index_of_variance_data)
        plt.close()

# main(image_folder_name,res_image_folder_name)
