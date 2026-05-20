from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt


class Question(QLabel):

    def __init__(self, category, question, answer, cost):
        QLabel.__init__(self, category,
                        scaledContents=True,
                        alignment=(Qt.AlignVCenter | Qt.AlignHCenter),
                        wordWrap=True)
        self.setStyleSheet("""
            QLabel {
                border: 2px solid black;
                padding: 0px;
            }
        """)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.question = question
        self.answer = answer
        self.cost = cost
