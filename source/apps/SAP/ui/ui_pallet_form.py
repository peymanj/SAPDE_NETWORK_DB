from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *
class UiPalletForm(UiBaseClass):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    
    _menu_bar = False
    _model = 'pallet'

    _list_view = {
        'first_list': {'source': 'UiPalletForm'}
    }

    _form_view = {
        'fields': [
            'code',
        ],

    }

    