import os
import time
import common.utils as utils
from src import video_to_frames, blur, color_detection, identify_pixels, identify_circles


def main():
    root = utils.get_project_root()
    videos_folder = os.path.join(str(root), 'for_testing')
    frames_folder = os.path.join(str(root), 'data', 'frames')
    frames_creator = video_to_frames.FramesCreator(videos_folder, frames_folder, crop=True)
    frames_creator.get_frame()

    # Loop through all videos in folder
    for video_name, video_path in utils.folder_reader(videos_folder):
        video_name_no_extension, video_name_extension = os.path.splitext(video_name)
        frames_raw = os.path.join(str(root), 'data', 'frames', video_name_no_extension, 'raw')
        frames_res = os.path.join(str(root), 'data', 'frames', video_name_no_extension, 'res')
        color_detector = color_detection.ColorDetector(frames_raw, frames_res)
        # HSV values
        yellow_low = [18, 25, 25]
        yellow_high = [30, 255, 255]
        color_detector.detect_yellow(yellow_low, yellow_high)
        frames_blur = os.path.join(str(root), 'data', 'frames', video_name_no_extension, 'blur')
        blur_detector = blur.BlurDetector(frames_raw, frames_blur)
        blur_detector.calculate_laplacian()
        blur_detector.blur_results()
        # Identify pixels
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
        return 6


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Main program took", round(time.time() - start_time, 2), "seconds to run")
