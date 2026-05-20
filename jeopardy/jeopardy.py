from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QResizeEvent
import json
from logo import Logo
from board import Board
from players import Players


class Jeopardy(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Jeopardy")

        with open(file) as f:
            self.dat = json.load(f)

        self.logo = Logo(self)

        self.players = Players(self, self.dat["players"])
        self.board = Board(self, 1, self.dat["rounds"]["1"])

        self.resize(1400,1000)
        self.show()

    def resizeEvent(self, event: QResizeEvent):
        self.logo.setGeometry(self.width() * 0.1, 0, 
                              self.width() * 0.5, self.height() * 0.25)
        self.players.setGeometry(self.width() * 0.7, 0,
                                 self.width() * 0.3, self.height())
        self.board.setGeometry(0, self.height() * 0.25,
                               self.width() * 0.7, self.height() * 0.75)
        
