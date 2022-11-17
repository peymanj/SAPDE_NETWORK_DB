from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
from source.framework.framework_models.ui import userAccessForm
from source.framework.ui.qt_ui.ui_base import UiBase
from source.framework.utilities import log, tr
from PyQt5.QtWidgets import QTreeWidgetItem
from source.framework.framework_models.ui.userAccessForm import UserAccessForm


class UiUserAccessForm(QMainWindow, UiBase):
    login_signal = pyqtSignal()
    field_map_dict = {
        'usernameLineEdit': 'username',
        'passwordLineEdit': 'password',
    }
    
    _model = 'user_access_relation'
    
    def __init__(self, current_user, refresh_signal):
        super(UiUserAccessForm, self).__init__()
        UserAccessForm().setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.user_id = current_user
        self.refresh_signal = refresh_signal
        self.cancelPushButton.clicked.connect(self.close)
        self.savePushButton.clicked.connect(self.save)
        self.get_access_data()
        self.set_list_widget_data()
        self.get_user_data()
        self.show()
        
        
    def show(self):
        super().show()

    def get_access_data(self):
        user_access = self.api('exec', 'user_access_relation', 'search', 
            {'condition': [('user', '=', self.user_id)],
            'return_dict':False, 'return_object':False })
        self.user_access_ids = list()
        if user_access:
            for rec in user_access:
                self.user_access_ids.append({'access_id': rec.get('access'), 'rel_id': rec.get('id')})
            
        self.all_access_raw = self.api('exec', 'access', 'read', {'return_dict':False, 'return_object':False})
        self.all_model_access = dict()
        self.all_ui_access = dict()
        
        if self.all_access_raw:
            for rec in self.all_access_raw:
                if rec.get('access_type') == 1:
                    if self.all_model_access.get(rec.get('model'), False) == False:
                        self.all_model_access[rec.get('model')] = list()
                    
                    if not rec.get('relation'):
                        self.all_model_access[rec.get('model')].append(
                            (rec.get('id'), rec.get('model'), rec.get('action'), rec.get('name'))
                        )
               
                if rec.get('access_type') == 2:
                    if self.all_ui_access.get(rec.get('model'), False) == False:
                        self.all_ui_access[rec.get('model')] = list()
                    
                    if not rec.get('relation'):
                        self.all_ui_access[rec.get('model')].append(
                            (rec.get('id'), rec.get('model'), rec.get('action'), rec.get('name'))
                            )

    def get_user_data(self):
        user_data = self.api('exec', 'user', 'read', {'ids': [self.user_id], 'as_relational':True})
        self.userLineEdit.setText(user_data[0][1])

    def set_list_widget_data(self):
        list = self.accessListWidget
        headerItem = QTreeWidgetItem()
        item = QTreeWidgetItem()

        for model, ac_list in self.all_ui_access.items():
            parent = QTreeWidgetItem(list)
            parent.setText(0, tr(model))
            parent.setFlags(parent.flags() | Qt.ItemIsTristate| Qt.ItemIsUserCheckable) 
            parent.setCheckState(0, Qt.Checked)
            for ac in ac_list:
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, tr(ac[3]))
                child.setData(0, Qt.UserRole, ac[0])
                child.setCheckState(0, Qt.Unchecked)
                for item in self.user_access_ids:
                    if ac[0] == item.get('access_id'):
                        child.setCheckState(0, Qt.Checked)
                        break
        list.show() 
    
   
    def get_list_widget_data(self):

        def get_sublist_nodes(list_widget_item):
            access_ids = list()
            for i in range(list_widget_item.childCount()):
                if list_widget_item.child(i).checkState(0):
                    access_ids.append(list_widget_item.child(i).data(0, Qt.UserRole))    
            return access_ids

        all_items = list()
        for i in range(self.accessListWidget.topLevelItemCount()):
            parent = self.accessListWidget.topLevelItem(i)
            all_items.extend(get_sublist_nodes(parent))
        return all_items

    def save(self):
        access_action_mapped = {
            'create': 'create',
            'update': 'update',
            'list': 'read',
            'form': 'read',
            'delete': 'delete',
        }
        def get_access_mapped(method):
            return access_action_mapped.get(ui_method, None) or ui_method

        new_access_ids = self.get_list_widget_data()
        for id in new_access_ids:
            exists = False
            search_result = self.search_tuples(id, self.all_ui_access, 0)
            ui_model_name = search_result[1]
            ui_method = search_result[2]

            access = self.api_get('get_ui_model_access', {'ui_model': ui_model_name, 'mode': self.Mode.list_view})
            model_name = self.pool.get('ui_models').get(ui_model_name)._model
            model_tup = self.search_tuples(model_name, self.all_model_access, 1, id2=get_access_mapped(ui_method), index2=2)
            if model_tup:
                model_access_item = model_tup
            else:
                model_access_item = None

            for item in self.user_access_ids:

                if item.get('access_id') == id:
                    exists = True
                    self.user_access_ids.remove(item)
                    if model_access_item:
                        for item in self.user_access_ids:
                            if item.get('access_id') == model_access_item[0]:
                                self.user_access_ids.remove(item)
                                break
                    break
            if not exists:
                context = {
                    'field_values': {'user': self.user_id, 'access': id}
                }
                self.api('exec', 'user_access_relation', 'create', context)
                
                if model_access_item:
                    context = {
                        'condition': ['and', ('user', '=', self.user_id), ('access', '=', model_access_item[0])]
                    }
                    if not self.api('exec', 'user_access_relation', 'search', context):
                        context = {
                            'field_values': {'user': self.user_id, 'access': model_access_item[0]}
                        }
                        self.api('exec', 'user_access_relation', 'create', context)


            
        for item in self.user_access_ids:
            self.api('exec', 'user_access_relation', 'delete', {'condition': [('id', '=', item.get('rel_id'))]})
          
            # search_result = self.search_tuples(item.get('rel_id'), self.all_ui_access, 0)
            # ui_model_name = search_result[1]
            # ui_method = search_result[2]
            # model_name = self.api('get_ui_model', ui_model_name, self.Mode.update_view)._model
            # model_tup = self.search_tuples(model_name, self.all_model_access, 1, id2=ui_method, index2=2)
                
            # if not model_tup: continue
            # model_access_id = model_tup[0]
            # self.api('exec', 'user_access_relation', 'delete', {'condition': [('id', '=', model_access_id)]})

        self.refresh_signal.emit()
        self.close()

    def search_tuples(self, id, data_dict, index, id2=None, index2=None):
        for ui_model, tup_list in data_dict.items():
            for tup in tup_list:
                if tup[index] == id:
                    if id2:
                        if tup[index2] == id2:
                            return tup
                    else:
                        return tup
        return None

