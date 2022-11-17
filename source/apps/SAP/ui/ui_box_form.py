import math
from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *
class UiBoxForm(UiBaseClass):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def report(self):
        if self.active_id:
            self.signal.new_form.emit(self, 'UiPartsPerBoxReportForm', self.Mode.list_view, None, False)
    
    def context_set(self):
        self.context.update({'order_item_id': self.get_current_parent('order_item')})
    
    def create_view(self):
        self.check_box_count()
        return super().create_view()

    def check_box_count(self):
        order_item  = self.get_current_parent('order_item')
        order_item_obj = self.api('exec', 'order_item', 'read', context={
            'ids': [order_item], 
            'fields': ['quantity', 'no_per_box'], 
            'return_object': False
            })[0]
        n_boxes_required = math.ceil(order_item_obj['quantity'] / order_item_obj['no_per_box'])
        boxes = self.api('exec', 'box', 'search', 
                context={'condition':[('order_item', '=', order_item)], 'fields':['status']})
        n_current_box = len(boxes)

        if n_current_box >= n_boxes_required:
            self.msg.show(self.msg.Error, 'Max boxes per order item reached.',
                add_msg=f'Max box per order item allowed: {n_boxes_required}')

    _model = 'box'
    _menu_bar = False
    _list_view = {
        'first_list': {'source': 'UiBoxForm'}
    }

    _form_view = {
        'fields': [
            {'order_item': {'readonly':True, }},
            'code',
            # 'status_disp',
        ],
        'one2many': {'field': 'item_sets', 'ui_model':'UiItemSetForm'}

    }

    _form_options = [
        {'name':'Report', 'action': 'report'}
    ]
