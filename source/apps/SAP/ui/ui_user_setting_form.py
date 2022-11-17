from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *


class UiUserSettingForm(UiBaseClass):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    _model = 'user_setting'
    _menu_bar = False
    _list_view = {
        'first_list': {'source': 'UiUserSettingForm'}
    }

    _form_view = {
        'fields': [
            'theme',
        ],

    }

