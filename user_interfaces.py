from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
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
        uic.loadUi('user_interfaces/main_window.ui', self)
        self.button1.clicked.connect(self.openOtherForm)

    def openOtherForm(self):
        # TODO: make a standard function to advance to the desired screen, to make the sequence random
        self.hide()
        otherview = VideoCompWindow(self)
        otherview.show()


class VideoCompWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("user_interfaces/comparisson_player.ui", self)
        self.player_1 = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface)
        self.player_2 = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface)
        file = os.path.join(os.path.dirname(__file__), "test.mp4")
        self.player_1.setMedia(QtMultimedia.QMediaContent(
            QtCore.QUrl.fromLocalFile(file)))
        self.player_1.setVideoOutput(self.ui.video_player_1)
        self.player_1.play()

        file = os.path.join(os.path.dirname(__file__), "test2.mp4")
        self.player_2.setMedia(QtMultimedia.QMediaContent(
            QtCore.QUrl.fromLocalFile(file)))
        self.player_2.setVideoOutput(self.ui.video_player_2)
        self.player_2.play()

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
            None, QtMultimedia.QMediaPlayer.VideoSurface)
        file = os.path.join(os.path.dirname(__file__), "test.mp4")
        self.player_1.setMedia(QtMultimedia.QMediaContent(
            QtCore.QUrl.fromLocalFile(file)))
        self.player_1.setVideoOutput(self.ui.video_player_1)
        self.player_1.play()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
