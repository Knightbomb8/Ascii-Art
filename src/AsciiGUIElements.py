from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QCheckBox,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
    QSlider
)


class __AsciiSection(QWidget):
    def __init__(self):
        pass

    # creates a QLabel object
    def create_label(self, text, parent, alignment=Qt.AlignLeft, wrap_text=True):
        """
        creates a QLabel object with the given text and adds the QLabel to parent
        returns QLabel \n
        :param text:
        :param parent:
        :param alignment:
        :param wrap_text:
        :return:
        """
        # creates the label
        new_label = QLabel()
        new_label.setAlignment(alignment)
        new_label.setWordWrap(wrap_text)
        new_label.setText(text)
        parent.addWidget(new_label)

        return new_label

    # create a QPushButton object
    def create_push_button(self, text, parent, tooltip=""):
        """
        creates a new QPushButton and adds it to the specified parent
        returns QPushButton \n
        :param text:
        :param parent:
        :param tooltip:
        :return:
        """
        # create the button
        new_button = QPushButton()
        new_button.setText(text)
        new_button.setToolTip(tooltip)
        parent.addWidget(new_button)

        return new_button

    # create a QCheckBox object
    def create_slider(self, min, max, label_text, parent, orientation=Qt.Orientation.Horizontal):
        """
        creates a QSlider with a label on the left
        returns [QCheckBox, QLabel] \n
        :param min:
        :param max:
        :param label_text:
        :param parent:
        :param orientation:
        :return:
        """
        # create the label
        new_label = self.create_label(label_text, parent)
        # create the slider
        new_slider = QSlider()
        new_slider.setOrientation(orientation)
        new_slider.setMinimum(min)
        new_slider.setMaximum(max)
        parent.addWidget(new_slider)

        return [new_label, new_slider]

    # create a QSlider object
    def create_check_box(self, text, parent):
        """
        creates a QCheckBox with the given text
        returns QCheckBox \n
        :param text:
        :param parent:
        :return:
        """
        new_check_box = QCheckBox()
        new_check_box.setText(text)
        parent.addWidget(new_check_box)

        return new_check_box

    # sets the generation message
    def set_generation_state(self, info, generation_message_display):
        """
        sets the state of a text given the info \n
        TODO refactor this explanaton
        :param info:
        :param generation_message_display:
        :return:
        """
        # parse the info out then set the message accordingly
        successful, message = info
        if successful:
            generation_message_display.setStyleSheet("color: green")
        else:
            generation_message_display.setStyleSheet("color: red")
        generation_message_display.setText(message)

    # handles the select file push button
    def select_file_handler(self, file_display, media_filter):
        """
        sets the selected file location for the user \n
        :param file_display:
        :param media_filter:
        :return:
        """
        file_explorer_dialog = QFileDialog()
        file_location = file_explorer_dialog.getOpenFileName(filter=media_filter)[0]
        # if no file returned return
        if file_location == "":
            return
        # else update the file and shown text
        file_display.setText(file_location)


