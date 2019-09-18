import cv2
import numpy as np
import identifyPixels


def color_detection(image_path):
    # image_path = '/home/staffanbjorkdahl/PycharmProjects/tubus/data/framesT20190819122035/image23.jpg'
    # image_path = '/home/manuel/PycharmProjects/tubus_project/data/frames/T20190829091542/image15.jpg'
    # image_path = '/home/manuel/Desktop/yellowblack.png'
    image_read = cv2.imread(image_path)
    hsv = cv2.cvtColor(image_read, cv2.COLOR_BGR2HSV)
    yellow_lower = np.array([18, 25, 25], np.uint8)
    yellow_upper = np.array([30, 255, 255], np.uint8)
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    # kernal = np.ones((5, 5), "uint8")
    # blue = cv2.dilate(yellow, kernal)
    res = cv2.bitwise_and(src1=image_read, src2=image_read, mask=yellow)
    return res


if __name__ == "__main__":
    color_detection()
