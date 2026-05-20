from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from question import Question
from pathlib import Path


class Category(QFrame):

    def __init__(self, board, category, dat):
        QFrame.__init__(self, board)
        self.setStyleSheet("""
            QFrame {
                border: 2px solid black;
                padding: 5px;
            }
        """)

        where = Path(__file__).parent
        self.pixmap = QPixmap(f'{where}/jeopardy.png')

        self.board = board
        self.category = category

        # dictionary of {question: answer, ...}
        self.dat = dat

        self.title = QLabel(self, scaledContents=True,
                            alignment=(Qt.AlignVCenter | Qt.AlignHCenter),
                            wordWrap=True)
        self.title.setStyleSheet("""
            QLabel {
                border: 2px solid black;
                padding: 5px;
            }
        """)

        self.title.setPixmap(self.pixmap)
        self.title.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.questions = []
        for i, (question, answer) in enumerate(self.dat.items()):
            i += 1
            self.questions.append(Question(self, question, answer, 
                                           100 * i * self.board.round)
                                  )

    @property
    def num_questions(self):
        return len(self.questions)
    
    def resizeEvent(self, event):
        dh = self.height() / (self.num_questions + 1)
        self.title.setGeometry(0, 0, self.width(), dh)
        for i, question in enumerate(self.questions):
            question.setGeometry(0, dh * (i + 1), self.width(), dh)
