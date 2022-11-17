from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLineEdit, QAction
from PyQt5.QtGui import QIcon
from .extended_lineedit import ExtendedLineEdit

class ExtendedUserRoleLineEdit(ExtendedLineEdit):


    def __init__(self, parent=None, **kwargs):
        super(ExtendedUserRoleLineEdit, self).__init__(parent, **kwargs)

    def getValue(self):
        if not hasattr(self, 'userrole') or isinstance(self.userrole, str):
            return super().getValue()
        else:
            return self.userrole
        

    def setValue(self, val, **kwargs):
        if isinstance(val, (tuple, list)) and val and isinstance(val[0], int):
            self.userrole = val[0]
        elif isinstance(val, list):
            self.userrole = [item[0] for item in val]
        elif not val:
            pass
        else:
            self.userrole = val

        return super().setValue(val)
