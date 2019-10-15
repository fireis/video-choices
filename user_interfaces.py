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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
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
        # TODO: save the data to file
        collected_data = [
            self.name_input.toPlainText(),
            self.gender_box.currentText(),
            self.edu_lvl_box.currentText(),
            self.age_range_box.currentText(),
        ]
        print(collected_data)
        self.hide()

        otherview = VideoCompWindow(self)
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

    def openNextScreen(self):
        self.hide()
        otherview = VideoSingleWindow(self)
        otherview.show()


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

        self.next_button.clicked.connect(self.openNextScreen)

    def openNextScreen(self):
        self.hide()
        otherview = VideoSingleWindow(self)
        otherview.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
