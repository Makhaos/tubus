import cv2
import numpy as np
import common.utils as utils
import os

# TODO change '/' paths to os.path.join for cross platform compatibility. Working example at video_to_frames

class ColorDetector:
    def __init__(self, frames_folder, output_frames_folder):
        self.frames_folder = frames_folder
        self.output_images_folder = output_frames_folder

    def detect_yellow(self, hsv_low, hsv_high):
        os.makedirs(self.output_images_folder, exist_ok=True)
        for image_name, image_path in utils.folder_reader(self.frames_folder):
            image_read = cv2.imread(image_path + '/' + image_name)
            hsv = cv2.cvtColor(image_read, cv2.COLOR_BGR2HSV)
            yellow_lower = np.array(hsv_low, np.uint8)
            yellow_upper = np.array(hsv_high, np.uint8)
            yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
            res = cv2.bitwise_and(src1=image_read, src2=image_read, mask=yellow)
            cv2.imwrite(self.output_images_folder + '/' + image_name, res)


def main():
    root = utils.get_project_root()
    frames_folder = str(root) + '/data/frames'
    output_frames_folder = str(root) + '/data/frames_res'
    color_detector = ColorDetector(frames_folder, output_frames_folder)
    # HSV values
    yellow_low = [18, 25, 25]
    yellow_high = [30, 255, 255]
    color_detector.detect_yellow(yellow_low, yellow_high)


if __name__ == '__main__':
    main()
