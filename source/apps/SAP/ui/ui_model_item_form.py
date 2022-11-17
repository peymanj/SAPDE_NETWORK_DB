from source.framework.ui.qt_ui.ui_base_class import UiBaseClass

class UiModelItemForm(UiBaseClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    _menu_bar = False
    _model = 'model_item'
    
    _list_view = {
        'first_list': {'source': 'UiModelItemForm'}
    }

    _form_view = {
        'fields': [
            'model',
            'size',
            'min_weight_front',
            'max_weight_front',
            'min_weight_back',
            'max_weight_back',
            {'no_front_serials': {'max':8}},
            {'no_back_serials': {'max':8}},
        ]

    }

    