from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *
from source.framework.utilities import tr
from source.apps.SAP.ui.google_auth_form import GoogleAuthForm
class UiOrderForm(UiBaseClass):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def order_report(self):
        if self.get_active_id():
            self.signal.new_form.emit(self, 'UiPartsPerOrderReportForm', self.Mode.list_view, None, False)

    def all_order_general_report(self):
        self.signal.new_form.emit(self, 'UiAllOrdersGeneralReportForm', self.Mode.list_view, None, False)

    def upload_to_gdrive(self):
        if not self.active_id: self.msg.show(self.msg.Error, tr('No orders selected.'))
        res = self.api('exec', 'order', 'upload_order_to_gdrive', context={'id': self.active_id})
        if res.get('message') == 'cred_file_not_found':
            self.creds_input_form = GoogleAuthForm()
            self.creds_input_form.setupUi(self)
            self.creds_input_form.show()
            return
        self.msg.show(self.msg.Info, res.get('message'))
    _model = 'order'
    
    _menu_bar = False
    _list_view = {
        'first_list': {'source': 'UiOrderForm'}
    }

    _form_view = {
        'fields': [
            'code',
            'delivery_date',
            {'update_date': {'readonly': True}},
            {'create_user': {'readonly': True}},
            {'create_date': {'readonly':True}},
            'client_gmail',
            {'g_sheet': {'readonly':True}},
            'caption_set',
        ],
        'one2many': {'field': 'order_items', 'ui_model':'UiOrderItemForm'}
    }

    _list_options = [
        {'name': 'General Report', 'action': 'all_order_general_report'}
    ]

    _form_options = [
        {'name': 'Upload to Google drive', 'action': 'upload_to_gdrive'},
        {'name': 'Report', 'action': 'order_report'}
    ]

