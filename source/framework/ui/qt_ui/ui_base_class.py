from source.framework.ui.qt_ui.ui_base_layout import UiBaseLayout

class UiBaseClass(UiBaseLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    _model = False

    _base_menu_bar = False
    # _base_menu_bar = {
    #     'File': {'parent': False, 'action': 'model'},
    #     'Model': {'parent': False, 'action': 'model'} ,
    #     'order': {'parent': 'model', 'action': 'order'},
    # }
    _form_menu_bar = False
    _status_bar = False
    
    _list_veiw = False #{
    #     'first_list': False, # {'source': field}
    #     'second_list': False,
    #     'third_list': False,
    # }
    
    _form_view = False    # used for create and form view
    #       'one2many': False # {'source': field}

    
    _update_view = False  # if not defined, form view is used

    _list_options = False
    # [
    #     {'name':'Print', 'action': 'print_form'}
    # ]
    _form_options = False
 
