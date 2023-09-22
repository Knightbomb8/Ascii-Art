import math
import cv2
import os
import numpy
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp
import time

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

# ascii_dict = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '"', '"', '"', '"', '"', '"', '"', '"', '"', '"', '"', '"', '"', '"', '"', '"', '"', '"', '"', '*', '*', '*', '*', '!', '!', '!', '!', '!', '!', '!', '!', 'I', 'I', 'I', 'I', 'I', 'I', '|', '|', '(', '(', ')', ')', ')', ')', ')', '}', '}', '}', '}', '}', '{', '{', '{', '{', '{', 'z', 'z', 'z', 'z', 'z', 'z', 'z', 'y', 'y', 'T', 'T', 'T', 'T', 'o', 'o', 'o', 'o', 'Y', 'F', '4', '4', '4', '4', '4', 'V', 'V', 'V', 'V', 'p', '3', '3', '2', '2', 'q', 'q', 'q', '0', '0', '0', '5', '5', 'C', 'C', 'C', 'Z', 'U', 'U', 'X', 'H', 'H', 'P', '#', '#', '#', 'S', 'S', 'S', 'S', 'S', 'E', 'E', 'E', 'O', 'O', 'O', 'O', '$', '$', '$', 'D', 'D', '&', '&', '%', '%', 'R', 'R', 'R', 'Q', 'Q', 'Q', 'Q', 'Q', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@']
# TODO add param for custom res while keeping same quality
def create_ascii_image(cv2_image, quality, is_colored):
    """
    Generates an ascii equivalent of an image. \n
    Returns PIL image \n
    :param cv2_image:
    :param quality:
    :param is_colored:
    :return:
    """
    # gets the image width and height
    image_height = cv2_image.shape[0]
    image_width = cv2_image.shape[1]

    # creates the new image with the correct sizing
    font = ImageFont.load_default()
    char_width = font.getsize("x")[0]
    char_height = font.getsize("$")[1]

    # create a new img
    new_img = Image.new("RGB", (math.ceil((image_width * char_width) / quality), math.ceil((image_height * char_height)
                                                                               / (2 * quality))), 'black')
    # add a drawing to the image
    draw = ImageDraw.Draw(new_img)

    y_height = 0

    # set the ascii chars for the image
    # set the ascii chars for the image
    for i in range(image_height):
        if i % (quality * 2) == 0:
            text = ''
            y_width = 0
            for x in range(image_width):
                if x % quality == 0:
                    # get greyscale val
                    grey_scale_val = int((int(format(cv2_image[i, x, 0])) + int(format(cv2_image[i, x, 1])) + int(format(cv2_image[i, x, 2]))) / 3)

                    ascii_char = ascii_dict[int(grey_scale_val)]
                    text += ascii_char

                    # set fill to black if no color otherwise set the color to the given pixels color
                    fill = (cv2_image[i, x, 2], cv2_image[i, x, 1], cv2_image[i, x, 0]) if is_colored \
                        else (255, 255, 255)

                    # colors the cell
                    draw.text((y_width, y_height), ascii_char, font=font, fill=fill)
                    y_width += char_width
            y_height += char_height

    # return the new image
    return new_img


# TODO add multi threading on image creation
class ASCIIVideo:
    def __init__(self):
        pass

    def generate_ascii_video(self, original_video_path, quality, save_file_path, is_colored, has_audio):
        """
        generates a ascii video at th save_file_path taking the video at original_video_path
        :param original_video_path:
        :param quality:
        :param save_file_path:
        :param is_colored:
        :param has_audio:
        :return:
        """
        start_video = time.time()
        # gets a reference to the video and fps
        cam = cv2.VideoCapture(original_video_path)
        fps = cam.get(cv2.CAP_PROP_FPS)

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


        # frame counter
        frame_count = 0
        keep_reading = True

        start_generating_ascii_images = time.time()
        # keep reading the video until no more frames
        while keep_reading:
            # read the image
            keep_reading, frame = cam.read()

            # if an image was found
            if keep_reading:
                # add to the total count
                frame_count += 1

                # create the ascii image
                new_img = create_ascii_image(frame, quality, is_colored)

                # convert PIL image to opencv2 image and convert RGB to BGR
                opencv_new_image = cv2.cvtColor(numpy.asarray(new_img), cv2.COLOR_RGB2BGR)

                # add image to video
                video.write(opencv_new_image)

        end_generating_ascii_images = time.time()

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

        end_video = time.time()
        print("Total time to make video: " + str(int(end_video - start_video)))
        print("Time to generate ascii images: " + str(int(end_generating_ascii_images - start_generating_ascii_images)))

        return [True, "Finished Creating Ascii Video"]


class ASCIIImage:
    def __init__(self):
        pass

    def generate_ascii_image(self, path, quality, is_colored):
        """
        generates an ascii image of the image at the given path \n
        :param path:
        :param quality:
        :param is_colored:
        :return:
        """
        # checks if the path is proper otherwise returns an error
        try:
            pic = cv2.imread(path)
        except ValueError:
            return [False, "File path does not lead to an image"]

        # create the ascii image
        new_img = create_ascii_image(pic, quality, is_colored)

        # returns a successful gen and the created img
        return [True, new_img]
