from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QPushButton
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtCore import QRect, Qt, QTimer
from pathlib import Path


class Player(QFrame):

    # state codes
    UNFLIPPED = 0
    NAME = 1
    
    def __init__(self, parent, name):
        QFrame.__init__(self, parent=parent)
        self.setStyleSheet("""
            QFrame {
                border: 2px solid gray;
                padding: 5px;
            }
        """)

        self.state = self.UNFLIPPED
        self.name = name
        self.money = 0
        self.can_buzz = False

        # Labels for displaying the player's money and name
        self.labels = {}
        self.labels["money"] = QLabel(self,
                                      alignment=(Qt.AlignVCenter | Qt.AlignHCenter),
                                      wordWrap=True)
        
        self.labels["background"] = QLabel(self,
                                           scaledContents=True)
        self.labels["background"].setStyleSheet("""
            QLabel {
                background-color: gray;
                border: 2px solid gray;
                padding: 0px;
            }
        """)
        self.labels["background"].setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        where = Path(__file__).parent
        pixmap = QPixmap(f'{where}/jeopardy_dark.webp')
        width = pixmap.width()
        height = pixmap.height()
        rect = QRect(0, 3 * height / 4, width / 3, height / 4)
        pixmap = pixmap.copy(rect)
        self.labels["background"].setPixmap(pixmap)

        self.labels["name"] = QLabel(self.labels["background"],
                                     alignment=(Qt.AlignVCenter | Qt.AlignHCenter),
                                     wordWrap=True)
        self.labels["name"].setStyleSheet("""
            QLabel {
                font-size: 50pt;
                font-weight: bold;
                font: 'Times New Roman';
                color: white;
                background: transparent;
            }
        """)
        
        # Buttons for adding and subtracting money
        self.buttons = {}
        self.buttons["add_money"] = QPushButton("▲", self)
        self.buttons["add_money"].setStyleSheet("""
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
        self.buttons["subtract_money"] = QPushButton("▼", self)
        self.buttons["subtract_money"].setStyleSheet("""
            QPushButton {
                font-size: 30pt;
                font-weight: bold;
                font: 'Times New Roman';
                color: red;
                background-color: white;
                border: 2px solid gray;
                padding: 5px;
            }
        """)
        self.buttons["add_money"].clicked.connect(self.add_money)
        self.buttons["subtract_money"].clicked.connect(self.subtract_money)

        self.root.on_buzz.connect(self.buzz)

        self.root.on_player_selected.connect(self.player_selected)
        self.root.on_player_deselected.connect(self.player_deselected)

        self.update()

    def resizeEvent(self, event: QResizeEvent):
        self.labels["money"].setGeometry(0, 0, 
                                         self.width() * 0.85, self.height() * 0.5)
        self.labels["background"].setGeometry(0, self.height() * 0.5, 
                                              self.width(), self.height() * 0.5)
        self.labels["name"].resize(self.labels["background"].size())
        self.buttons["add_money"].setGeometry(self.width() * 0.85, 0,
                                              self.width() * 0.15, self.height() * 0.25)
        self.buttons["subtract_money"].setGeometry(self.width() * 0.85, self.height() * 0.25,
                                                   self.width() * 0.15, self.height() * 0.25)
        
    @property
    def root(self):
        return self.topLevelWidget()
    
    def next(self):
        if self.state <= self.NAME:
            self.state += 1
        self.update()

    def update(self):
        match self.state:
            case self.UNFLIPPED:
                pass
            case self.NAME:
                self.labels["name"].setText(self.name)
                # immediately move to the next state
                # once we've flipped the name
                self.next()
            case _:
                pass

        if self.money >= 0:
            self.labels["money"].setText(f"${self.money}")
            self.labels["money"].setStyleSheet("""
                QLabel {
                    font-size: 50pt;
                    font-weight: bold;
                    font: 'Times New Roman';
                    color: white;
                    background-color: blue;
                }
            """)
        else:
            self.labels["money"].setText(f"-${-self.money}")
            self.labels["money"].setStyleSheet("""
                QLabel {
                    font-size: 50pt;
                    font-weight: bold;
                    font: 'Times New Roman';
                    color: red;
                    background-color: blue;
                }
            """)

    def add_money(self):
        amount = 0

        if self.root.override.isChecked():
            amount = self.root.wager.wager
            self.root.wager.setText(None)
            self.root.override.setChecked(False)
        elif (self.root.curr_player is self
                or (self.root.curr_question is not None
                    and self.root.curr_question.is_daily_double)):

            if self.root.curr_question.is_daily_double:
                amount = self.root.wager.wager
                self.root.wager.setText(None)
            else:
                amount = self.root.curr_question.cost
            self.root.on_question_answered.emit()
            self.root.on_player_deselected.emit()

        self.money += amount
        self.update()

    def subtract_money(self):
        amount = 0

        if self.root.override.isChecked():
            amount = self.root.wager.wager
            self.root.wager.setText(None)
            self.root.override.setChecked(False)
        elif (self.root.curr_player is self
                or (self.root.curr_question is not None
                    and self.root.curr_question.is_daily_double)):

            if self.root.curr_question.is_daily_double:
                amount = self.root.wager.wager
                self.root.wager.setText(None)
            else:
                amount = self.root.curr_question.cost

            self.can_buzz = False
            self.root.on_player_deselected.emit()

        self.money -= amount
        self.update()

    @property
    def index(self):
        return self.root.players.players.index(self) + 1

    def buzz(self, player):
        if player != self.index:
            return
        if not self.can_buzz:
            return
        
        if not self.root.curr_question.can_buzz:
            self.can_buzz = False
            def toggle_buzz(player):
                player.can_buzz = True
            QTimer.singleShot(250, lambda: toggle_buzz(self))
            return
        
        if self.root.curr_player is None:
            self.root.on_player_selected.emit(self)
            print(f"{self.name} buzzed in\n")

    def player_selected(self, player):
        if player is not self:
            return
        self.labels["name"].setStyleSheet("""
                QLabel {
                    font-size: 50pt;
                    font-weight: bold;
                    font: 'Times New Roman';
                    color: white;
                    background: transparent;
                    border: 5px solid lawngreen;
                    padding: 5px;                   
                }
            """)
        self.update()
        
    def player_deselected(self):
        self.labels["name"].setStyleSheet("""
                QLabel {
                    font-size: 50pt;
                    font-weight: bold;
                    font: 'Times New Roman';
                    color: white;
                    background: transparent;
                }
            """)
        self.update()
