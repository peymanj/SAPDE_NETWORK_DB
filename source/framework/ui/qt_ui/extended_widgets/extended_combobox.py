from typing import Type
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QCompleter, QComboBox


class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedComboBox, self).__init__(parent, **kwargs)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)
        self.lineEdit().setAlignment(Qt.AlignCenter)
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        self.completer = QCompleter(self.pFilterModel, self)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)


    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)

    def setValue(self, items, set_default=False, **kwargs): # items = [(id, val),]
        self.clear()
        self.data = items
        if not items:
            return

        items = items if type(items) in (list, dict) else [items]
        for item in items:
            if set_default:
                self.set_current_item(item)
                return
            if isinstance(item, (tuple, list)):
                self.addItem(item[1], item[0])
            else:
                self.addItem(item)
        if self.count() > 1:
            self.setCurrentIndex(-1)
        
    def set_current_item(self, item):
        if isinstance(item, (tuple, list)):
            for i in range(len(self.data)):
                if self.data[i][0] == item[0]:
                    self.blockSignals(True)
                    self.setCurrentIndex(-1)
                    self.blockSignals(False)
                    self.setCurrentIndex(i)
                    break
                
    def getValue(self):
        return self.currentData()

    def setReadOnly(self, val):
        if val:
            self.setEnabled(False)
        else:
            self.setEnabled(True)

    def setOnChange(self, func):
        self.currentIndexChanged.connect(func)
