from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLineEdit

class ExtendedTagLineEdit(QLineEdit):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedTagLineEdit, self).__init__(parent, **kwargs)

    def getValue(self):
        return self.text()

    def setValue(self, val, **kwargs):
        if isinstance(val, (tuple, list)):
            self.setText(str(val[1]))
        else:
            self.setText(str(val))

    def setOnChange(self, func):
        self.textEdited.connect(func)