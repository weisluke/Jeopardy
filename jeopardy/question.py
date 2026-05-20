from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from pathlib import Path


class Question(QLabel):

    def __init__(self, category, question, answer, cost):
        QLabel.__init__(self, category,
                        scaledContents=True,
                        alignment=(Qt.AlignVCenter | Qt.AlignHCenter),
                        wordWrap=True)
        self.setStyleSheet("""
            QLabel {
                border: 2px solid black;
                padding: 5px;
            }
        """)

        where = Path(__file__).parent
        self.pixmap = QPixmap(f'{where}/jeopardy.png')
        self.setPixmap(self.pixmap)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.question = question
        self.answer = answer
        self.cost = cost
