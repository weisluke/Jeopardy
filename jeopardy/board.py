from PySide6.QtWidgets import QFrame, QLabel
from PySide6.QtGui import QPixmap, QResizeEvent, Qt
from PySide6.QtCore import QRect, QTimer, QUrl, QEventLoop
from PySide6.QtMultimedia import QMediaPlayer
from category import Category
from question import Question
from pathlib import Path
import numpy as np


class Board(QFrame):

    def __init__(self, parent, round, dat):
        QFrame.__init__(self, parent)

        where = Path(__file__).parent
        self.pixmap = QPixmap(f'{where}/jeopardy.webp')

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

        self.display = QLabel(self, 
                              alignment=(Qt.AlignVCenter | Qt.AlignHCenter),
                              wordWrap=True)
        self.display.setStyleSheet("""
            QLabel {
                font-size: 60pt;
                font-weight: bold;
                font: 'Times New Roman';
                color: white;
                border: 2px solid black;
                padding: 0px;
                background-color: blue;
            }
        """)
        self.display.hide()
        
        self.root.on_question_answered.connect(self.question_answered)
        self.root.on_player_selected.connect(self.player_selected)
    
        # create daily doubles
        indices = []
        for i in range(self.num_categories):
            for j in range(self.num_questions):
                indices.append([i, j])

        rng = np.random.default_rng()
        indices = rng.choice(indices, self.round)
        self.daily_doubles = [self.categories[i].questions[j]
                              for i, j in indices]
        for what in self.daily_doubles:
            print('Daily double:')
            print(f'Category: {what.category.category}')
            print(f'Cost: ${what.cost}')
            print()
    
    def resizeEvent(self, event: QResizeEvent):
        dw = self.width() * 0.98 / self.num_categories
        for i, category in enumerate(self.categories):
            category.setGeometry(self.width() * 0.01 + dw * i, self.height() * 0.01, 
                                 dw, self.height() * 0.98)
        dh = self.height() * 0.98 / (self.num_questions + 1)
        self.display.setGeometry(self.width() * 0.01, self.height() * 0.01 + dh, 
                                 self.width() * 0.98, dh * self.num_questions)

    @property
    def root(self):
        return self.topLevelWidget()
        
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
        def check_status(status, loop):
            if status == QMediaPlayer.MediaStatus.LoadedMedia:
                loop.quit()
        audio_player.mediaStatusChanged.connect(lambda x: check_status(x, loop))
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
                
    @property
    def flipping_categories(self):
        return np.any([category.state == Category.UNFLIPPED
                       for category in self.categories])
    
    def flip_categories(self):
        for category in self.categories:
            if category.state == Category.UNFLIPPED:
                category.next()
                self.display.setText(category.category)
                return
            
    @property
    def flipping(self):
        return self.flipping_questions or self.flipping_categories

    @property
    def answering_questions(self):
        return np.any([question.state <= Question.ANSWER
                       for category in self.categories
                       for question in category.questions])

    def next(self):
        # cannot advance if no question selected
        if self.root.curr_question is None:
            return
        # cannot advance if player has been locked in
        if self.root.curr_player is not None:
            return
        # cannot advance if current question is a daily double
        # and no wager has been set
        if (self.root.curr_question.is_daily_double
                and self.root.curr_question.state == Question.COST
                and self.root.wager.wager <= 0):
            return
        
        self.root.curr_question.next()

        if self.root.curr_question is not None:
            self.display.setText(self.root.curr_question.text())
        else:
            self.display.setText("")
    
    def question_answered(self):
        self.setStyleSheet(None)

    def player_selected(self, player):
        self.setStyleSheet(None)
