from PySide6.QtWidgets import QMainWindow

class Jeopardy(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Jeopardy")

        self.resize(1400,1000)
        self.show()
