from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel
from .extended_label import ExtendedLabel
from source.framework.ui.qt_ui.theme.colors import ColorManager

class ExtendedNavLabel(ExtendedLabel):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedNavLabel, self).__init__(parent, **kwargs)
        color = ColorManager().get_color
        self.setStyleSheet(
            f"background-color: {color('ExtendedNavLabel', 'background')};"
            "font:Bold;"
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