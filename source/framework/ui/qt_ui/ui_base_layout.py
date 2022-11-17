from PyQt5.QtWidgets import *

from source.framework.utilities import tr
from .extended_widgets import *
from .ui_base import UiBase
from PyQt5 import uic
from PyQt5.QtCore import Qt
from .ui_list_view import list_set
from .ui_form_view import form_set
from .ui_update_view import update_set
from .ui_create_view import create_set
from source.framework.config import current_app
# from source.framework.ui.qt_ui.baseForm import BaseForm
# from .baseForm import BaseForm
from .baseFormListLayoutForm import BaseFormListLayoutForm
from source.framework.ui.qt_ui.ui_search import UiSearch




class UiBaseLayout(QWidget, UiBase):
    
    def __init__(self, *args, **kwargs):
        super(UiBaseLayout, self).__init__()
        if kwargs.get('set_form_stat'):
            if kwargs.get('ui_designer'):
                uic.loadUi(kwargs.get('ui_designer'), self)
            else:
                BaseFormListLayoutForm().setupUi(self)

        self.model = kwargs.get('model')
        self.ui = self
        self.mode = kwargs.get('mode')
        self.active_id = kwargs.get('id')
        self.current_mode = kwargs.get('mode')
        self.form_parent = kwargs.get('parent')   
        self.stacked_form = kwargs.get('stacked_form')
        self.setWindowTitle(tr(current_app))
        self._fields = self.api_get('get_model_fields', {'model': self.model})['fields']
        self.form_set = form_set
        self.update_set = update_set
        self.list_set = list_set
        self.create_set = create_set
        self.context = dict()
        self.set_form_stat = kwargs.get('set_form_stat')
        

    def init(self):
        self.set_mode(self.mode)
        self.set_elements()
        # self.show()
        # self.minimumSizeHint()
        # self.showNormal()
        # 


    def set_signals(self, signal):
        self.signal = signal

    def set_mode(self, mode):
        self.context_set()
        if mode == self.Mode.create_view:
            self.create_view()
            self.create_init()
        elif mode == self.Mode.update_view:
            self.update_view()
            self.update_init()
        elif mode == self.Mode.list_view:
            self.list_view()
            self.list_init()
        elif mode == self.Mode.form_view:
            self.form_view()
            self.form_init()

        self.lock_layout()
    
    def update_view(self):
        update_set(self)

    def create_view(self):
        create_set(self)

    def form_view(self):
        form_set(self)

    def list_view(self):
        list_set(self)

    def set_button_connection(self):
        self.signal.open_search.connect\
            (lambda table_widget, field_name: self.open_search_form(table_widget, field_name)) 
        

    def set_status_bar(self, val):
        self.statusBar.setVisible(val)

    def set_options(self):
        
        if self._list_options and hasattr(self, 'list_widget'):
            tbutton = self.list_widget.listOptionsToolButton
            menu = QMenu()
            tbutton.setMenu(menu)
            for opt in self._list_options:
                name = opt.get('name')
                method = opt.get('action')
                action = QAction(name, self)
                #     action.setShortcut("Ctrl+Q")
                # action.setStatusTip('Leave The App')
                action.triggered.connect(getattr(self, method))
                menu.addAction(action)
        
        if self._form_options and hasattr(self, 'form_widget'):
            tbutton = self.form_widget.formOptionsToolButton
            menu = QMenu()
            tbutton.setMenu(menu)
            for opt in self._form_options:
                name = opt.get('name')
                method = opt.get('action')
                action = QAction(name, self)
                #     action.setShortcut("Ctrl+Q")
                # action.setStatusTip('Leave The App')
                action.triggered.connect(getattr(self, method))
                menu.addAction(action)
   
   
    def set_elements(self):
        # self.set_status_bar()
        self.set_button_connection()
        self.set_options()    

   
    def delete(self, active_id):
        if not active_id:
            self.msg.show(self.msg.Warning, 'No items selected.')
            return
        item_name = self.api('exec', self.model, 'read', {'ids': [active_id], 'as_relational': True})[0][1]
        if not self.msg.show(self.msg.Question, 'Are you sure?', 
                add_msg=self.model + ':\n' + item_name):
            return
        
        if not self.is_delete_allowd(active_id):
            self.msg.show(self.msg.Error, 'Unable to delete item.', 
                add_msg='Please delete child items first.')
            return
        else:
            pass
        id_column = self.api_get('get_model_parameter', {'model': self.model, 'param': '_id_column'})['_id_column']
        deleted = self.api('exec', self.model, 'delete', 
            context={'condition':[(id_column, '=', active_id)]})
        self.refresh()
        if self.current_mode == self.Mode.form_view:
            self.close()
        # return deleted

    def list_init(self):
        pass

    def form_init(self):
        pass

    def update_init(self):
        pass

    def create_init(self):
        pass
    
    def context_set(self):
        pass

    def refresh(self):
 
        if self.current_mode == self.Mode.list_view:
            if self.set_form_stat:
                list_set(self, refresh=True)
            if self.form_parent:
                self.form_parent.refresh()

        if self.form_parent:
            if self.current_mode == self.Mode.form_view:
                if self.set_form_stat:
                    self.form_set(self, refresh=True)
                self.form_parent.refresh()
           
            elif self.current_mode == self.Mode.update_view:
                self.form_parent.refresh()
                self.signal.close_form.emit()
           
            elif self.current_mode == self.Mode.create_view:
                self.form_parent.refresh()
                self.signal.close_form.emit()
                   
    def is_delete_allowd(self, active_id):
        relations = self.api_get('get_relations', {'model': False}).get(self.model, None)
        if relations:
            for tup in relations:
                context = {'condition': [(tup[1], '=', active_id)], 'id_only': True}
                data = self.api('exec', tup[0], 'search', context=context)
                return True if not data else False
        else: 
            return True

    def closeEvent(self, event):
        # if self.form_parent:
            # self.form_parent.show()
        event.accept()
        # if can_exit:
        #     event.accept() # let the window close
        # else:
        #     event.ignore()

    def show(self):
        
        if not self.form_parent:
            self.setWindowState(Qt.WindowMaximized)
        else:
            current_stat = self.form_parent.windowState()
            self.resize(self.form_parent.size())   
            self.setWindowState(current_stat)
            self.move(self.form_parent.pos().x(), self.form_parent.pos().y())
        super().show()

    def showMaximized(self):
        # if self   .form_parent:
        #     self.form_parent.hide()
        super().showMaximized()

    def save(self):
        self.save_method(self)

    def save_and_create_new(self):
        self.save_and_create_new_method(self)

    def lock_layout(self):
        ButtomSpacerItem = QSpacerItem(102, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.baseFormListLayoutWidgetLayout.addItem(ButtomSpacerItem, 
                        self.baseFormListLayoutWidgetLayout.rowCount(), 0, 1, 1)


    def open_search_form(self, table_widget, field_name):
        if not getattr(self, 'ui_search', False):
            self.ui_search = UiSearch(parent_form=self, table_widget=table_widget)
        self.ui_search.show(field_name=field_name)

    def get_active_id(self):
        if self.current_mode == self.Mode.list_view:
            return self.list_widget.listFirstTableWidget.get_active_id()
        elif self.current_mode == self.Mode.form_view:
            return self.active_id

    def reopen_create_preprocess(self):
        print('abstract method, override')