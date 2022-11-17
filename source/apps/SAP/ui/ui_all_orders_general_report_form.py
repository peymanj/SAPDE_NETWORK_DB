from source.framework.intergration.port import port_read
from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *
from source.framework.intergration.port.port_read import PortRead
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette
from datetime import datetime
from source.framework.utilities import tr

class UiAllOrdersGeneralReportForm(UiBaseClass):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    _menu_bar = False
    _model = 'all_orders_general_report'

    _list_view = {
        'first_list': {'source': 'UiAllOrdersGeneralReportForm'}
    }

    _form_view = {
        'fields': [
            'order',
            'order_item',
            'pallet',
            'box',
            'model',
            'size',
            'item_set',
            'side',
            'weight',
            'sn1',
            'sn2',
            'sn3',
            'sn4',
            'sn5',
            'sn6',
            'sn7',
            'sn8',
            'check1',
            'check2',
            'check3',
            'check4',
            'check5',
            'check6',
            'check7',
            'check8',
            'check_user',
            'create_user',
            'update_date',
            ],
    }

    # _list_options = [
    #     {'name': 'Print report', 'action': 'print_order_rep'}
    # ]
