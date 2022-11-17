from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel, QKeyEvent
from PyQt5.QtCore import Qt
import sys
  
# creating checkable combo box class
class ExtendedCheckableCombobox(QComboBox):
    def __init__(self, parent=None, **kwargs):
        super(ExtendedCheckableCombobox, self).__init__(parent, **kwargs)
        self.view().pressed.connect(self.handle_item_pressed)
        self.setModel(QStandardItemModel(self))
  
    def handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.CheckState.Checked:
            item.setCheckState(Qt.CheckState.Unchecked)
        else:
            item.setCheckState(Qt.CheckState.Checked)
        self.current_index = item.row()
        self.check_items()
  
    def item_checked(self, index):
        item = self.model().item(index, 0)
        return item.checkState() == Qt.CheckState.Checked
  
    def check_items(self):
        checkedItems = []
        for i in range(self.count()):
            if self.item_checked(i):
                checkedItems.append(i)
        self.update_label(checkedItems)
  
    def update_label(self, item_list):
            txt = ' - '.join(['[' + self.data[item][1] + ']' for item in item_list])
            self.setItemText(self.current_index, txt)
  
    # sys.stdout.flush()
  
    def setValue(self, items, **kwargs):
        self.clear()
        if not items:
            return
        items = items if type(items) in (list, dict) else [items]
        self.data = items
        for i, item in enumerate(items):

            if isinstance(item, (tuple, list)):
                self.addItem(item[1], item[0])
                item = self.model().item(i, 0)
                item.setCheckState(Qt.CheckState.Unchecked)
        
    def set_checked(self, ids):
        if not ids:
            return
            
        for id in ids:
            for i in range(self.count()):
                if self.data[i][0] == id:
                    item = self.model().item(i, 0)
                    item.setCheckState(Qt.CheckState.Checked)
                    break
        self.current_index = self.currentIndex()
        self.check_items()

    def getValue(self):
        selected_ids = list()
        for i in range(self.count()):
            if self.item_checked(i):
                selected_ids.append(self.data[i][0])
        return selected_ids

    def setReadOnly(self, val):
        if val:
            self.setEnabled(False)
        else:
            self.setEnabled(True)

    def setOnChange(self, func):
        pass
        # self.currentIndexChanged.connect(func)

    def showPopup(self) -> None:
        for i, item in enumerate(self.data):
            self.setItemText(i, item[1])
        return super().showPopup()
  
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() in (Qt.Key_Up, Qt.Key_Down):
            pass
        else:
            return super().keyPressEvent(e)