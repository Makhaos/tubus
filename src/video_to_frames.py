import cv2


# From a video creates one frame a second

def get_frame(video_root, video_name, frames_folder, video_name_no_extension):
    video = cv2.VideoCapture(video_root + '/' + video_name)
    frame_rate = float(video.get(cv2.CAP_PROP_FPS))
    number_of_frames = float(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video_length = round(number_of_frames / frame_rate)
    sec = 0
    while sec <= video_length - 1:  # Removing last frame
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_rate * sec)
        has_frames, image = video.read()
        image = image[30:495, 30:670]

        cv2.imwrite(frames_folder + '/' + video_name_no_extension + "/image" + str(sec) + ".jpg", image)
        sec += 1
    return video_name_no_extension
