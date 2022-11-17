from source.framework.ui.qt_ui.ui_base_class import UiBaseClass

class UiSizeForm(UiBaseClass):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    _menu_bar = False
    _model = 'size'
    
    _list_view = {
        'first_list': {'source': 'UiSizeForm'}
    }

    _form_view = {
        'fields': [
            'name',
        ]

    }

    