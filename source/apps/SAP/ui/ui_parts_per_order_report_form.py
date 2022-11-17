from source.framework.intergration.port import port_read
from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *
from source.framework.intergration.port.port_read import PortRead
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette
from datetime import datetime
from source.framework.utilities import tr


class UiPartsPerOrderReportForm(UiBaseClass):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def context_set(self):
        self.context.update({'order_id': self.get_current_parent('order')})

    def print_order_rep(self):
        data = self.list_data
        if len(data) % 2 == 1:
            return

        wmax = 0
        wmin = 100000
        for i in range(0, len(data) - 1, 2):
            w1 = data[i].get('weight') or 0
            w2 = data[i + 1].get('weight') or 0
            w = w1 + w2
            if w > wmax:
                wmax = w
            if w < wmin:
                wmin = w

        visible_sn = dict.fromkeys(['sn%s' % i for i in range(1, 11)], False)
        visible_check = dict.fromkeys(['check%s' % i for i in range(1, 11)], False)
        visible_sn_count = 0
        visible_check_count = 0

        for c in range(1, 11):
            for rec in data:
                if rec.get('sn%s' % c) is not None:
                    visible_sn['sn%s' % c] = True
                    visible_sn_count += 1
                    break
        for c in range(1, 11):
            for rec in data:
                if rec.get('check%s' % c) is not None:
                    visible_check['check%s' % c] = True
                    visible_check_count += 1
                    break

        fields = boxes = self.api_get('get_model_fields', {'model': 'parts_per_order_report'})['fields']
        header = {}
        for f, obj in fields.items():
            header[f] = self.translate(obj['string'],  self.get_current_parent('order'))

        header['front'] = tr('Front')
        header['back'] = tr('Back')
        header['company_name'] = tr('Company Name')
        header['sap_order_report'] = tr('SAP Order Report')
        header['date'] = tr('Date')
        header['row'] = tr('Row')

        self.render_print_template(template_file='template_order_report.html',
                                   data=data,
                                   header=header,
                                   other_data={'date': str(datetime.now().replace(microsecond=0)),
                                               'max_weight': wmax,
                                               'min_weight': wmin,
                                               'visible_sn': visible_sn,
                                               'visible_check': visible_check,
                                               'visible_sn_count': visible_sn_count,
                                               'visible_check_count': visible_check_count,
                                               }
                                   )

    _menu_bar = False
    _model = 'parts_per_order_report'

    _list_view = {
        'first_list': {'source': 'UiPartsPerOrderReportForm'}
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

    _list_options = [
        {'name': 'Print report', 'action': 'print_order_rep'}
    ]
