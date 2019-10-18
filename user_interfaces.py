from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider,
    QStyle,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction, QDialog
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtMultimedia
from PyQt5 import QtCore
import sys
import os
import uuid
import pandas as pd
import logging

# I hate this, but this is what you get when youre sleepy, but wants to get it done
exp_counter = 0


class MainWindow(QMainWindow):
    def __init__(self, data, id):
        super(MainWindow, self).__init__()
        self.data = data
        self.id = id
        uic.loadUi("user_interfaces/main_window.ui", self)
        self.start_button.clicked.connect(self.openOtherForm)

        self.gender_box.clear()
        self.gender_box.addItems(
            ["Masculino", "Feminino", "Não Binário", "Outros", "Prefiro não informar"]
        )

        self.edu_lvl_box.clear()
        self.edu_lvl_box.addItems(
            [
                "Superior Completo",
                "Superior Incompleto",
                "Médio Completo",
                "Médio Incompleto",
                "Fundamental Completo",
                "Fundamental Incompleto",
            ]
        )

        self.age_range_box.clear()
        self.age_range_box.addItems(
            [
                "18 a 25 anos",
                "26 a 35 anos",
                "36 a 45 anos",
                "46 a 55 anos",
                "56 a 65 anos",
                "66 a 75 anos",
                "76 a 85 anos",
                "86 + anos",
            ]
        )

        self.start_button.setEnabled(False)

        self.tcle_ok.toggled.connect(
            lambda: self.start_button.setEnabled(self.tcle_ok.isChecked())
        )

    def openOtherForm(self):
        # TODO: make a standard function to advance to the desired screen, to make the sequence random
        collected_data = {
            "id": self.id,
            "name": self.name_input.toPlainText(),
            "gender": self.gender_box.currentText(),
            "edu": self.edu_lvl_box.currentText(),
            "age": self.age_range_box.currentText(),
        }
        logging.info(collected_data)
        print(collected_data)

        self.data = self.data.append(collected_data, ignore_index=True)
        # JSON would make more sense, but lets try a csv for now
        save_df(self.data)
        self.hide()
        otherview = next_test(self)
        otherview.show()


class VideoCompWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("user_interfaces/comparison_player.ui", self)
        self.player_1 = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface
        )
        self.player_2 = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface
        )
        file = os.path.join(os.path.dirname(__file__), "test.mp4")
        self.player_1.setMedia(
            QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file))
        )
        self.player_1.setVideoOutput(self.ui.video_player_1)
        self.player_1.play()

        file = os.path.join(os.path.dirname(__file__), "test2.mp4")
        self.player_2.setMedia(
            QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file))
        )
        self.player_2.setVideoOutput(self.ui.video_player_2)
        self.player_2.play()

        self.next_button.setEnabled(False)
        self.confirm_button.clicked.connect(lambda: self.next_button.setEnabled(True))

        self.next_button.clicked.connect(self.openNextScreen)

        self.play_button.clicked.connect(self.reset_video)

    def openNextScreen(self):
        self.hide()
        otherview = next_test(self)
        global exp_counter
        exp_counter += 1
        otherview.show()

    def reset_video(self):
        self.player_1.setPosition(1)
        self.player_2.setPosition(1)


class VideoSingleWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.ui = uic.loadUi("user_interfaces/single_player.ui", self)
        self.player_1 = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface
        )
        file = os.path.join(os.path.dirname(__file__), "test.mp4")
        self.player_1.setMedia(
            QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file))
        )
        self.player_1.setVideoOutput(self.ui.video_player_1)
        self.player_1.play()
        self.next_button.setEnabled(False)
        self.confirm_button.clicked.connect(lambda: self.next_button.setEnabled(True))

        self.play_button.clicked.connect(self.reset_video)

        self.next_button.clicked.connect(self.openNextScreen)

    def openNextScreen(self):
        self.hide()
        otherview = next_test(self)
        global exp_counter
        exp_counter += 1
        otherview.show()

    def reset_video(self):
        self.player_1.setPosition(1)


class EndWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.ui = uic.loadUi("user_interfaces/end_window.ui", self)
        self.end_button.clicked.connect(self.close)


def init_experiment():
    id = uuid.uuid4().__str__()
    data = pd.DataFrame(columns=["id", "name", "gender", "edu", "age", "v1"])
    logging.basicConfig(
        filename="app.log",
        filemode="a",
        level=logging.DEBUG,
        format="%(asctime)s -  %(levelname)s - %(message)s",
    )

    return id, data


def save_df(data):
    print(data["id"][0])
    data.to_csv(data["id"][0] + ".csv", index=False)


def next_test(self):

    if exp_counter < 1:
        otherview = VideoSingleWindow(self)
    elif exp_counter < 3:
        otherview = VideoCompWindow(self)
    else:
        otherview = EndWindow(self)
    return otherview


if __name__ == "__main__":
    id, data = init_experiment()
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(data, id)
    w.show()

    sys.exit(app.exec())
