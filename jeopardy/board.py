from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QPixmap, QResizeEvent
from PySide6.QtCore import QRect
from category import Category
from pathlib import Path


class Board(QFrame):

    def __init__(self, parent, round, dat):
        QFrame.__init__(self, parent)
        self.setStyleSheet("""
            QFrame {
                border: 2px solid gray;
                padding: 5px;
            }
        """)

        where = Path(__file__).parent
        self.pixmap = QPixmap(f'{where}/jeopardy.png')

        self.round = round
        # dictionary of {category: {question: answer}, ...}
        self.dat = dat

        self.categories = []
        for category, questions in self.dat.items():
            self.categories.append(Category(self, category, questions))

        width = self.pixmap.width() / self.num_categories
        for i, category in enumerate(self.categories):
            height = self.pixmap.height() / category.num_questions
            for j, question in enumerate(category.questions):
                rect = QRect(width * i, height * j, width, height)
                question.setPixmap(self.pixmap.copy(rect))

    @property
    def num_categories(self):
        return len(self.dat)
   
    def resizeEvent(self, event: QResizeEvent):
        dw = self.width() / self.num_categories
        for i, category in enumerate(self.categories):
            category.setGeometry(dw * i, 0, dw, self.height())
