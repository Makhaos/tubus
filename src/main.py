import os
import time
import sys
import utils
from src import video_to_frames, blur, identify_pixels, plot, color_detection, identify_circles_bit_map


def main():
    root = utils.get_project_root()

    # Edit according to the relevant video data
    videos_folder = str(root) + '/data/videos/0819/12'

    frames_folder = str(root) + '/data/frames'

    # Loop through all videos in folder
    for video_name, video_path in utils.folder_reader(videos_folder):
        video_name_no_extension, video_name_extension = os.path.splitext(video_name)

        # Create frames from a video
        os.makedirs(frames_folder + '/' + video_name_no_extension, exist_ok=True)
        video_to_frames.get_frame(video_path, video_name, frames_folder, video_name_no_extension)

        # TODO improve blurriness algorithm and code
        # # Calculate blurriness of each image
        # fm_list = blur.calculate_laplacian(video_name_no_extension, frames_folder)
        # # Print blurriness results
        # blur.print_blur_results(fm_list, video_name_no_extension)

        # Detect yellow in frames
        hue_low = 18
        saturation_low = 25
        value_low = 25
        color_detection.yellow_detection(frames_folder + '/' + video_name_no_extension,
                                         frames_folder + '/res/' + video_name_no_extension, hue_low,
                                         saturation_low, value_low)

        # Calculate variance
        variance_list = identify_pixels.main(frames_folder + '/res/' + video_name_no_extension)

        # Plot variance results
        plot.plot_list(variance_list, video_name_no_extension)  # TODO improve quality of saved plots

        # Identify black holes (circles) in the pipes
        hue_low = 16
        saturation_low = 25
        value_low = 0
        color_detection.yellow_detection(frames_folder + '/' + video_name_no_extension,
                                         frames_folder + '/res_for_circles/' + video_name_no_extension, hue_low,
                                         saturation_low, value_low)

        identify_circles_bit_map.main(frames_folder + '/' + video_name_no_extension, frames_folder + '/res_for_circles/' + video_name_no_extension)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Main program took", round(time.time() - start_time, 2), "seconds to run")
