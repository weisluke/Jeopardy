from PySide6.QtWidgets import QMainWindow, QPushButton
from PySide6.QtGui import QResizeEvent
from PySide6.QtCore import QUrl, QVariantAnimation, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import json
from pathlib import Path
from logo import Logo
from board import Board
from players import Players


class Jeopardy(QMainWindow):

    # state codes
    INTRO = 0
    FLIP_PLAYERS = 1
    FLIP_QUESTIONS = 2
    FLIP_CATEGORIES = 3
    FINAL_JEOPARDY = 4

    def __init__(self, file):
        QMainWindow.__init__(self)
        self.setWindowTitle("Jeopardy")

        with open(file) as f:
            self.dat = json.load(f)
        
        # make sure there is at least one round
        assert self.MAX_NUM_ROUNDS >= 1
        # check that the keys of the rounds are strings of integers
        # ranging from 1 to the maximum number of rounds
        assert (set([int(r) for r in self.dat['rounds'].keys()])
                == set(range(1, self.MAX_NUM_ROUNDS + 1)))
        self.round = 1

        # ensure that all categories have the same number of questions
        num_questions = [len(questions)
                         for round, categories in self.dat['rounds'].items()
                         for category, questions in categories.items()]
        assert all([n == num_questions[0] for n in num_questions])
        
        self.state = self.INTRO

        self.logo = Logo(self)

        self.players = Players(self, self.dat["players"])
        self.board = Board(self, 1, self.dat["rounds"]["1"])

        self.play = QPushButton("▶", self)
        self.play.setStyleSheet("""
            QPushButton {
                font-size: 30pt;
                font-weight: bold;
                font: 'Times New Roman';
                color: green;
                background-color: white;
                border: 2px solid gray;
                padding: 5px;
            }
        """)
        self.play.clicked.connect(self.update)

        # Initialize the player and the output device
        self.audio_output = QAudioOutput()
        self.audio_player = QMediaPlayer(audioOutput=self.audio_output)

        self.resize(1400,1000)
        self.show()

    def resizeEvent(self, event: QResizeEvent):
        self.logo.setGeometry(self.width() * 0.1, 0, 
                              self.width() * 0.5, self.height() * 0.25)
        self.players.setGeometry(self.width() * 0.7, 0,
                                 self.width() * 0.3, self.height())
        self.board.setGeometry(0, self.height() * 0.25,
                               self.width() * 0.7, self.height() * 0.75)
        
        self.play.setGeometry(self.width() * 0.025, self.height() * 0.1, 
                              self.width() * 0.05, self.height() * 0.05)

    @property
    def MAX_NUM_ROUNDS(self):
        return len(self.dat['rounds'])

    def next(self):
        if self.state <= self.FINAL_JEOPARDY:
            self.state += 1

    def update(self):
        match self.state:
            case self.INTRO:
                where = Path(__file__).parent
                self.audio_player.setSource(QUrl.fromLocalFile(f'{where}/sounds/intro.mp3'))
                self.audio_output.setVolume(1.0)

                # 10 second fadeout from full volume to silent
                self.fadeout = QVariantAnimation(duration=10000, startValue=1.0, endValue=0.0)
                self.fadeout.valueChanged.connect(self.audio_output.setVolume)
                self.fadeout.finished.connect(self.audio_player.stop)

                self.audio_player.play()
                # start fadeout after 10 seconds
                QTimer.singleShot(10000, self.fadeout.start)
                self.next()
            case self.FLIP_PLAYERS:
                if self.audio_player.isPlaying():
                    return
                self.fadeout = None
                self.players.flip_players()
                if not self.players.flipping_players:
                    self.next()
            case self.FLIP_QUESTIONS:
                where = Path(__file__).parent
                self.audio_player.setSource(QUrl.fromLocalFile(f'{where}/sounds/flip_questions.mp3'))
                self.audio_output.setVolume(1.0)
                self.audio_player.play()
                self.board.flip_questions()
                self.next()
            case self.FLIP_CATEGORIES:
                if self.board.flipping_questions:
                    return
                self.board.display.show()
                if self.board.flipping_categories:
                    self.board.flip_categories()
                    return
                self.board.display.hide()
                self.next()
            case self.FINAL_JEOPARDY:
                if self.audio_player.isPlaying():
                    return
                print("FINAL JEOPARDY!")
                self.next()
            case _:
                return
