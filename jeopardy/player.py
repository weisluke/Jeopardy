from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QPushButton
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtCore import QRect, Qt
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
        pixmap = QPixmap(f'{where}/jeopardy.png')
        width = pixmap.width()
        height = pixmap.height()
        rect = QRect(0, 3 * height / 4, width / 3, height / 4)
        pixmap = pixmap.copy(rect)
        self.labels["background"].setPixmap(pixmap)

        self.labels["name"] = QLabel(self.labels["background"],
                                     alignment=(Qt.AlignVCenter | Qt.AlignHCenter),
                                     wordWrap=True)
        self.labels["name"].setStyleSheet("background: transparent;")
        
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

        self.update()

    def resizeEvent(self, event: QResizeEvent):
        self.labels["money"].setGeometry(0, 0, 
                                         self.width() * 0.9, self.height() * 0.5)
        self.labels["background"].setGeometry(0, self.height() * 0.5, 
                                              self.width(), self.height() * 0.5)
        self.labels["name"].resize(self.labels["background"].size())
        self.buttons["add_money"].setGeometry(self.width() * 0.9, 0,
                                              self.width() * 0.1, self.height() * 0.25)
        self.buttons["subtract_money"].setGeometry(self.width() * 0.9, self.height() * 0.25,
                                                   self.width() * 0.1, self.height() * 0.25)
        
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
                self.labels["name"].setStyleSheet("""
                    QLabel {
                        font-size: 50pt;
                        font-weight: bold;
                        font: 'Times New Roman';
                        color: white;
                        background: transparent;
                    }
                """)
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
