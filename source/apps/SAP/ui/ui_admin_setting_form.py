from source.framework.ui.qt_ui.ui_base_class import UiBaseClass


class UiAdminSettingForm(UiBaseClass):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self):
        super().init()
        if hasattr(self, 'form_widget'):
            self.form_widget.master_password_qwidget.showEye()

    _model = 'admin_setting'
    _menu_bar = False
    _list_view = {
        'first_list': {'source': 'UiAdminSettingForm'}
    }

    _form_view = {
        'fields': [
            'master_password',
        ],

    }

    