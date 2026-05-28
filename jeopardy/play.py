import sys
from PySide6.QtWidgets import QApplication
from jeopardy import Jeopardy

app = QApplication()

widget = Jeopardy("game_blank.json")

sys.exit(app.exec())