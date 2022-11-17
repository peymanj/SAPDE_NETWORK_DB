from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMenuBar

class ExtendedMenuBar(QMenuBar):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedMenuBar, self).__init__(parent, **kwargs)

    