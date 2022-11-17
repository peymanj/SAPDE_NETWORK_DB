from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QWidget, QLabel, QGridLayout
from PyQt5 import QtGui, QtCore
import base64
from source.framework.ui.qt_ui.icon.icons import IconManager


class ExtendedShowImageButton(QPushButton):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedShowImageButton, self).__init__(parent, **kwargs)
        self.val = str()
        self.clicked.connect(self.bin2image)
        self.setText('View Image')

    def setValue(self, val, **kwargs):
        self.val = val
        if self.val:
            icon = IconManager().get_icon('green_circular_check_mark',
                                          theme_based=False)
        else:
            icon = IconManager().get_icon('red_circular_cross_mark',
                                          theme_based=False)
        self.setIcon(icon)

    def get_value(self):
        return str()

    def setReadOnly(self, val):
        pass
        # self.setEnabled(False)

    def bin2image(self):
        class box(QMainWindow):
            def __init__(self, val, parent=None) -> None:
                super().__init__(parent=parent)
                self.setGeometry(100, 100, 600, 600)
                self.setWindowModality(QtCore.Qt.ApplicationModal)
                wid = QWidget(self)
                self.setCentralWidget(wid)
                self.label = QLabel(self)
                pm = QtGui.QPixmap()
                # pm = Image.open(BytesIO(base64.b64decode(val)))
                pm.loadFromData(base64.b64decode(val))
                pm.scaled(self.label.height(), self.label.width(), QtCore.Qt.KeepAspectRatio)
                self.label.setPixmap(pm)
                self.grid = QGridLayout()
                self.grid.addWidget(self.label, 1, 1)
                wid.setLayout(self.grid)
                self.show()

        self.box = box(self.val)
