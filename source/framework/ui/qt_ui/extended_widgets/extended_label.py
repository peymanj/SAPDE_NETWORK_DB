from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel

class ExtendedLabel(QLabel):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedLabel, self).__init__(parent, **kwargs)

    def setValue(self, val, **kwargs):
        if isinstance(val, str):
            self.setText(val or '')
        
    def setReadOnly(self, val):
        pass