from os.path import isfile
from time import sleep
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QProgressBar, QSplashScreen
from PyQt5.QtGui import QPixmap
from source.framework.ui.qt_ui.icon import IconManager
import time

'''
displays splash screen for desiredamount of time
'''


class SplashScreen:
    def __init__(self):
        splash_path = r'source\icons\splash.png'
        if isfile(splash_path):
            splash_pxm = QPixmap(splash_path)
        else:
            splash_pxm = IconManager().get_icon('default_splash', theme_based=False, return_pixmap=True)
        self.splash = QSplashScreen(splash_pxm, Qt.WindowStaysOnTopHint)
        # self.progress_bar = QProgressBar(self.splash)
        # self.splash.setMask(splash_pxm.mask())

    def show(self):
        self.splash.show()

    def close(self):
        self.splash.close()
