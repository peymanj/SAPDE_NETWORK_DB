from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *
class UiOrderPalletRelationForm(UiBaseClass):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    _model = 'order_pallet_relation'
    _menu_bar = False
    _list_view = {
        'first_list': {'source': 'UiOrderPalletRelationForm'}
    }

    _form_view = {
        'fields': [
            'order',
            'pallet',
        ],

    }

    