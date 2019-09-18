import os
import common.natural_keys as natural_keys
import matplotlib.pyplot as plt
import numpy as np
import cv2


def calculate_laplacian(video_name_no_extension, frames_folder):
    fm_list = []
    for root, dirs, files in os.walk(frames_folder + video_name_no_extension):
        for image in sorted(files, key=natural_keys.natural_keys):
            with open(os.path.join(root, image), "r") as auto:
                image_read = cv2.imread(root + '/' + image)
                # For cropping
                # image_read = image_read[0:495, 0:800]
                # Optional Gaussian filter
                # image_read = cv2.GaussianBlur(image_read, (3, 3), 0)
                gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
                fm = cv2.Laplacian(gray, cv2.CV_64F).var()
                fm_list.append(fm)
                cv2.putText(image_read, "Blurry level: {:.2f}".format(fm), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
                cv2.imwrite(root + '/' + image,
                            image_read)  # save frame as JPG file
                return fm_list


def print_blur_results(fm_list, video_name_no_extension):
    blurry_list = []
    print("Video name:", video_name_no_extension)
    average = round(sum(fm_list) / len(fm_list), 2)
    print(' ' * 5, "Average of blurriness:", average)
    for l in fm_list:
        if l < 110:
            blurry_list.append(fm_list.index(l))
    print(' ' * 5, "List of blurry images", blurry_list)
    print(' ' * 5, "Amount of blurry images", len(blurry_list), "|", "in", len(fm_list), "total amount of images")
    print(' ' * 5, "Percentage of blurry images", round(len(blurry_list) / len(fm_list), 2) * 100, '%')

    return average


def plot_video_blurriness_level(fm_list):
    plt.figure()
    y = fm_list
    x = np.arange(0, 180, 1)
    plt.xticks(np.arange(0, 180, step=2))

    plt.plot(x, y, color='green', linestyle='dashed', linewidth=3,
             marker='o', markerfacecolor='blue', markersize=8)
    for x, y in zip(x, y):
        plt.text(x, y, str(x), color="red", fontsize=6)
    plt.grid()
    plt.pause(0.0001)
