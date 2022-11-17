from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLineEdit, QAction
from source.framework.ui.qt_ui.icon import IconManager
from source.framework.utilities import _eval, tr


class ExtendedLineEdit(QLineEdit):
    
    def __init__(self, parent=None, **kwargs):
        super(ExtendedLineEdit, self).__init__(parent, **kwargs)
        self.return_press_connected = False

    def focusInEvent(self, *args, **kwargs):
        QTimer.singleShot(0, self.selectAll)
            
    def getValue(self):
        return self.text() or (None if self.isHidden() else False) # None is not transferd to db, False is transfered

    def setValue(self, val, **kwargs):
        val = _eval(val)
        if isinstance(val, (tuple, list)) and val and isinstance(val[0], int):
            val = str(val[1])
        elif isinstance(val, list):
            val = '- '.join(['[' + str(item[1]) + ']' for item in val])
        elif val is None or val is False:
            val = str()
        else:
            val = str(val)
        self.setText(val)

    def setOnChange(self, func):
        self.textEdited.connect(func)

    def showEye(self, theme=None):
        
        self.setEchoMode(QLineEdit.Password)
        icon = IconManager().get_icon('eye')
        self.showPassAction = QAction(icon, tr('Show password'), self)
        self.addAction(
            self.showPassAction, QLineEdit.TrailingPosition)
        self.showPassAction.setCheckable(True)
        self.showPassAction.toggled.connect(self.showPassword)

    def showPassword(self, show):
        self.setEchoMode(
            QLineEdit.Normal if show else QLineEdit.Password)

    def setReadOnly(self, a0: bool) -> None:
        return super().setReadOnly(a0)
