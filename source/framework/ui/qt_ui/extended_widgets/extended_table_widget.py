from datetime import date, datetime
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import *  # QTableWidget, QMenu, QAction, QHeaderView, QTableWidgetItem, QAbstractScrollArea, QToolTip
from PyQt5.QtCore import Qt
from source.framework.utilities import log

from source.framework.utilities import tr
from source.framework.ui.qt_ui.icon import IconManager


def value_converter(value):
    if isinstance(value, (tuple, list)):
        value = value[1]
    elif isinstance(value, bool):
        if value:
            value = u'\u2713'  # tick mark
        else:
            value = u'\u2715'  # cross mark
    elif value is None:
        value = '-'
    elif isinstance(value, (datetime, date)):
        value = str(value)
    elif isinstance(value, int):
        value = str(value)
    return value


class ExtendedQTableWidget(QTableWidget):
    Append = 1
    Replace = 2

    def __init__(self, parent=None):
        super(ExtendedQTableWidget, self).__init__(parent)
        self.row = False
        self.column = False
        self.source = None
        self.cellClicked.connect(self.cell_clicked)
        self.active_id = False
        self.search_args = dict()

    def get_active_id(self):
        return self.active_id

    def create_context_menu(self):
        self.menu.clear()
        field_name = self.headers[self.active_col]
        for item in self.context_menu_method:
            setattr(self, 'context_' + item, QAction(tr(item), self))
            action = getattr(self, 'context_' + item)
            action.triggered.connect(self.context_menu_method.get(item))
            self.menu.addAction(action)
        if self.model_fields.get(field_name).get('search'):
            self.connect_column_search()

    def connect_context_menu(self, methods, model_fields):
        self.context_menu_method = methods
        self.model_fields = model_fields
        header = self.horizontalHeader()
        header.sectionClicked.connect(self.header_clicked_sort)
        self.menu = QMenu(self)
        self.menu.aboutToShow.connect(self.create_context_menu)

    def connect_column_search(self):
            search_icon = IconManager().get_icon('search')
            action = QAction(tr('Search'), self)
            setattr(self, 'context_search', action)
            action.setIcon(search_icon)
            action.triggered.connect(self.show_search_box)
            self.menu.addAction(action)

    def set_external_context_menu(self, mode=Append, menu=None, methods=None):
        if mode == self.Append:
            for item in methods:
                setattr(self, 'context_' + item, QAction(tr(item), self))
                action = getattr(self, 'context_' + item)
                action.triggered.connect(methods.get(item))
                self.menu.addAction(action)

        if mode == self.Replace:
            self.menu = menu

    def current_id(self, item=None, row=None):
        active_id = -1
        if not item and row == -1:
            return None
        row = row if row != None else item.row()
        try:
            active_id = int(self.item(row, 0).text())
        except Exception as e:
            log(e)
            active_id = self.item(row, 0).text()
        finally:
            return active_id

    def contextMenuEvent(self, event):
        self.get_coordinates(event)
        self.menu.popup(QCursor.pos())

    def get_coordinates(self, event):
        self.active_row = self.rowAt(event.pos().y())
        self.active_col = self.columnAt(event.pos().x()) - 1  # 0 is hidden id column
        self.active_id = self.current_id(row=self.active_row)

    def header_clicked_sort(self, col):
        if getattr(self, 'sort', None) == Qt.DescendingOrder:
            self.sort = Qt.AscendingOrder
        else:
            self.sort = Qt.DescendingOrder
        self.sortItems(col, self.sort)

    def cell_clicked(self, row, col):
        self.active_id = self.current_id(row=row)
        self.active_col = col

    def show_search_box(self):
        if self.active_col < 0: return
        field_name = self.headers[self.active_col]
        self.search_signal.emit(self, field_name)

    def set_table_widget(self, data, headers, sort_col=None, order='asc', id_col='id',
                         search_signal=None, model=None, model_fields=None, order_id=None):
        self.model_fields = model_fields
        self.source_model = model
        self.order_id = order_id
        self.clearContents()
        self.setRowCount(0)
        if not data:
            return
        self.id_col = id_col
        self.setColumnCount(len(headers) + 1)
        self.headers = headers
        self.search_signal = search_signal

        if sort_col and order.lower() == 'asc':
            if order.lower() == 'asc':
                reverse = False
            elif order.lower() == 'desc':
                reverse = True
            data = sorted(data, key=lambda k: k[sort_col], reverse=reverse)

        self.data = data
        self.load_data_to_table(self.data)

    def load_data_to_table(self, data):
        self.clearContents()
        self.setSortingEnabled(False)
        self.set_headers()
        if not data:
            self.setRowCount(0)
            return
        self.setRowCount(len(data))
        for row_num, row_dict in enumerate(data):
            for col_num, h in enumerate(self.headers):
                value = row_dict.get(h)
                item = QTableWidgetItem(value_converter(value))
                # if col_num == 0:
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_num, col_num + 1, item)
            self.setItem(row_num, 0, QTableWidgetItem(str(row_dict.get(self.id_col))))  # id hidden column
        self.setColumnHidden(0, True)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        self.setSortingEnabled(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.horizontalHeader().setMinimumSectionSize(120)
        self.show()

    def set_headers(self):
        search_icon = IconManager().get_icon('search')
        labels = self.headers
        for i, lbl in enumerate(labels):
            item = QTableWidgetItem()
            if self.search_args.get(lbl, False):
                item.setIcon(search_icon)
            else:
                item.setIcon(QIcon())
            if lbl in self.model_fields:
                item.setText(tr(self.model_fields.get(lbl)['string'],
                             model=self.source_model,
                             model_id=self.order_id,
                             cache=False).title())
            else:
                item.setText(tr(lbl,
                             model=self.source_model,
                             model_id=self.order_id,
                             cache=False).title())
            self.setHorizontalHeaderItem(i + 1, item)
