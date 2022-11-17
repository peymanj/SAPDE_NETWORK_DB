from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter
from PyQt5.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
    pyqtSlot, pyqtProperty)


class ExtendedNavPushButton(QPushButton):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedNavPushButton, self).__init__(parent, **kwargs)
        self.setStyleSheet(
            "border :3px solid #15a6cf;"
            "font-size: 14px;"
        )
        # "background-color: QLinearGradient(spread:pad x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0" + DefColores[i][0] + ",  stop: 0.4" + DefColores[i][1] + ", stop: 1.0"+ DefColores[i][2]+");"  
        #                    "color: white; "
        #                    "border-style: solid;"
        #                    "border-style: solid;"
        #                    "border-radius: 7;"
        #                    "padding: 3px;"
        #                    "padding-left: 5px;"
        #                    "padding-right: 5px;"
        #                    "border-color: #339;"
        #                    "border-width: 1px;"
        #                    "font:Bold;"
        #                    "font-family:Georgia"
        self.value = None

    def setValue(self, val, **kwargs):
        self.value = val
    
    def getValue(self):    
        return self.value