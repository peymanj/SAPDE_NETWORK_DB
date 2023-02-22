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


        n_data = len(data)
        order_name = data[0].get('order')[1]
        order_item_data = {}
        ordered_data = {}
        for i in range(n_data):
            set_no = data[i]['item_set'][0]
            order_item_no = data[i]['order_item'][0]

            if order_item_no not in ordered_data:
                ordered_data[order_item_no] = {}
            if set_no not in ordered_data[order_item_no]:
                ordered_data[order_item_no][set_no] = {
                   'parts': [False] * 4,
                   'weight': 0,
                   'create_user': None,
                   'update_user': None,
                   'update_date': None,
            }
            ordered_data[order_item_no][set_no]['parts'][data[i]['side'][0]-1] = (data[i])
            if order_item_no not in order_item_data:
                order_item_data[order_item_no] = data[i]



        max_part_column = 0
        update_date = datetime(1900, 1, 1)

        for o_i in ordered_data:
            for i_s in ordered_data[o_i]:
                parts = ordered_data[o_i][i_s]['parts']
                max_part = 0
                for i in range(len(parts), 0, -1):
                    if parts[i-1]:
                        max_part = i
                        break

                if max_part > max_part_column:
                    max_part_column = max_part

                sum_weight = 0
                for part in ordered_data[o_i][i_s]['parts']:
                    sum_weight += part.get('weight', 0) if part else 0
                    if part and update_date < part["update_date"]:
                        update_date = part["update_date"]
                ordered_data[o_i][i_s]['weight'] = sum_weight
                ordered_data[o_i][i_s]['update_date'] = update_date


        wmax = 0
        wmin = 100000
        for o_i in ordered_data:
            for n in ordered_data[o_i]:
                i_s = ordered_data[o_i][n]
                if i_s.get('weight') > wmax:
                    wmax = i_s.get('weight')
            if i_s.get('weight') < wmin:
                wmin = i_s.get('weight')


        max_part_count = {
            1: {'sn': 0, 'check': 0},
            2: {'sn': 0, 'check': 0},
            3: {'sn': 0, 'check': 0},
            4: {'sn': 0, 'check': 0},
        }
        for o_i in ordered_data:
            for i_s in ordered_data[o_i]:
                for i in range(1, len(ordered_data[o_i][i_s]['parts']) + 1):
                    part = ordered_data[o_i][i_s]['parts'][i - 1]
                    sn = 0
                    check = 0
                    for c in range(1, 9):
                        if part and part.get('sn%s' % c) is not None:
                            sn += 1
                        if part and part.get('check%s' % c) is not None:
                            check += 1
                    if max_part_count[i]['sn'] < sn:
                        max_part_count[i]['sn'] = sn
                    if max_part_count[i]['check'] < check:
                        max_part_count[i]['check'] = check
                break

        fields = self.api_get('get_model_fields', {'model': 'parts_per_order_report'})['fields']
        header = {}
        for f, obj in fields.items():
            header[f] = self.translate(obj['string'], self.get_current_parent('order'))

        for i in range(1, 5):
            string = f'Part {i}'
            header[string] = self.pool.get('api').internal_exec('part', 'translate',
                                                                {'phrase': string,
                                                                 'model_id': self.get_current_parent('order')})

        # header['front'] = tr('Front')
        # header['back'] = tr('Back')
        header['company_name'] = tr('Company Name')
        header['sap_order_report'] = tr('SAP Order Report')
        header['date'] = tr('Date')
        header['row'] = tr('Row')
        header['total_weight'] = tr('Total weight')


        visible_parts = {}
        for i in range(1, 5):
            visible_parts[i] = {}
            if i <= max_part_column:
                visible_parts[i]['visible'] = True
                sn = max_part_count[i]['sn']
                check = max_part_count[i]['check']
            else:
                visible_parts[i]['visible'] = False
                sn = 0
                check = 0

            visible_parts[i]['visible_sn_count'] = [True]*sn + [False]*(8-sn)
            visible_parts[i]['visible_check_count'] = [True]*check + [False] * (8 - check)

        self.render_print_template(template_file='template_order_report.html',
                                   data=ordered_data,
                                   header=header,
                                   other_data={
                                       'order': order_name,
                                       'date': str(datetime.now().replace(microsecond=0)),
                                       'max_weight': wmax,
                                       'min_weight': wmin,
                                       },
                                   visibility=visible_parts,
                                   field_count=max_part_count,
                                   order_item_data=order_item_data,
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
