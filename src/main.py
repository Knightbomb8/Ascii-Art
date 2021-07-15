from __future__ import print_function    # (at top of module)
import sys
import os.path
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)
from AsciiGUIElements import *
from ASCIIGenerators import *


# create a window
def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


# stores data for the main window the gui generates
class Window(QMainWindow):
    # given a path returns the first available path name not taken
    def get_first_valid_path(self, path, file_extension):
        # if the path does not exist return original path
        if not os.path.isfile(path + file_extension):
            return path + file_extension

        # check the first available file name
        iterations = 1
        while os.path.isfile(path + "(" + str(iterations) + ")" + file_extension):
            iterations += 1

        # return said file name
        return path + "(" + str(iterations) + ")" + file_extension

    # TODO make the ascii image on a sep thread
    # TODO make a progress bar for generation
    def generate_ascii_image(self, path, quality, is_colored):
        """
        generates an ascii image at the specific path at the given quality (1-10)
        Returns error string if something went wrong
        :param path:
        :param quality:
        :return:
        """
        successful_completion, data = self.ascii_image_gen.generate_ascii_image(path, 11 - quality, is_colored)

        # if not a successful image generation return the data denoting the error string
        if not successful_completion:
            return [False, data]

        file_save_name = QFileDialog.getSaveFileName()[0]
        # if the file name is not valid return the error string
        if file_save_name == "":
            return [False, "Invalid File name"]

        # save the file
        file_name = self.get_first_valid_path(file_save_name, ".jpg")
        data.save(file_name)

        # return successful status
        return [True, "Successfully generated an ascii image"]

    # add status updates for the video as they take a while to make
    # TODO make the ascii video on a sep thread
    # TODO make a progress bar for generation
    def generate_ascii_video(self, path, quality, is_colored, has_audio):
        file_save_name = QFileDialog.getSaveFileName()[0]
        # if the file name is not valid return the error string
        if file_save_name == "":
            return [False, "Invalid File name"]

        # get the path to save the movie at
        file_name = self.get_first_valid_path(file_save_name, ".mp4")

        # generate the movie
        if not path == "":
            results = self.ascii_video_gen.generate_ascii_video(path, 11 - quality, file_name, is_colored, has_audio)
        else:
            return [False, "Not a valid video path"]

        # return the results
        return results

    def __init__(self):
        self.window_height = 1920
        self.window_width = 1080

        # ascii generators
        self.ascii_image_gen = ASCIIImage()
        self.ascii_video_gen = ASCIIVideo()

        # initialize window
        super().__init__()
        self.setWindowTitle("Ascii Art Creator")
        self.resize(1920, 1080)

        # create central widget
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)

        # create the container object for all pieces
        self.outer_layout = QHBoxLayout()
        self.cw.setLayout(self.outer_layout)

        # create the two sections
        self.outer_layout.addWidget(AsciiImageGenerationSection("Ascii Image Generator", self.window_width,
                                                          "Images (*.png *.jpg)", self.generate_ascii_image))
        self.outer_layout.addWidget(AsciiVideoGenerationSection("Ascii Video Generator", self.window_width,
                                                          "Videos (*.mp4 *.mov)", self.generate_ascii_video))
        self.outer_layout.addStretch()


if __name__ == "__main__":
    main()