# container for the ascii video gen
class AsciiImageGenerationSection(__AsciiSection):
    def __init__(self, title, width, media_filter, media_generator):
        # init the super
        QWidget.__init__(self)
        self.v_box = QVBoxLayout()
        self.setLayout(self.v_box)
        self.setFixedWidth(width)

        # set some default values
        self.media_filter = media_filter

        # add title label
        self.title = self.create_label(title, self.v_box,Qt.AlignCenter)

        self.select_file_section = QHBoxLayout()
        self.v_box.addLayout(self.select_file_section)

        # add select file for importing
        self.select_file_button = self.create_push_button("Select File", self.select_file_section,
                                                          "Acceptable Files: " + self.media_filter)

        # add text to show the selected file
        self.selected_file_display = self.create_label("", self.select_file_section)
        self.selected_file_display.setStyleSheet("border: 3px solid grey;")

        # add the event for when the user clicks to select a file
        self.select_file_button.clicked.connect(lambda e: self.select_file_handler(self.selected_file_display,
                                                                                   media_filter))

        # add quality slider
        self.set_quality_section = QHBoxLayout()
        self.v_box.addLayout(self.set_quality_section)
        self.quality_label, self.quality_slider = self.create_slider(1, 10, "Quality: 1", self.set_quality_section)

        # handle the event when the slider moves
        self.quality_slider.valueChanged.connect(lambda e: self.quality_label.setText("Quality: " + str(e)))

        # add the color checkbox
        self.color_check_box = self.create_check_box("Add Color?", self.v_box)

        # add spacing
        self.v_box.addSpacing(50)

        # description for what happens when you click the "Generate ascii art button"
        description_text = "Upon clicking the below button, the program will generate the requested art " \
                           "and then open a file manager. Navigate to where you want to " \
                           "save the file, enter a name and hit save."
        self.generation_description = self.create_label(description_text, self.v_box, Qt.AlignCenter)

        # add generate file button
        self.generate_art_button = self.create_push_button("Generate Ascii Art", self.v_box)

        # add label to show ascii image generation errors
        self.generation_message = self.create_label("", self.v_box, Qt.AlignCenter)

        # add the event that occurs on final gen
        self.generate_art_button.clicked.connect(lambda e: self.set_generation_state(media_generator(
            self.selected_file_display.text(), int(self.quality_label.text().split(':')[1].strip()),
            self.color_check_box.checkState()), self.generation_message))

        # add a stretch at the end to set each element as a finite height
        self.v_box.addStretch()


# container for the ascii video gen
class AsciiVideoGenerationSection(__AsciiSection):
    def __init__(self, title, width, media_filter, media_generator):
        # init the super
        QWidget.__init__(self)
        self.v_box = QVBoxLayout()
        self.setLayout(self.v_box)
        self.setFixedWidth(width)

        # set some default values
        self.media_filter = media_filter

        # add title label
        self.title = self.create_label(title, self.v_box, Qt.AlignCenter)

        self.select_file_section = QHBoxLayout()
        self.v_box.addLayout(self.select_file_section)

        # add select file for importing
        self.select_file_button = self.create_push_button("Select File", self.select_file_section,
                                                          "Acceptable Files: " + self.media_filter)

        # add text to show the selected file
        self.selected_file_display = self.create_label("", self.select_file_section)
        self.selected_file_display.setStyleSheet("border: 3px solid grey;")

        # add the event for when the user clicks to select a file
        self.select_file_button.clicked.connect(lambda e: self.select_file_handler(self.selected_file_display,
                                                                                   media_filter))

        # add quality slider
        self.set_quality_section = QHBoxLayout()
        self.v_box.addLayout(self.set_quality_section)
        self.quality_label, self.quality_slider = self.create_slider(1, 10, "Quality: 1", self.set_quality_section)

        # handle the event when the slider moves
        self.quality_slider.valueChanged.connect(lambda e: self.quality_label.setText("Quality: " + str(e)))

        # add the color checkbox
        self.color_check_box = self.create_check_box("Add Color?", self.v_box)

        self.sound_check_box = self.create_check_box("Add Sound?", self.v_box)

        # add spacing
        self.v_box.addSpacing(50)

        # description for what happens when you click the "Generate ascii art button"
        description_text = "Upon clicking the below button, the program will generate the requested art " \
                           "and then open a file manager. Navigate to where you want to " \
                           "save the file, enter a name and hit save."
        self.generation_description = self.create_label(description_text, self.v_box, Qt.AlignCenter)

        # add generate file button
        self.generate_art_button = self.create_push_button("Generate Ascii Art", self.v_box)

        # add label to show ascii image generation errors
        self.generation_message = self.create_label("", self.v_box, Qt.AlignCenter)

        # add the event that occurs on final gen
        self.generate_art_button.clicked.connect(lambda e: self.set_generation_state(media_generator(
            self.selected_file_display.text(), int(self.quality_label.text().split(':')[1].strip()),
            self.color_check_box.checkState(), self.sound_check_box.checkState()), self.generation_message))

        # add a stretch at the end to set each element as a finite height
        self.v_box.addStretch()
