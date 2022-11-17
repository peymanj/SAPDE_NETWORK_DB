from PyQt5.QtCore import QDate, QTimer, QLocale
from PyQt5.QtWidgets import QDateEdit, QDateTimeEdit

class ExtendedDateEdit(QDateEdit):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedDateEdit, self).__init__(parent, **kwargs)

    def setValue(self, val, **kwargs):
        if val:
            if isinstance(val, str) and val.lower() == 'today':
                val = QDate.currentDate()
            self.setDate(val or QDateTimeEdit().date())

    def getValue(self):
        return QLocale.c().toString(self.date(), 'yyyy-MM-dd')
        

    