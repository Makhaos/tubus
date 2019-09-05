import cv2
import os


def get_frame(video, sec):
    video.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    has_frames, image = video.read()
    if has_frames:
        cv2.imwrite("data/images/image" + str(sec) + ".jpg", image)  # save frame as JPG file
        return has_frames


def main():
    # os.system("rm -r data/images/*")  # This deletes all images created
    video = cv2.VideoCapture("data/T20190821174253.AVI")
    sec = 0
    frame_rate = 1
    success = get_frame(video, sec)
    while success:
        sec = sec + frame_rate
        sec = round(sec, 2)
        success = get_frame(video, sec)


if __name__ == "__main__":
    main()
