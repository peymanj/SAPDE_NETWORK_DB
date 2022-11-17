from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QSpinBox

class ExtendedSpinBox(QSpinBox):

    focus_in_signal = pyqtSignal()
    focus_out_signal = pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        super(ExtendedSpinBox, self).__init__(parent, **kwargs)
        self.setMaximum(100000)
        
    def setValue(self, val, **kwargs):
        if isinstance(val, int):
            return super().setValue(val or 0)
        

    def getValue(self):
        return self.value()

    def focusInEvent(self, *args, **kwargs):
        self.focus_in_signal.emit()
        super().focusInEvent(*args, **kwargs)
    
    def focusOutEvent(self, *args, **kwargs):
        self.focus_out_signal.emit()
        super().focusOutEvent(*args, **kwargs)
