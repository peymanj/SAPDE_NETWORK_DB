from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *
from .ui_user_access import UiUserAccessForm

class UiUserForm(UiBaseClass):
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def init(self):
        super().init()  
        if hasattr(self, 'form_widget'):
            self.form_widget.password_qwidget.showEye()
            self.set_connections()
        
        if self.current_mode != self.Mode.list_view:
            if self.active_id:
                if not self.is_user_authorized(self.active_id):
                    self.msg.show(self.msg.Error, 'Access denied!')
                    return

    def set_connections(self):
        if hasattr(self, 'list_widget'):
            tw = self.list_widget.listFirstTableWidget
            item = 'Edit'
            menu = QMenu(tw)
            action = QAction(item, tw)
            action.triggered.connect(self.open_access_form)
            menu.addAction(action)    
            tw.set_external_context_menu(tw.Replace, menu=menu)
    
    def open_access_form(self):
        if self.pool.get('current_user').get('id') == self.active_id:
            self.msg.show(self.msg.Error, 'You cannot edit current user accesses!')
            return
        self.user_accesss = UiUserAccessForm(self.active_id, self.signal.refresh)

    def is_user_authorized(self, id):
        selected_user = self.api('exec', 'user', 'read', {'ids': [id], 'return_object': False})[0]
        if selected_user['access_level'] < self.pool.get('current_user').get('access_level'):
            return False
        else:
            return True

    def delete(self, id):
        if not self.is_user_authorized(id):
            self.msg.show(self.msg.Error, 'Access denied!')
            return
        super().delete(id)

    _model = 'user'
    _menu_bar = False
    _list_view = {
        'first_list': {'source': 'UiUserForm'}
    }

    _form_view = {
        'fields': [
            'fullname',
            'username',
            'password',
            'is_active',
        ],
        'many2many': {'field': 'access', 'ui_model':'UiAccessForm'}
    }

    