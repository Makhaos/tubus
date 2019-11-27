import cv2
import os
import common.utils as utils
import common.plot as plot
import common.aws_manager as aws_manager


class BlurDetector:
    def __init__(self, frames_raw, frames_blur):
        self.frames_raw = frames_raw
        self.frames_blur = frames_blur
        self.fm_list = []

    def calculate_laplacian(self):
        for image_name, image_path in utils.folder_reader(self.frames_raw):
            image_read = cv2.imread(os.path.join(image_path, image_name))
            gray = cv2.cvtColor(image_read, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            self.fm_list.append(fm)
            os.makedirs(self.frames_blur, exist_ok=True)
            cv2.putText(image_read, "Blurry level: {:.2f}".format(fm),
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
            cv2.imwrite(os.path.join(self.frames_blur, image_name), image_read)
        with open(os.path.join(self.frames_blur, 'laplacian_values.txt'), 'w') as writer:
            writer.write(str(self.fm_list))

    def blur_results(self):
        root = utils.get_project_root()
        video_name = os.path.basename(os.path.dirname(self.frames_raw))
        os.makedirs(os.path.join(str(root), 'data', 'files', video_name), exist_ok=True)
        # TODO clean up txt creation
        with open(os.path.join(str(root), 'data', 'files', video_name, 'blur_results.json'), 'w') as writer:
            blurry_list = []
            writer.write('Video: ' + video_name + '\n')
            try:
                average = round(sum(self.fm_list) / len(self.fm_list), 2)
                writer.write(' ' * 5 + ' Average of blurriness: ' + str(average) + '\n')
                for l in self.fm_list:
                    if l < 110:
                        blurry_list.append(self.fm_list.index(l))
                writer.write(' ' * 5 + ' List of blurry images ' + str(blurry_list) + '\n')
                writer.write(' ' * 5 + ' Amount of blurry images ' + str(len(blurry_list)) + ' | ' + ' in ' + str(
                    len(self.fm_list)) + ' total amount of images ' + '\n')
                writer.write(' ' * 5 + ' Percentage of blurry images ' + str(
                    round(len(blurry_list) / len(self.fm_list), 2) * 100) + ' % ' + '\n')
                plot.plot_list(self.fm_list, video_name, 'blur_plot')
                print('Blur results completed. File located at',
                      os.path.join(str(root), 'data', 'files', video_name, 'blur_results.txt'))
                data = {
                    'name': video_name,
                    'blur_images': str(blurry_list),
                    'blur_percentage': str(round(len(blurry_list) / len(self.fm_list), 2) * 100) + ' % ',
                    'type': 'blur'
                }
                aws_manager.dynamo_upload(data)
            except ZeroDivisionError as error:
                print(error, 'in method blur_results:\n',
                      'To get results, the Laplacian needs to be calculated before. '
                      'Use the calculate_laplacian method')


def main():
    root = utils.get_project_root()
    frames_raw = os.path.join(str(root), 'data', 'frames', 'a_video_for_test', 'raw')
    frames_blur = os.path.join(str(root), 'data', 'frames', 'a_video_for_test', 'blur')
    blur_detector = BlurDetector(frames_raw, frames_blur)
    blur_detector.calculate_laplacian()
    blur_detector.blur_results()


if __name__ == '__main__':
    main()
