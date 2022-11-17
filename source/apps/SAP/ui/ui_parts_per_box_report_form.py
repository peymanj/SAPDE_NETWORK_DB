from source.framework.ui.qt_ui.ui_base_class import UiBaseClass

from datetime import datetime
from source.framework.utilities import tr

class UiPartsPerBoxReportForm(UiBaseClass):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def context_set(self):
        self.context.update({'box': self.get_current_parent('box')})
        return super().context_set()
       

    def print_box_rep(self):
        data = self.list_data
        if len(data) % 2 == 1:
            self.msg.show(self.msg.Error, tr('Incomplete set detected'))
        wmax = 0
        wmin = 100000
        for i in range(0, len(data)-1, 2):
            w1 = data[i].get('weight') or 0
            w2 = data[i+1].get('weight') or 0
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
        fields = boxes = self.api_get('get_model_fields', {'model': 'parts_per_box_report'})['fields']
        header = {}
        for f, obj in fields.items():
            header[f] = self.translate(obj['string'],  self.get_current_parent('order'))

        header['front'] = tr('Front')
        header['back'] = tr('Back')
        header['company_name'] = tr('Company Name')
        header['sap_box_report'] = tr('SAP Box Report')
        header['date'] = tr('Date')
        header['max_weight'] = tr('Max weight')
        header['min_weight'] = tr('Min weight')
        header['row'] = tr('Row')
        header['set_weight'] = tr('Set weight')



        self.render_print_template(template_file='template_box_report.html',
                                   header=header,
                                   data=data,
                                   other_data={'date': str(datetime.now().replace(microsecond=0)),
                                               'max_weight': wmax,
                                               'min_weight': wmin,
                                               'visible_sn': visible_sn,
                                               'visible_check': visible_check,
                                               'visible_sn_count': visible_sn_count,
                                               'visible_check_count': visible_check_count,
                                               }
                                   )

    _model = 'parts_per_box_report'
     
    _menu_bar = False
    _list_view = {
        'first_list': {'source': 'UiPartsPerBoxReportForm'}
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
        {'name':'Print report', 'action': 'print_box_rep'}
    ]
