from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt


class Question(QLabel):

    # state codes
    UNFLIPPED = 0
    COST = 1
    QUESTION = 2
    BUZZING = 3
    ANSWER = 4

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

        self.state = self.UNFLIPPED
        self.question = question
        self.answer = answer
        self.cost = cost

    def next(self):
        if self.state <= self.ANSWER:
            self.state += 1
        self.update()

    def update(self):
        match self.state:
            case self.UNFLIPPED:
                pass
            case self.COST:
                self.setText(f"${self.cost}")
                self.setStyleSheet("""
                    QLabel {
                        font-size: 25pt;
                        font-weight: bold;
                        font: 'Times New Roman';
                        color: white;
                        background-color: blue;
                    }
                """)
            case self.QUESTION:
                self.setText(self.question)
            case self.BUZZING:
                pass
            case self.ANSWER:
                self.setText(self.answer)
            case _:
                pass
