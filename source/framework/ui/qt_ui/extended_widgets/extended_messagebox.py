from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from source.framework.utilities import tr
from pyodbc import IntegrityError

class MsgBoxError(Exception):
    message = "Action aborted."


class ExtendedMessageBox(QMessageBox):
    Warning = 1
    Error = 2
    Info = 3
    Question = 4
    
    mapped = {
        Warning:     {'icon': QMessageBox.Warning,     'title': 'Warning'},
        Error:       {'icon': QMessageBox.Critical,    'title': 'Error'},
        Info:        {'icon': QMessageBox.Information, 'title': 'Message'},
        Question:    {'icon': QMessageBox.Question,    'title': 'Attention'},
    }
    def __init__(self, parent=None):
        super(ExtendedMessageBox, self).__init__(parent)

    def show(self, box_type, msg, add_msg=None, detail=None):
        self.setIcon(self.mapped.get(box_type).get('icon'))
        self.setText(tr(self._error_translator(msg)))
        self.setInformativeText(tr(add_msg))
        self.setWindowTitle(tr(self.mapped.get(box_type).get('title')))
        self.setDetailedText(tr(detail))
        if box_type in (self.Info, self.Error):
            self.setStandardButtons(QMessageBox.Ok) 
        elif box_type in (self.Warning, self.Question):
            self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
        super().show()
        
        if box_type in (self.Error,):
            if self.exec_() == QMessageBox.Ok:
                if isinstance(msg, Exception):
                    raise msg
                raise MsgBoxError
        else:
            if self.exec_() == QMessageBox.Ok:
                return True
            else:
                return False
    
    def _error_translator(self, e):
        if isinstance(e, IntegrityError) and 'unique' in str(e):
            msg = tr('Operation failed. Item already exists.')
        else:
            msg = str(e)
        return msg

        

