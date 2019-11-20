from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QRadioButton
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
        # TODO: CLEAN THIS MESS
        # WARNING: THIS COMMIT SUX BUT WORKS FOR THE TEST
        # self.emo_okp_car_vem_count = 0
        # self.emo_okp_edu_vem_count = 0
        # self.emo_hmm_vem_count = 0
        # self.syn_car_vem_v2v_count = 0
        # self.emo_hmm_vem = 0
        # self.syn_vem_hmm_v2v_count = 0
        # self.syn_hmm_vem_v2v_count = 0
        # self.syn_car_vem_v2v = 0
        # self.syn_hmm_vem_v2v_aud_count = 0
        # self.exp_choices = ["emo_okp_car_vem", "emo_okp_edu_vem", "emo_hmm_vem", "syn_car_vem_v2v", "syn_hmm_vem_v2v", "syn_hmm_vem_v2v_aud"]

        path = os.path.join(os.path.dirname(__file__), "videos/")

        self.comp_experiments = glob.glob(path + "comp" + "/*/*.mp4")
        random.shuffle(self.comp_experiments)
        self.single_experiments = glob.glob(path + "single" + "/*/*.mp4")
        random.shuffle(self.single_experiments)

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
        self.comp_experiments = parent.comp_experiments
        self.single_experiments = parent.single_experiments

        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("user_interfaces/comparison_player.ui", self)
        self.player_1 = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface
        )

        vid_l = self.comp_experiments.pop()
        logging.info(f"Opening file: {vid_l} as left video")
        self.player_1.setMedia(
            QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(vid_l))
        )
        self.player_1.setVideoOutput(self.ui.video_player_1)
        self.vid1 = vid_l

        self.player_1.play()
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
            "v1_opt": self.choose_video1.isChecked(),
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
        # self.player_2.setPosition(1)
        self.player_1.play()
        # self.player_2.play()
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

        self.exp_data = parent.exp_data

        self.comp_experiments = parent.comp_experiments
        self.single_experiments = parent.single_experiments

        self.ui = uic.loadUi("user_interfaces/single_player.ui", self)
        self.order = self.write_emotion_labels()
        self.player_1 = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface
        )

        vid1 = self.single_experiments.pop()
        self.player_1.setMedia(
            QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(vid1))
        )
        self.vid1 = vid1
        self.player_1.setVideoOutput(self.ui.video_player_1)
        self.player_1.play()
        self.times_played += 1
        logging.info("Videos playing")

        self.next_button.setEnabled(False)
        self.confirm_button.clicked.connect(lambda: self.next_button.setEnabled(True))

        self.play_button.clicked.connect(lambda: self.reset_video())

        self.next_button.clicked.connect(self.openNextScreen)

    def write_emotion_labels(self):
        emotions = ["Com Raiva", "Admirada", "Amedrontada", "Feliz por alguém"]
        random.shuffle(emotions)
        self.choose_emot_1.setText(emotions[0])
        self.choose_emot_2.setText(emotions[1])
        self.choose_emot_3.setText(emotions[2])
        self.choose_emot_4.setText(emotions[3])
        return emotions

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
        otherview.show()

    def reset_video(self):
        self.player_1.setPosition(1)
        self.player_1.play()
        self.times_played += 1
        logging.info("Reset Video Button Clicked")


class VideoSingleWindow_emo_okp_car_vem(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.exp_counter = parent.exp_counter
        self.times_played = 0
        self.uid = parent.uid
        self.window_type = "single"
        self.start_time = time.time()

        self.exp_data = parent.exp_data
        self.single_count = parent.single_count + 1
        self.comp_count = parent.comp_count
        self.emo_okp_car_vem_count = parent.emo_okp_car_vem_count + 1
        self.emo_okp_edu_vem_count = parent.emo_okp_edu_vem_count
        self.emo_hmm_vem_count = parent.emo_hmm_vem_count
        self.syn_car_vem_v2v_count = parent.syn_car_vem_v2v_count
        self.syn_hmm_vem_v2v_count = parent.syn_hmm_vem_v2v_count
        self.syn_hmm_vem_v2v_aud_count = parent.syn_hmm_vem_v2v_aud_count
        self.emo_hmm_vem = parent.emo_hmm_vem
        self.syn_car_vem_v2v = parent.syn_car_vem_v2v
        self.exp_choices = parent.exp_choices

        self.ui = uic.loadUi("user_interfaces/single_player.ui", self)
        self.order = self.write_emotion_labels()
        self.player_1 = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface
        )
        file = os.path.join(os.path.dirname(__file__), "videos/emo_okp_car_vem/")
        file = find_videos_on_folder(file, ab=False)
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
        return emotions

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
        otherview, self = next_test(self)
        otherview.show()

    def reset_video(self):
        self.player_1.setPosition(1)
        self.player_1.play()
        self.times_played += 1
        logging.info("Reset Video Button Clicked")


class EndWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.ui = uic.loadUi("user_interfaces/end_window.ui", self)
        self.end_button.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        comments = self.comments.toPlainText()
        logging.info(comments)
        self.close()


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
        level=logging.INFO,
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


def find_videos_on_folder(path, ab):
    """
    searches the input path for videos and returns one or two randomly selected videos
    :param path: in which the videos should be found
    :param ab: if true, return two videos from folders a and b
    :return: list with paths for available videos
    """
    # TODO: fix as this doesnt work on mac
    if ab:
        video_a = random.choice(glob.glob(path + "A/*/*.mp4"))
        video_b = video_a.replace("/A", "/B")
        videos = [video_a, video_b]
        random.shuffle(videos)
        return videos[0], videos[1]
    else:
        print(glob.glob(path + "*.mp4"))
        video = random.choice(glob.glob(path + "*.mp4"))
        return video


def next_test(self):
    """
    assures the sequence of screens is random while respecting the max of interaction
    """
    next = random.choice(["comp", "single"])
    if next == "comp" and len(self.comp_experiments) > 19:
        return VideoCompWindow(self)
    elif len(self.single_experiments) > 29:
        return VideoSingleWindow(self)

    return EndWindow(self)


if __name__ == "__main__":
    id, pers_data, exp_data = init_experiment()
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(id, pers_data, exp_data)
    w.show()

    sys.exit(app.exec())
