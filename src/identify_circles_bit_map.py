import cv2
import circle_fit as cf
from matplotlib import pyplot as plt
import numpy as np
from src import identify_pixels
from PIL import Image
import os
import time
import sys
import utils


start_time = time.time()
root = utils.get_project_root()


def yellow_detection(input_image):
    image_read = cv2.imread(input_image)
    hsv = cv2.cvtColor(image_read, cv2.COLOR_BGR2HSV)
    yellow_lower = np.array([16, 25, 0], np.uint8)
    yellow_upper = np.array([30, 255, 255], np.uint8)
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    res = cv2.bitwise_and(src1=image_read, src2=image_read, mask=yellow)
    plt.imshow(res)
    plt.savefig(str(root) + '/data/tempPicture.jpg')



def rgb_2_gray_scale(image_to_grayscale):
    print(type(image_to_grayscale))
    img = Image.fromarray(image_to_grayscale).convert("L")
    arr = np.asarray(img)
    return arr

def count_pixels_in_circle(pos_and_radius,black_x, black_y, pixel_value):
    n_black_pixels_list = list()
    black_pixels_pos = np.c_[black_x,black_y]
    print(black_pixels_pos.shape)
    for x, y, r in pos_and_radius:
        dist_sqrd = (black_x-x)**2 + (black_y-y)**2
        bool_array = dist_sqrd <= r**2
        n_black_pixels = np.count_nonzero(bool_array == True)
        n_black_pixels_list.append(n_black_pixels)
    return np.argmax(n_black_pixels_list)

def create_grayscale_from_bitmap():
    image_to_grayscale = cv2.imread(str(root) + '/data/tempPicture.jpg')
    arr = rgb_2_gray_scale(image_to_grayscale)
    arr = arr[70:-70, 70:-70]
    return arr

def save_scatter_plot_and_get_pixels(arr,pixel_value):
    indexArray_x, indexArray_y, indexArray_x_black, indexArray_y_black = identify_pixels.get_bright_and_dark_pixels(arr, pixel_value)
    plt.close()
    plt.scatter(indexArray_x_black, indexArray_y_black ,c = 'black')
    plt.scatter(indexArray_x, indexArray_y, c = 'yellow')
    plt.savefig(str(root) + '/data/tempPicture2.jpg')
    black_x = indexArray_x_black
    black_y = indexArray_y_black
    return black_x, black_y


def get_the_edges():
    raw_image = cv2.imread(str(root) + '/data/tempPicture2.jpg')
    bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
    #cv2.imshow('Bilateral', bilateral_filtered_image)
    #cv2.waitKey(0)
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
    #cv2.imshow('Edge', edge_detected_image)
    #cv2.waitKey(0)
    contours, _ = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def put_contours_in_list(contours):
    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True), True)
        area = cv2.contourArea(contour)
        if ((len(approx) > 8) & (area > 25) ):
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
        if r > 30 and r < 200:
            radius_list.append([xc, yc, r])
    return radius_list

def flip_orig_image(input_image):
    orig_image_read = plt.imread(input_image)
    plt.close()
    plt.imshow(orig_image_read)
    plt.savefig(str(root) + '/data/tempPicture3.jpg')
    orig_image = plt.imread(str(root) + '/data/tempPicture3.jpg')
    plt.close()
    orig_flipped = np.flipud(orig_image)
    return orig_flipped


def plot_circles_on_orig(index_most_black_pixels,pos_and_radius,input_image):
    number_of_points = np.linspace(0, 2*np.pi, 200)
    xunit = pos_and_radius[index_most_black_pixels][2]*np.cos(number_of_points) + pos_and_radius[index_most_black_pixels][0]
    yunit = pos_and_radius[index_most_black_pixels][2]*np.sin(number_of_points) + pos_and_radius[index_most_black_pixels][1]
    #plt.close()
    orig_flipped = flip_orig_image(input_image)
    plt.imshow(orig_flipped)
    plt.plot(xunit,yunit)
    plt.axis('scaled')
    folder_name = input_image.split('/')[-2]
    image_name = input_image.split('/')[-1]
    os.makedirs(str(root) + '/data/circle_folder/', exist_ok=True)
    print(str(root) + '/data/circle_folder/' + image_name)
    plt.savefig(str(root) + '/data/circle_folder/' + image_name)
    plt.show()

def remove_temp_jpgs():
    os.remove(str(root) + '/data/tempPicture.jpg')
    os.remove(str(root) + '/data/tempPicture2.jpg')
    os.remove(str(root) + '/data/tempPicture3.jpg')


#input_image = '/home/staffanbjorkdahl/PycharmProjects/tubus/data/frames/T20190823155414/image53.jpg'
#input_image = '/home/staffanbjorkdahl/PycharmProjects/tubus/data/frames/T20190829141432/image62.jpg'
#input_image = '/home/staffanbjorkdahl/PycharmProjects/tubus/data/frames/T20190823152643/image112.jpg'
#input_image = '/home/staffanbjorkdahl/PycharmProjects/tubus/data/frames/T20190829140453/image172.jpg'
#input_image = '/home/staffanbjorkdahl/PycharmProjects/tubus/data/frames/T20190829140453/image164.jpg'
#input_image = '/home/staffanbjorkdahl/PycharmProjects/tubus/data/frames/T20190829140453/image29.jpg'
#input_image = '/home/staffanbjorkdahl/PycharmProjects/tubus/data/frames/T20190823154915/image19.jpg'
#input_image = '/home/staffanbjorkdahl/PycharmProjects/tubus/data/frames/T20190823154915/image68.jpg' # No hole
#input_image = '/home/staffanbjorkdahl/PycharmProjects/tubus/data/frames/T20190823154915/image105.jpg' # No hole
pixel_value = 20

def main(images_folder):
    #for i in range(103, number_of_images_in_folder+1):
    #input_image = path_to_framefolder+'/image'+str(i)+'.jpg'

    for image_name, image_path in utils.folder_reader(images_folder):
        input_image = str(root) + '/data/frames/T20190829141432/image62.jpg'
        yellow_detection(input_image)
        arr = create_grayscale_from_bitmap()
        black_x, black_y=save_scatter_plot_and_get_pixels(arr,pixel_value)
        contours = get_the_edges()
        updated_contour_list = put_contours_in_list(contours)
        pos_and_radius = winnow_radii(updated_contour_list)
        index_most_black_pixels = count_pixels_in_circle(pos_and_radius,black_x, black_y, pixel_value)
        plot_circles_on_orig(index_most_black_pixels,pos_and_radius,input_image)
        remove_temp_jpgs()
        plt.close()

path_to_framefolder = str(root) + '/data/frames/res/T20190819122035'
number_of_images_in_folder = 239
main(path_to_framefolder, number_of_images_in_folder)

end_time = time.time()-start_time

print(end_time)
