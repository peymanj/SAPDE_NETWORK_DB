from PyQt5.QtWidgets import QCheckBox, QToolButton
from PyQt5.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter
from PyQt5.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
    pyqtSlot, pyqtProperty)


class ExtendedToolButton(QToolButton):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedToolButton, self).__init__(parent, **kwargs)
        self.setPopupMode(QToolButton.MenuButtonPopup)
    
