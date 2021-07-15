import math
import cv2
import os
import imageio
import numpy
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp

# TODO create more characters in dict
# ascii dict used
ascii_dict = [None]
ascii_dict[0:40] = (40 - 0) * [' ']
ascii_dict[40:50] = (50 - 40) * ['_']
ascii_dict[50:75] = (75 - 50) * ['!']
ascii_dict[75:90] = (90 - 75) * ['|']
ascii_dict[90:128] = (128 - 90) * ['t']
ascii_dict[128:170] = (170 - 128) * ['w']
ascii_dict[170:220] = (220 - 170) * ['#']
ascii_dict[220:256] = (256 - 220) * ['@']


class ASCIIVideo:
    def __init__(self):
        pass

    def generate_ascii_video(self, original_video_path, quality, save_file_path, is_colored, has_audio):
        """
        generates a ascii video at th save_file_path taking the video at original_video_path
        :param original_video_path:
        :param quality:
        :param save_file_path:
        :return:
        """
        # gets a reference to the video and fps
        cam = cv2.VideoCapture(original_video_path)
        fps = cam.get(cv2.CAP_PROP_FPS)

        # frame counter
        frame_count = 0
        keep_reading = True

        # setup for Image creation
        font = ImageFont.load_default()
        l_width = font.getsize("x")[0]
        l_height = font.getsize("$")[1]

        # vars to store vid height and width
        vid_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        vid_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # video to be saved
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_file_path = save_file_path.rsplit(".mp4", 1)[0] + "_video_only.mp4"
        video = cv2.VideoWriter(video_file_path, fourcc, fps, (math.ceil(vid_width * l_width / quality),
                                                              math.ceil(vid_height * l_height / (quality * 2))))

        # keep reading the video until no more frames
        while keep_reading:
            # read the image
            keep_reading, frame = cam.read()

            # if an image was found
            if keep_reading:
                # add to the total count
                frame_count += 1

                # create image container for ascii image
                new_img = Image.new("RGB", (math.ceil((vid_width * l_width) / quality), math.ceil((vid_height * l_height) /
                                                                                      (2 * quality))), 'black')
                draw = ImageDraw.Draw(new_img)

                # transfer image to ascii
                y_height = 0

                # set the ascii chars for the image
                for i in range(vid_height):
                    if i % (quality * 2) == 0:
                        text = ''
                        y_width = 0
                        for x in range(vid_width):
                            if x % quality == 0:
                                ascii_char = ascii_dict[int((int(format(frame[i, x, 0])) + int(
                                    format(frame[i, x, 1])) + int(format(frame[i, x, 2]))) / 3)]
                                text += ascii_char

                                # set fill to black if no color otherwise set the color to the given pixels color
                                fill = (frame[i, x, 2], frame[i, x, 1], frame[i, x, 0]) if is_colored \
                                    else (255, 255, 255)

                                # colors the cell
                                draw.text((y_width, y_height), ascii_char, font=font, fill=fill)
                                y_width += l_width
                        y_height += l_height

                # convert PIL image to opencv2 image and convert RGB to BGR
                opencv_new_image = cv2.cvtColor(numpy.asarray(new_img), cv2.COLOR_RGB2BGR)

                # add image to video
                video.write(opencv_new_image)

        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()
        video.release()

        # converting the video with moviepy also compresses it
        # add audio back to video
        original_video = mp.VideoFileClip(original_video_path)
        new_video = mp.VideoFileClip(video_file_path)
        # if we keep the audio add it here
        if has_audio:
            new_video.audio = original_video.audio

        # set the audio codec to Advanced Audio Coding (aac) to play on phones
        new_video.write_videofile(save_file_path, audio_codec='aac')

        # remove the video only file
        os.remove(video_file_path)

        return [True, "Finished Creating Ascii Video"]


class ASCIIImage:
    def __init__(self):
        pass

    def generate_ascii_image(self, path, quality, is_colored):
        # checks if the path is proper otherwise returns an error
        try:
            pic = imageio.imread(path)
        except ValueError:
            return [False, "File path does not lead to an image"]
        height = int(format(pic.shape[0]))
        width = int(format(pic.shape[1]))

        # creates the new image with the correct sizing
        font = ImageFont.load_default()
        l_width = font.getsize("x")[0]
        l_height = font.getsize("$")[1]
        new_img = Image.new("RGB", (int((width * l_width) / quality), int((height * l_height) / (2 * quality))),
                            'black')
        draw = ImageDraw.Draw(new_img)

        y_height = 0

        # set the ascii chars for the image
        # set the ascii chars for the image
        for i in range(height):
            if i % (quality * 2) == 0:
                text = ''
                y_width = 0
                for x in range(width):
                    if x % quality == 0:
                        ascii_char = ascii_dict[int((int(format(pic[i, x, 0])) + int(
                            format(pic[i, x, 1])) + int(format(pic[i, x, 2]))) / 3)]
                        text += ascii_char

                        # set fill to black if no color otherwise set the color to the given pixels color
                        fill = (pic[i, x, 0], pic[i, x, 1], pic[i, x, 2]) if is_colored else (255, 255, 255)

                        # colors the cell
                        draw.text((y_width, y_height), ascii_char, font=font, fill=fill)
                        y_width += l_width
                y_height += l_height

        # returns a successful gen and the created img
        return [True, new_img]
