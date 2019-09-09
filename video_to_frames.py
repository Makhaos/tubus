import os
import cv2
import matplotlib.pyplot as plt
import numpy as np


def blur():
    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--images", required=True,
    #                 help="data/images")
    # ap.add_argument("-t", "--threshold", type=float, default=100.0,
    #                 help="focus measures that fall below this value will be considered 'blurry'")
    # args = vars(ap.parse_args())
    i = 0
    fm_list = []
    blurry_list = []
    while i < 4236:
        image_number = i

        # Create an Image object from an Image
        # image_object = Image.open("data/images/image{}.jpg".format(image_number))
        # width, height = image_object.size

        # Crop the iceberg portion
        # cropped = image_object.crop((0, 0, width, height / 1.23))

        image = cv2.imread("data/at24fps/image{}.jpg".format(image_number))
        # image = image[0:495, 0:800]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        text = "Not Blurry"
        fm_list.append(fm)
        if fm < 100:
            text = "Blurry"

        # # show the image
        # cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        # cv2.imshow("Image", image)
        # key = cv2.waitKey(0)
        i += 1
    print(fm_list)
    y = fm_list
    x = np.arange(0, 4236, 1)
    plt.xticks(np.arange(0, 4236, step=5))
    # plotting the points
    plt.plot(x, y, color='green', linestyle='dashed', linewidth=3,
             marker='o', markerfacecolor='blue', markersize=8)
    for x, y in zip(x, y):
        plt.text(x, y, str(x), color="red", fontsize=6)
    plt.grid
    plt.show()
    average = sum(fm_list) / len(fm_list)
    print(average)
    for l in fm_list:
        if l < 110:
            blurry_list.append(fm_list.index(l))
    print(blurry_list)
    print(len(blurry_list))


def get_frame(video_name):
    video = cv2.VideoCapture("data/{}".format(video_name))
    frame_rate = float(video.get(cv2.CAP_PROP_FPS))
    number_of_frames = float(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video_length = number_of_frames / frame_rate
    sec = 0
    while sec <= number_of_frames:
        # video.set(cv2.CAP_PROP_POS_FRAMES, frame_rate * sec)
        video.set(cv2.CAP_PROP_POS_FRAMES, sec)
        has_frames, image = video.read()
        cv2.imwrite("data/at24fps/image" + str(sec) + ".jpg", image)  # save frame as JPG file
        sec += 1


def main():
    # os.system("rm -r data/images/*")  # This deletes all images created
    video_name = "T20190821174253.AVI"
    # get_frame(video_name)
    blur()


if __name__ == "__main__":
    main()
