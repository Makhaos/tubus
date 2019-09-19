import os
import time
import sys
import utils
from src import video_to_frames, blur, identify_pixels, plot, color_detection


def main():
    root = utils.get_project_root()

    # Edit according to the relevant video data
    videos_folder = str(root) + '/data/videos/0823/15'

    frames_folder = str(root) + '/data/frames'

    bit_map_bool = 1  # bit_map_bool = 1 yields bitmap object. bit_map_bool = 0 yields image object

    if bit_map_bool == 0 or bit_map_bool == 1:
        pass
    else:
        print('bit_map_bool must be either 0 or 1')
        sys.exit()

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
        bit_map_list = color_detection.yellow_detection(frames_folder + '/' + video_name_no_extension,
                                         str(root) + '/data/frames/res/' + video_name_no_extension)

        # Calculate variance
        variance_list = identify_pixels.main(str(root) + '/data/frames/res/' + video_name_no_extension, bit_map_list, bit_map_bool)

        # Plot variance results
        plot.plot_list(variance_list, video_name_no_extension, bit_map_bool) # TODO improve quality of saved plots


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Main program took", round(time.time() - start_time, 2), "seconds to run")
