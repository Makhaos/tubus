import os
import common.utils as utils
import common.aws_manager as aws_manager
import numpy as np
from scipy.ndimage import variance
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import laplace, gaussian


class BlurDetector:
    def __init__(self, frames_raw, frames_blur):
        self.frames_raw = frames_raw
        self.frames_blur = frames_blur
        self.fm_list = []
        self.variance_list = []
        self.max_list = []
        self.threshold = 0.02

    def calculate_laplacian(self):
        for image_name, image_path in utils.folder_reader(self.frames_raw):
            image_read = io.imread(os.path.join(image_path, image_name))
            gray = rgb2gray(image_read)
            gauss = gaussian(gray)
            fm = laplace(gauss, ksize=3)
            # Output
            self.fm_list.append(fm)
            self.variance_list.append(variance(fm)*1000)
            self.max_list.append(np.amax(fm))
            os.makedirs(self.frames_blur, exist_ok=True)

    def blur_results(self):
        root = utils.get_project_root()
        video_name = os.path.basename(os.path.dirname(self.frames_raw))
        os.makedirs(os.path.join(str(root), 'data', 'files', video_name), exist_ok=True)

        blurry_list = []
        blurry_dict = {}
        for t in self.variance_list:
            if t < self.threshold:
                blurry_list.append(self.variance_list.index(t))
                blurry_dict[str(self.variance_list.index(t))] = 'blur'
            else:
                blurry_dict[str(self.variance_list.index(t))] = 'no_blur'
        progressbar_dict = utils.progress_bar_subroutine(blurry_dict, len(self.variance_list))
        data = {
            'name': video_name,
            'blur_images': blurry_dict,
            'blur_percentage': str(round(len(blurry_list) / len(self.variance_list) * 100)) + ' % ',
            'focused_percentage': str(100-round(len(blurry_list) / len(self.variance_list) * 100)) + ' % ',
            'total_images': str(len(self.variance_list)),
            'progress_bar': progressbar_dict,
            'type': 'blur'
        }
        aws_manager.dynamo_upload(data)
