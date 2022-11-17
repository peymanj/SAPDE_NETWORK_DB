from source.framework.ui.qt_ui.ui_base_class import UiBaseClass

class UiTranslationForm(UiBaseClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    _menu_bar = False
    _model = 'translation'
    
    _list_view = {
        'first_list': {'source': 'UiTranslationForm'}
    }

    _form_view = {
        'fields': [
            'phrase',
            'translation',
        ]

    }

    