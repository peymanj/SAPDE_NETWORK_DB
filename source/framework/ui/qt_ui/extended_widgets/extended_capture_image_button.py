from PyQt5.QtWidgets import QPushButton
from source.framework.intergration.camera import CameraCapture
from source.framework.ui.qt_ui.icon.icons import IconManager

class ExtendedCaptureImageButton(QPushButton):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedCaptureImageButton, self).__init__(parent, **kwargs)
        self.setText('Capture Image')
        self.clicked.connect(self.initaite_camera_reader)
        not_checked_icon = IconManager().get_icon('red_circular_cross_mark',
                                                 theme_based=False)
        self.setIcon(not_checked_icon)
        self.val = None

    def initaite_camera_reader(self):
        self.camera_capture_form = CameraCapture(self)
        self.camera_capture_form.save_signal.connect(self.setValue)
        self.val = str()
        self.camera_capture_form.show()

    def setValue(self, val, **kwargs):
        self.val = val.replace("b'", '').replace("'","") # b' removed and tailing '
        if self.val:
            checked_icon = IconManager().get_icon('green_circular_check_mark',
                                                       theme_based=False)
            self.setIcon(checked_icon)

    def getValue(self): 
        return self.val
    
    def setReadOnly(self, val):
        self.setEnabled(False)
