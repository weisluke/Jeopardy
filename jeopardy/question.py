from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt, QTimer
import numpy as np


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
        self.can_buzz = False  # whether or not this question can be buzzed on
        self.category = category
        self.question = question
        self.answer = answer
        self.cost = cost

        self.root.on_player_deselected.connect(self.player_deselected)

    @property
    def root(self):
        return self.topLevelWidget()
    
    @property
    def board(self):
        return self.category.board

    def next(self):
        # if waiting on players to buzz in,
        # and all of the players can still buzz in,
        # and not overriding
        # don't accidentally move forward to the answer
        if (self.state == self.BUZZING
                and self.root.players.can_buzz
                and not self.root.override.isChecked()):
            return
        
        # disable override if moving to next state
        self.root.override.setChecked(False)
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
                        border: 2px solid black;
                        padding: 0px;
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
                        border: 2px solid black;
                        padding: 0px;
                    }
                """)
            case self.BUZZING:
                # if a player answered correctly
                # but we have not yet moved to the next state
                # don't toggle buzzing
                if not self.root.players.can_buzz:
                    return
                
                self.can_buzz = False
                rng = np.random.default_rng()

                def toggle_buzz(question):
                    question.can_buzz = True
                    question.board.setStyleSheet("""
                        QFrame {
                            border: 10px solid lawngreen;
                        }
                    """)
                QTimer.singleShot(1000 * (rng.random() + 1), lambda: toggle_buzz(self))
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

    def player_deselected(self):
        self.update()
