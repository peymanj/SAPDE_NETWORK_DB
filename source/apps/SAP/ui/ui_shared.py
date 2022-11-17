from source.framework.ui.qt_ui.ui_base_class import UiBaseClass

class UiShared(UiBaseClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    _menu_bar = {
        'Data':     {} ,
        'Models':   {'parent': 'Data', 'action': 'UiModelForm'},
        'Sizes':   {'parent': 'Data', 'action': 'UiSizeForm'},
        'Model - Size relation':   {'parent': 'Data', 'action': 'UiModelItemForm'},
        'Pallets':   {'parent': 'Data', 'action': 'UiPalletForm'},
        'Caption Sets': {'parent': 'Data', 'action': 'UiCaptionSetForm'},
        'Orders':   {'parent': 'Data', 'action': 'UiOrderForm'},
        'Users':   {'parent': 'File', 'action': 'UiUserForm'},
        'Database': {'parent': 'File', 'action': 'UiDatabaseManagementForm', 'view': 'list_view'},
        'App Setting':   {'parent': 'File', 'action': 'UiAppSettingForm', 'view': 'list_view'},
        'User Setting': {'parent': 'File', 'action': 'UiUserSettingForm', 'view': 'list_view'},
        'Administration Setting': {'parent': 'File', 'action': 'UiAdminSettingForm', 'view': 'list_view'},
        'Translations': {'parent': 'File', 'action': 'UiTranslationForm', 'view': 'list_view'},

    }
    