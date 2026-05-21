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
        self.category = category
        self.question = question
        self.answer = answer
        self.cost = cost

    @property
    def root(self):
        return self.topLevelWidget()
    
    @property
    def board(self):
        return self.category.board

    def next(self):
        if self.state <= self.ANSWER:
            self.state += 1
        self.update()

    def update(self):
        match self.state:
            case self.UNFLIPPED:
                return
            case self.COST:
                self.setText(f"${self.cost}")
                self.setStyleSheet("""
                    QLabel {
                        font-size: 25pt;
                        font-weight: bold;
                        font: 'Times New Roman';
                        color: gold;
                        background-color: blue;
                    }
                """)
            case self.QUESTION:
                self.setText(self.question)
                self.setStyleSheet("""
                    QLabel {
                        font-size: 25pt;
                        font-weight: bold;
                        font: 'Times New Roman';
                        color: white;
                        background-color: blue;
                    }
                """)
            case self.BUZZING:
                pass
            case self.ANSWER:
                self.setText(self.answer)
            case _:
                self.setText("")
                if self.root.curr_question == self:
                    self.root.on_question_completed.emit()
            
    def mouseReleaseEvent(self, event):
        if self.board.flipping:
            return
        if self.state > self.ANSWER:
            return
        self.root.on_question_selected.emit(self)
