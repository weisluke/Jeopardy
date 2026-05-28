from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from pathlib import Path


class FinalJeopardy(QLabel):

    UNFLIPPED = 0
    CATEGORY = 1
    QUESTION = 2
    ANSWERING = 3
    ANSWER = 4

    def __init__(self, parent, dat):
        QLabel.__init__(self, "Final Jeopardy", parent,
                        scaledContents=True,
                        alignment=(Qt.AlignVCenter | Qt.AlignHCenter),
                        wordWrap=True)
        self.setStyleSheet("""
            QLabel {
                font-size: 60pt;
                font-weight: bold;
                font: 'Times New Roman';
                color: white;
                background-color: blue;
                border: 2px solid black;
                padding: 0px;
            }
        """)
        
        for category, what in dat.items():
            self.category = category
            for question, answer in what.items():
                self.question = question
                self.answer = answer

        self.state = self.UNFLIPPED
        self.hide()

        self.audio_output = QAudioOutput()
        self.audio_player = QMediaPlayer(audioOutput=self.audio_output)

        where = Path(__file__).parent
        self.audio_player.setSource(QUrl.fromLocalFile(f'{where}/sounds/final_jeopardy.mp3'))
        self.audio_output.setVolume(1.0)

    def next(self):
        # don't advance if answering questions and music is playing
        if (self.state == self.ANSWERING and
                self.audio_player.isPlaying()):
            return
        if self.state <= self.ANSWER:
            self.state += 1
        self.update()

    def update(self):
        match self.state:
            case self.UNFLIPPED:
                return
            case self.CATEGORY:
                self.setText(self.category)
            case self.QUESTION:
                self.setText(self.question)
            case self.ANSWERING:
                self.audio_player.play()
            case self.ANSWER:
                self.setText(self.answer)
            case _:
                self.setText('Thanks for playing!')
