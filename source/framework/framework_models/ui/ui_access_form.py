from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *
class UiAccessForm(UiBaseClass):
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    _model = 'access'
    _menu_bar = False
    _list_view = {
        'first_list': {'source': 'UiAccessForm'}
    }

    _form_view = {
        'fields': [
            'model',
            'action',
            'name',        
        ],

    }

    