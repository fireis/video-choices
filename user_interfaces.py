from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtMultimedia
from PyQt5 import QtCore
import sys
import os
import uuid
import pandas as pd
import logging
import time
import random
import glob
import pathlib

class MainWindow(QMainWindow):
    def __init__(self, id, pers_data, exp_data):
        super(MainWindow, self).__init__()
        self.start_time = time.time()
        self.pers_data = pers_data
        self.exp_data = exp_data
        self.uid = id
        self.exp_counter = 0
        self.window_type = "pers_info"
        self.single_count = 0
        self.comp_count = 0

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
        collected_pers_data = {
            "id": self.uid,
            "name": self.name_input.toPlainText(),
            "gender": self.gender_box.currentText(),
            "edu": self.edu_lvl_box.currentText(),
            "age": self.age_range_box.currentText(),
        }
        logging.info(collected_pers_data)
        self.pers_data = self.pers_data.append(collected_pers_data, ignore_index=True)

        collected_exp_data = {
            "id": self.uid,
            "type": self.window_type,
            "t0": self.start_time,
            "tf": time.time(),
        }
        logging.info(collected_exp_data)
        self.exp_data = self.exp_data.append(collected_exp_data, ignore_index=True)
        print(self.exp_data)

        save_df(self.pers_data, self.window_type)
        self.hide()
        otherview = next_test(self)
        otherview.show()


class VideoCompWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):

        self.exp_counter = parent.exp_counter
        self.times_played = 0
        self.uid = parent.uid
        self.window_type = "comp"
        self.start_time = time.time()
        self.exp_data = parent.exp_data
        self.single_count = parent.single_count
        self.comp_count = parent.comp_count + 1

        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("user_interfaces/comparison_player.ui", self)
        self.player_1 = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface
        )
        self.player_2 = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface
        )
        # TODO: make file choice so that picks a random video from A folder, other from B and ramdomly assign them to player 1 and 2
        file = os.path.join(os.path.dirname(__file__), "test.mp4")
        logging.info(f"Opening file: {file} as left video")
        self.player_1.setMedia(
            QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file))
        )
        self.player_1.setVideoOutput(self.ui.video_player_1)
        self.vid1 = file

        file = os.path.join(os.path.dirname(__file__), "test2.mp4")
        logging.info(f"Opening file: {file} as center video")
        self.player_2.setMedia(
            QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file))
        )
        self.player_2.setVideoOutput(self.ui.video_player_2)
        self.vid2 = file

        self.player_1.play()
        self.player_2.play()
        self.times_played += 1
        logging.info("Videos playing")

        self.next_button.setEnabled(False)
        self.confirm_button.clicked.connect(lambda: self.next_button.setEnabled(True))

        self.next_button.clicked.connect(self.openNextScreen)

        self.play_button.clicked.connect(lambda: self.reset_video())

    def openNextScreen(self):
        collected_exp_data = {
            "id": self.uid,
            "type": self.window_type,
            "vid1": self.vid1,
            "vid2": self.vid2,
            "v1_opt": self.choose_video1.isChecked(),
            "v2_opt": self.choose_video2.isChecked(),
            "t0": self.start_time,
            "tf": time.time(),
            "replays": self.times_played,
        }
        logging.info(collected_exp_data)
        self.exp_data = self.exp_data.append(collected_exp_data, ignore_index=True)
        print(self.exp_data)
        save_df(self.exp_data, self.window_type)

        self.hide()
        self.exp_counter += 1
        otherview = next_test(self)
        otherview.show()

    def reset_video(self):
        self.player_1.setPosition(1)
        self.player_2.setPosition(1)
        self.times_played += 1
        logging.info("Reset Video Button Clicked")


class VideoSingleWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.exp_counter = parent.exp_counter
        self.times_played = 0
        self.uid = parent.uid
        self.window_type = "single"
        self.start_time = time.time()
        self.order = "01091322"
        self.exp_data = parent.exp_data
        self.single_count = parent.single_count + 1
        self.comp_count = parent.comp_count

        self.ui = uic.loadUi("user_interfaces/single_player.ui", self)
        self.write_emotion_labels()
        self.player_1 = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface
        )
        file = os.path.join(os.path.dirname(__file__), "/videos/emotion_def/")
        # print(file)
        # print(find_videos_on_folder("videos/emotion_def/"))
        file = random.choice(
            find_videos_on_folder(file)
        )
        self.player_1.setMedia(
            QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file))
        )
        self.vid1 = file
        self.player_1.setVideoOutput(self.ui.video_player_1)
        self.player_1.play()
        self.times_played += 1
        logging.info("Videos playing")

        self.next_button.setEnabled(False)
        self.confirm_button.clicked.connect(lambda: self.next_button.setEnabled(True))

        self.play_button.clicked.connect(lambda: self.reset_video())

        self.next_button.clicked.connect(self.openNextScreen)

    def write_emotion_labels(self):
        emotions = ["Anger", "Admiration", "Fear", "Happy-for"]
        random.shuffle(emotions)
        self.choose_emot_1.setText(emotions[0])
        self.choose_emot_2.setText(emotions[1])
        self.choose_emot_3.setText(emotions[2])
        self.choose_emot_4.setText(emotions[3])

    def openNextScreen(self):
        # TODO: adjust emots and order to represent the actual labls displayed on the screen
        collected_exp_data = {
            "id": self.uid,
            "type": self.window_type,
            "vid1": self.vid1,
            "b1": (self.choose_emot_1.isChecked(), self.choose_emot_1.text()),
            "b2": (self.choose_emot_2.isChecked(), self.choose_emot_2.text()),
            "b3": (self.choose_emot_3.isChecked(), self.choose_emot_3.text()),
            "b4": (self.choose_emot_4.isChecked(), self.choose_emot_4.text()),
            "t0": self.start_time,
            "tf": time.time(),
            "replays": self.times_played,
            "order": self.order,
        }
        logging.info(collected_exp_data)
        self.exp_data = self.exp_data.append(collected_exp_data, ignore_index=True)
        print(self.exp_data)
        save_df(self.exp_data, self.window_type)

        self.hide()
        save_window_data(self)
        self.exp_counter += 1
        otherview = next_test(self)
        # global exp_counter
        otherview.show()

    def reset_video(self):
        self.player_1.setPosition(1)
        self.times_played += 1
        logging.info("Reset Video Button Clicked")


class EndWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.ui = uic.loadUi("user_interfaces/end_window.ui", self)
        self.end_button.clicked.connect(self.close)


def save_window_data(obj):
    print(obj.times_played)


def init_experiment():
    id = uuid.uuid4().__str__()
    pers_data = pd.DataFrame(columns=["id", "name", "gender", "edu", "age"])
    exp_data = pd.DataFrame(
        columns=[
            "id",
            "type",
            "vid1",
            "vid2",
            "em1",
            "em9",
            "em13",
            "em22",
            "v1_opt",
            "v2_opt",
            "t0",
            "tf",
            "replays",
            "order",
        ]
    )
    logging.basicConfig(
        filename="app.log",
        filemode="a",
        level=logging.DEBUG,
        format="%(asctime)s -  %(levelname)s - %(message)s",
    )
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    return id, pers_data, exp_data


def save_df(data, window_type):
    print(data["id"][0])
    if window_type == "pers_info":
        data.to_csv(data["id"][0] + ".csv", index=False)
    elif window_type == "single" or window_type == "comp":
        data.to_csv(f"exp_{data['id'][0]}.csv", index=False)


def find_videos_on_folder(path):
    """
    searches the input path for videos and returns a list with the found content
    :param path: in which the videos should be found
    :return: list with paths for available videos
    """
    videos = glob.glob(path + "*.mp4")
    # videos = pathlib.Path.glob(path, "*.mp4" )
    # videos = [x for x in videos if x.is_file()]

    return videos


def next_test(self):
    """
    assures the sequence of screens is random while respecting the max of interaction
    """
    experiment_choice = random.choice(["single", "comp"])
    individual_max = 3
    if self.single_count + self.comp_count < individual_max * 2:
        if (
            experiment_choice == "single" and self.single_count < individual_max
        ) or self.comp_count >= individual_max:
            return VideoSingleWindow(self)
        elif (
            experiment_choice == "comp" and self.comp_count < individual_max
        ) or self.single_count >= individual_max:
            return VideoCompWindow(self)
    return EndWindow(self)


if __name__ == "__main__":
    id, pers_data, exp_data = init_experiment()
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(id, pers_data, exp_data)
    w.show()

    sys.exit(app.exec())
