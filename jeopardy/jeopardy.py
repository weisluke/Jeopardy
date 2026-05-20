from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QResizeEvent
from logo import Logo


class Jeopardy(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Jeopardy")

        self.logo = Logo(self)

        self.resize(1400,1000)
        self.show()

    def resizeEvent(self, event: QResizeEvent):
        self.logo.setGeometry(self.width() * 0.1, 0, 
                              self.width() * 0.5, self.height() * 0.25)
        
