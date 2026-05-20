from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QResizeEvent
from category import Category


class Board(QFrame):

    def __init__(self, parent, round, dat):
        QFrame.__init__(self, parent)
        self.setStyleSheet("""
            QFrame {
                border: 2px solid gray;
                padding: 5px;
            }
        """)

        self.round = round
        # dictionary of {category: {question: answer}, ...}
        self.dat = dat

        self.categories = []
        for category, questions in self.dat.items():
            self.categories.append(Category(self, category, questions))

    @property
    def num_categories(self):
        return len(self.categories)
   
    def resizeEvent(self, event: QResizeEvent):
        dw = self.width() / self.num_categories
        for i, category in enumerate(self.categories):
            category.setGeometry(dw * i, 0, dw, self.height())
