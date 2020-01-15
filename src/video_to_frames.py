import cv2
import common.utils as utils
import os


# From a video creates one frame per second. Option to crop the video from the boolean crop
class FramesCreator:
    def __init__(self, video, frames_folder, fps, crop):
        self.video = video
        self.frames_folder = frames_folder
        self.crop = crop
        self.fps = fps
        os.makedirs(frames_folder, exist_ok=True)

    def get_frame(self):
        video_name_no_extension, video_name_extension = os.path.splitext(self.video)
        video = cv2.VideoCapture(self.video)
        frame_rate = float(video.get(cv2.CAP_PROP_FPS))
        number_of_frames = float(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video_length = round(number_of_frames / frame_rate)
        frames_raw = os.path.join(self.frames_folder, video_name_no_extension, 'raw')
        os.makedirs(frames_raw, exist_ok=True)
        frame = 0
        while frame <= video_length*self.fps - self.fps:  # Removing last second
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_rate*frame/self.fps)
            has_frames, image = video.read()
            if self.crop:
                image = image[30:495, 30:670]
            if not cv2.imwrite(
                    os.path.join(frames_raw, 'image' + str(frame) + '.jpg'),
                    image):
                raise Exception('Could not write frames')
            frame += 1
        else:
            print('Frames from the video', video_name_no_extension, 'created at', frames_raw)


def main():
    root = utils.get_project_root()
    videos_folder = os.path.join(str(root), 'data', 'videos', 'chosen_videos', 'for_testing')
    frames_folder = os.path.join(str(root), 'data', 'frames')
    frames_creator = FramesCreator(videos_folder, frames_folder, fps=1, crop=True)
    frames_creator.get_frame()


if __name__ == '__main__':
    main()
