import cv2
import os


def get_frame(video, frame_rate, sec):
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_rate * sec)
    has_frames, image = video.read()
    cv2.imwrite("data/images/image" + str(sec) + ".jpg", image)  # save frame as JPG file


def main():
    # os.system("rm -r data/images/*")  # This deletes all images created
    video = cv2.VideoCapture("data/T20190821174253.AVI")
    frame_rate = float(video.get(cv2.CAP_PROP_FPS))
    number_of_frames = float(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video_length = number_of_frames / frame_rate
    sec = 0
    while sec <= video_length:
        get_frame(video, frame_rate, sec)
        sec += 1


if __name__ == "__main__":
    main()
