from source.framework.ui.qt_ui.ui_base import UiBase


class UiBaseClassWizard(UiBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    _model = False


 
