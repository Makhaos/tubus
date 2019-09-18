import cv2
import numpy as np
import utils
import os


def yellow_detection(images_folder, filtered_images_folder):
    os.makedirs(filtered_images_folder, exist_ok=True)
    for image_name, image_path in utils.folder_reader(images_folder):
        image_read = cv2.imread(image_path + '/' + image_name)
        hsv = cv2.cvtColor(image_read, cv2.COLOR_BGR2HSV)
        yellow_lower = np.array([18, 25, 25], np.uint8)
        yellow_upper = np.array([30, 255, 255], np.uint8)
        yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
        res = cv2.bitwise_and(src1=image_read, src2=image_read, mask=yellow)
        cv2.imwrite(filtered_images_folder + '/' + image_name, res)
