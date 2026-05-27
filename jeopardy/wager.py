from PySide6.QtWidgets import QLineEdit


class Wager(QLineEdit):

    def __init__(self, parent):
        QLineEdit.__init__(self, parent=parent,
                           placeholderText="Wager")
        self.setStyleSheet("""
            QLineEdit {
                background-color: black;
                border: 2px solid gray;
                padding: 5px;
            }
        """)
        self.setEnabled(False)

        self.root.override.checkStateChanged.connect(self.enable)

    @property
    def root(self):
        return self.topLevelWidget()
    
    def enable(self):
        if self.root.override.isChecked():
            self.setEnabled(True)
        else:
            self.setEnabled(False)

    @property
    def wager(self):
        try:
            amount = int(self.text())
        except ValueError:
            amount = 0
            self.setText(None)
        return amount