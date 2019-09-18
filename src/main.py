import os
import time
import common.natural_keys as natural_keys
from src import video_to_frames, blur, video_reader, identifyPixels, plot, color_detection


def main():
    videos_folder = "/home/manuel/PycharmProjects/tubus_project/data/videos/0827/10"
    frames_folder = "/home/manuel/PycharmProjects/tubus_project/data/frames"
    videos_list, videos_root_list = video_reader.videos_reader(videos_folder)

    # Loop through all videos
    # for video_name, video_root in zip(videos_list, videos_root_list):
    #     video_name_no_extension, video_name_extension = os.path.splitext(video_name)
    #     # Create frames from a video
    #     os.makedirs(frames_folder + video_name_no_extension, exist_ok=True)
        # video_to_frames.get_frame(video_root, video_name, frames_folder, video_name_no_extension)
        #
        # # Calculate blurriness of each image
        # fm_list = blur.calculate_laplacian(video_name_no_extension, frames_folder)
        # # Print blurriness results
        # blur.print_blur_results(fm_list, video_name_no_extension)

        # Loop through frames TODO only one loop for blurriness and variances
    variance_list = []
    for root, dirs, files in os.walk(frames_folder + '/T20190823152643'):
        for image in sorted(files, key=natural_keys.natural_keys):
            with open(os.path.join(root, image), "r") as auto:
                res = color_detection.color_detection(root + '/' + image)
                variance_x, variance_y = identifyPixels.main(res)
                print('Frame:', image)
                variance = variance_x + variance_y
                variance_list.append(variance)
    with open('data/files/T20190823152643.txt', 'w') as f:
        for item in variance_list:
            f.write("%s\n" % item)
    plot.plot_list(variance_list)



if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Main program took", round(time.time() - start_time, 2), "seconds to run")
