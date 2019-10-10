import os
import time
import common.utils as utils
from src import video_to_frames, blur, color_detection


def main():
    root = utils.get_project_root()
    videos_folder = os.path.join(str(root), 'data', 'videos', 'chosen_videos', 'for_testing')
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


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Main program took", round(time.time() - start_time, 2), "seconds to run")
