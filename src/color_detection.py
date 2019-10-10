import cv2
import numpy as np
import common.utils as utils
import os


class ColorDetector:
    def __init__(self, frames_raw, frames_res):
        self.frames_raw = frames_raw
        self.frames_res = frames_res

    def detect_yellow(self, hsv_low, hsv_high):
        os.makedirs(self.frames_res, exist_ok=True)
        for image_name, image_path in utils.folder_reader(self.frames_raw):
            image_read = cv2.imread(os.path.join(image_path, image_name))
            hsv = cv2.cvtColor(image_read, cv2.COLOR_BGR2HSV)
            yellow_lower = np.array(hsv_low, np.uint8)
            yellow_upper = np.array(hsv_high, np.uint8)
            yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
            res = cv2.bitwise_and(src1=image_read, src2=image_read, mask=yellow)
            cv2.imwrite(os.path.join(self.frames_res, image_name), res)


def main():
    root = utils.get_project_root()
    frames_raw = os.path.join(str(root), 'data', 'frames', 'a_video_for_test', 'raw')
    frames_res = os.path.join(str(root), 'data', 'frames', 'a_video_for_test', 'res')
    color_detector = ColorDetector(frames_raw, frames_res)
    # HSV values
    yellow_low = [18, 25, 25]
    yellow_high = [30, 255, 255]
    color_detector.detect_yellow(yellow_low, yellow_high)


if __name__ == '__main__':
    main()
