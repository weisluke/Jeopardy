from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QResizeEvent
from player import Player
import numpy as np


class Players(QFrame):
    
    def __init__(self, parent, players):
        QFrame.__init__(self, parent=parent)

        self.players = []
        for name in players:
            self.players.append(Player(self, name))

    def resizeEvent(self, event: QResizeEvent):
        # 90% of the height is for players
        h = 0.9 / self.num_players 
        # 10% of the height is for spacing between players
        dh = 0.1 / (self.num_players - 1) 
        for i, player in enumerate(self.players):
            player.setGeometry(0, self.height() * (h + dh) * i,
                               self.width(), self.height() * h)

    @property
    def root(self):
        return self.topLevelWidget()
    
    @property
    def num_players(self):
        return len(self.players)

    @property
    def flipping_players(self):
        return np.any([player.state == Player.UNFLIPPED
                       for player in self.players])

    def flip_players(self):
        for player in self.players:
            if player.state == Player.UNFLIPPED:
                player.next()
                return
    
    @property
    def can_buzz(self):
        return np.any([player.can_buzz
                       for player in self.players])
