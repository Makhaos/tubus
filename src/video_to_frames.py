import cv2
import common.utils as utils
import os


# From a video creates one frame per second. Option to crop the video from the boolean crop
class FramesCreator:
    def __init__(self, videos_folder, frames_folder, crop):
        self.videos_folder = videos_folder
        self.frames_folder = frames_folder
        self.crop = crop
        os.makedirs(frames_folder, exist_ok=True)

    def get_frame(self):
        for video_name, video_path in utils.folder_reader(self.videos_folder):
            video_name_no_extension, video_name_extension = os.path.splitext(video_name)
            video = cv2.VideoCapture(os.path.join(video_path, video_name))
            frame_rate = float(video.get(cv2.CAP_PROP_FPS))
            number_of_frames = float(video.get(cv2.CAP_PROP_FRAME_COUNT))
            video_length = round(number_of_frames / frame_rate)
            frames_raw = os.path.join(self.frames_folder, video_name_no_extension, 'raw')
            os.makedirs(frames_raw, exist_ok=True)
            second = 0
            while second <= video_length - 1:  # Removing last frame
                video.set(cv2.CAP_PROP_POS_FRAMES, frame_rate * second)
                has_frames, image = video.read()
                if self.crop:
                    image = image[30:495, 30:670]
                if not cv2.imwrite(
                        os.path.join(frames_raw, 'image' + str(second) + '.jpg'),
                        image):
                    raise Exception('Could not write frames')
                second += 1
            else:
                print('Frames from the video', video_name_no_extension, 'created at', frames_raw)


def main():
    root = utils.get_project_root()
    videos_folder = os.path.join(str(root), 'data', 'videos', 'chosen_videos', 'for_testing')
    frames_folder = os.path.join(str(root), 'data', 'frames')
    frames_creator = FramesCreator(videos_folder, frames_folder, crop=True)
    frames_creator.get_frame()


if __name__ == '__main__':
    main()
