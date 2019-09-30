import cv2
import numpy as np
import utils
import os
from matplotlib import pyplot as plt


def yellow_detection(images_folder, filtered_images_folder, h_low, s_low, v_low):
    bit_map_list = list()
    os.makedirs(filtered_images_folder, exist_ok=True)
    for image_name, image_path in utils.folder_reader(images_folder):
        print(image_name)
        image_read = cv2.imread(image_path + '/' + image_name)
        hsv = cv2.cvtColor(image_read, cv2.COLOR_BGR2HSV)
        yellow_lower = np.array([h_low, s_low, v_low], np.uint8)
        yellow_upper = np.array([30, 255, 255], np.uint8)
        yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
        res = cv2.bitwise_and(src1=image_read, src2=image_read, mask=yellow)
        cv2.imwrite(filtered_images_folder + '/' + image_name, res)
        bit_map_list.append(res)
        # plt.imshow(res)
        # plt.savefig(filtered_images_folder + '/' + image_name)
    return bit_map_list

