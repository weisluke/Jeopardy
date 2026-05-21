from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtCore import QRect, QTimer, QUrl, QEventLoop
from PySide6.QtMultimedia import QMediaPlayer
from category import Category
from question import Question
from pathlib import Path
import numpy as np


class Board(QFrame):

    def __init__(self, parent, round, dat):
        QFrame.__init__(self, parent)
        self.setStyleSheet("""
            QFrame {
                border: 2px solid gray;
                padding: 5px;
            }
        """)

        where = Path(__file__).parent
        self.pixmap = QPixmap(f'{where}/jeopardy.png')

        self.round = round
        # dictionary of {category: {question: answer}, ...}
        self.dat = dat

        self.categories = []
        for category, questions in self.dat.items():
            self.categories.append(Category(self, category, questions))

        width = self.pixmap.width() / self.num_categories
        for i, category in enumerate(self.categories):
            height = self.pixmap.height() / category.num_questions
            for j, question in enumerate(category.questions):
                rect = QRect(width * i, height * j, width, height)
                question.setPixmap(self.pixmap.copy(rect))
   
    def resizeEvent(self, event: QResizeEvent):
        dw = self.width() / self.num_categories
        for i, category in enumerate(self.categories):
            category.setGeometry(dw * i, 0, dw, self.height())

    @property
    def num_categories(self):
        return len(self.dat)

    @property
    def num_questions(self):
        n = [len(questions)
             for category, questions in self.dat.items()]
        n = np.unique(n)
        assert n.size == 1
        return n[0]

    @property
    def flipping_questions(self):
        return np.any([question.state == Question.UNFLIPPED
                       for category in self.categories
                       for question in category.questions])

    def flip_questions(self):
        audio_player = QMediaPlayer()
        where = Path(__file__).parent
        audio_player.setSource(QUrl.fromLocalFile(f'{where}/sounds/flip_questions.mp3'))

        # Create a local event loop to force synchronous waiting
        loop = QEventLoop()
        # Unblock the loop only when the media is fully loaded
        def check_status(status):
            if status == QMediaPlayer.MediaStatus.LoadedMedia:
                loop.quit()
        audio_player.mediaStatusChanged.connect(check_status)
        # Start the local loop (blocks execution here)
        loop.exec()

        time_to_flip = audio_player.duration()
        time_to_flip = ((time_to_flip - 1000)
                        / (self.num_questions * self.num_categories))

        indices = []
        for i in range(self.num_categories):
            for j in range(self.num_questions):
                indices.append([i, j])

        rng = np.random.default_rng()
        rng.shuffle(indices)

        for t, index in enumerate(indices):
            i, j = index
            if self.categories[i].questions[j].state == Question.UNFLIPPED:
                QTimer.singleShot(time_to_flip * (t + 1),
                                  self.categories[i].questions[j].next)
