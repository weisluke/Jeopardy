from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QRect, Qt
from pathlib import Path


class Logo(QLabel):

    def __init__(self, parent=None):
        QLabel.__init__(self, parent=parent,
                        scaledContents=True,
                        alignment=(Qt.AlignVCenter | Qt.AlignHCenter),
                        wordWrap=True)

        where = Path(__file__).parent
        pixmap = QPixmap(f'{where}/jeopardy.png')

        width = pixmap.width()
        height = pixmap.height()
        rect = QRect(0, height / 4, width, height / 2)
        pixmap = pixmap.copy(rect)

        self.setPixmap(pixmap)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.setStyleSheet("""
            QLabel {
                background-color: gray;
                border: 2px solid gray;
                padding: 5px;
            }
        """)
