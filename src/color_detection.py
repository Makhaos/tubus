import cv2
import numpy as np


def color_detection(image_path):
    # image_path = '/home/manuel/PycharmProjects/tubus_project/data/frames/movie2/image107.jpg'
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
    # print(np.max(res))
    # print(np.max(image_read))
    # (contours, hierarchy) = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if area > 100:
    #         x, y, w, h = cv2.boundingRect(contour)
    #         image_read = cv2.rectangle(image_read, (x, y), (x + w, y + h), (255, 0, 0), 3)

    # Display results
    # cv2.imshow("Color Tracking", image_read)
    # cv2.imshow("Yellow", res)
    # cv2.waitKey()

    # cv2.imwrite('/home/manuel/Desktop/testing_color/black.jpg', image_read)
    # cv2.imwrite(image_path + '/res', res)
    # cv2.imwrite(frames_folder + video_name_no_extension + "/image" + str(
    #     sec) + ".jpg",
    #             image)
    return res
    # if cv2.waitKey(10) & 0xFF == 27:
    #     cv2.destroyAllWindows()


if __name__ == "__main__":
    color_detection()
