import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import re
import time


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    """
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def blur(video_name_no_extension):
    fm_list = []
    blurry_list = []
    print("Video name:", video_name_no_extension)
    # while image_number < video_length:
    for root, dirs, files in os.walk("data/frames/" + video_name_no_extension):
        for image in sorted(files, key=natural_keys):
            with open(os.path.join(root, image), "r") as auto:
                image_read = cv2.imread(root + '/' + image)
                # image = image[0:495, 0:800] # cropping
                gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
                fm = cv2.Laplacian(gray, cv2.CV_64F).var()
                fm_list.append(fm)
    # printing
    average = round(sum(fm_list) / len(fm_list), 2)
    print(' ' * 5, "Average of blurriness:", average)
    for l in fm_list:
        if l < 110:
            blurry_list.append(fm_list.index(l))
    print(' ' * 5, "List of blurry images", blurry_list)
    print(' ' * 5, "Amount of blurry images", len(blurry_list), "|", "in", len(fm_list), "total amount of images")
    print(' ' * 5, "Percentage of blurry images", round(len(blurry_list) / len(fm_list), 2) * 100, '%')
    return fm_list, average


def plot(fm_list):
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


def get_frame(video_root, video_name):
    video = cv2.VideoCapture(video_root + '/' + video_name)
    frame_rate = float(video.get(cv2.CAP_PROP_FPS))
    number_of_frames = float(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video_length = round(number_of_frames / frame_rate)
    print(video_length)
    sec = 0
    video_name_no_extension, video_name_extension = os.path.splitext(video_name)
    os.makedirs("data/frames/" + video_name_no_extension, exist_ok=True)
    while sec <= video_length - 1:  # Removing last frame
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_rate * sec)
        # video.set(cv2.CAP_PROP_POS_FRAMES, sec)
        has_frames, image = video.read()
        cv2.imwrite("data/frames/" + video_name_no_extension + "/image" + str(sec) + ".jpg",
                    image)  # save frame as JPG file
        sec += 1
    return video_name_no_extension


def main():
    blurry_averages = []
    plt.ion()
    videos_list, videos_root_list = videos_reader()
    # video_name = "T20190821174253.AVI"
    for video_name, video_root in zip(videos_list, videos_root_list):
        video_name_no_extension, video_name_extension = os.path.splitext(video_name)
        get_frame(video_root, video_name)
        fm_list, average = blur(video_name_no_extension)
        blurry_averages.append(average)
        # plot(fm_list)
        print('*' * 100)
    print("List of averages", blurry_averages)
    average_of_averages = sum(blurry_averages) / len(blurry_averages)
    print("Average of averages:", average_of_averages)
    # plt.show()
    # input("Press [enter] to continue.")


def videos_reader():
    videos_list = []
    root_list = []
    for root, dirs, files in os.walk("data/videos"):
        for file in files:
            with open(os.path.join(root, file), "r") as auto:
                root_list.append(root)
                videos_list.append(file)
    return videos_list, root_list


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("My program took", round(time.time() - start_time, 2), "seconds to run")
