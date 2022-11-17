from PyQt5.QtCore import QDateTime, QTimer, QLocale
from PyQt5.QtWidgets import QDateEdit, QDateTimeEdit
from datetime import datetime


class ExtendedDateTimeEdit(QDateTimeEdit):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedDateTimeEdit, self).__init__(parent, **kwargs)

    def setValue(self, val, **kwargs):
        if val:
            if isinstance(val, str) and val.lower() in ('now', 'today'):
                val = QDateTime().currentDateTime()
            self.setDateTime(val or QDateTimeEdit().dateTime())

    def getValue(self):
        return QLocale.c().toString(self.dateTime(), 'yyyy-MM-dd hh:mm:ss')
        

    