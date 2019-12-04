from src import video_to_frames
from common import utils
import os
import numpy as np
from scipy.ndimage import variance
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import laplace

class BlurDetector:
    def __init__(self, frames_raw):
        self.frames_raw = frames_raw
        self.fm_list = []

    def calculation(self):
        for image_name, image_path in utils.folder_reader(self.frames_raw):
            image_read = io.imread(os.path.join(image_path, image_name))
            # image_read = resize(image_read, (400, 600))
            gray = rgb2gray(image_read)
            fm = laplace(gray, ksize=3)
            self.fm_list.append(fm)
            # Print output
            # print(f"{variance(fm)}")
            print(f"{np.amax(fm)}")


def main():
    root = utils.get_project_root()
    # video = os.path.join(str(root), 'data', 'videos', '0821', '18', 'T20190821181537.AVI')
    # frames_folder = os.path.join(str(root), 'data', 'frames')
    # frames_creator = video_to_frames.FramesCreator(video, frames_folder, fps=1, crop=True)
    # frames_creator.get_frame()
    frames_raw = os.path.join(str(root), 'data', 'frames', 'T20190819081657', 'raw')
    blur_detector = BlurDetector(frames_raw)
    blur_detector.calculation()


if __name__ == '__main__':
    main()
