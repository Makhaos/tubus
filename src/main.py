import os
import time
from common import utils
from common.aws_manager import download_file
from src import video_to_frames, blur, color_detection, identify_pixels, identify_circles

root = utils.get_project_root()
os.makedirs(os.path.join(str(root), 'data', 'videos'), exist_ok=True)


def download_and_process(video_name, blur_is_enabled, variance_is_enabled, circles_is_enabled, bucket):
    video = download_file(video_name, bucket)
    main(video, blur=blur_is_enabled, variance=variance_is_enabled, circles=circles_is_enabled)


def main(video, **kwargs):
    start_time = time.time()
    blur_is_enabled = kwargs.get('blur', False)
    variance_is_enabled = kwargs.get('variance', False)
    circles_is_enabled = kwargs.get('circles', False)
    root = utils.get_project_root()
    frames_folder = os.path.join(str(root), 'data', 'frames')
    frames_creator = video_to_frames.FramesCreator(video, frames_folder, fps=1, crop=True)
    frames_creator.get_frame()
    video_name_no_extension, video_name_extension = os.path.splitext(video)
    frames_raw = os.path.join(str(root), 'data', 'frames', video_name_no_extension, 'raw')
    frames_res = os.path.join(str(root), 'data', 'frames', video_name_no_extension, 'res')

    if blur_is_enabled or variance_is_enabled:
        color_detector = color_detection.ColorDetector(frames_raw, frames_res)
        # HSV values
        yellow_low = [18, 25, 25]
        yellow_high = [30, 255, 255]
        color_detector.detect_yellow(yellow_low, yellow_high)

    if blur_is_enabled:
        frames_blur = os.path.join(str(root), 'data', 'frames', video_name_no_extension, 'blur')
        blur_detector = blur.BlurDetector(frames_raw, frames_blur)
        blur_detector.calculate_laplacian()
        blur_detector.blur_results()

    # Identify pixels
    if variance_is_enabled:
        variance_index = 0
        for image_name, image_directory in utils.folder_reader(frames_raw):
            variance_index += 1
            image_name_path = os.path.join(image_directory, image_name)
            variance_image = identify_pixels.Variance(image_name_path)
            variance_image.create_grayscale_from_rgb()
            variance_image.get_bright_and_dark_pixels()
            variance_image.calculate_variance()
            csv = identify_pixels.WritingCSV(image_name_path)
            csv.write_plot_data_2_csv(variance_index)

    # Identify circles
    if circles_is_enabled:
        yellow_low = [14, 25, 25]
        yellow_high = [30, 255, 255]
        scatter_images = identify_circles.ScatterImages(video_name_no_extension)
        scatter_images.get_res(yellow_low, yellow_high)
        scatter_images.get_scatter_plot()
        edge_detection = identify_circles.EdgeDetection(video_name_no_extension)
        edge_detection.get_edges()
        circle_pos = identify_circles.CirclePosition(video_name_no_extension)
        circle_pos.get_valid_radii()
        circle_pos.count_pixels_in_circle()
        circle_pos.plot_circles_on_raw_image()
        identify_circles.CirclePosition.features_selected_circle = list()

    print("Main program took", round(time.time() - start_time, 2), "seconds to run")
