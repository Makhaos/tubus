import os
import sys
import time
from src import video_to_frames, blur, video_reader


def main():
    videos_folder = "/home/manuel/PycharmProjects/tubus_project/data/videos/0820/12"
    frames_folder = "/home/manuel/PycharmProjects/tubus_project/data/frames"
    videos_list, videos_root_list = video_reader.videos_reader(videos_folder)

    # Loop through all videos
    for video_name, video_root in zip(videos_list, videos_root_list):
        video_name_no_extension, video_name_extension = os.path.splitext(video_name)
        # Create frames from a video
        os.makedirs(frames_folder + video_name_no_extension, exist_ok=True)
        video_to_frames.get_frame(video_root, video_name, frames_folder, video_name_no_extension)

        # Calculate blurriness of each image
        fm_list = blur.calculate_laplacian(video_name_no_extension, frames_folder)
        # Print blurriness results
        blur.print_blur_results(fm_list, video_name_no_extension)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Main program took", round(time.time() - start_time, 2), "seconds to run")
