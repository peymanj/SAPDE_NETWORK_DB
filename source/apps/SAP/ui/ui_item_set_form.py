from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *
class UiItemSetForm(UiBaseClass):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def create_view(self):
        self.check_item_set_count()
        super().create_view()


    def check_item_set_count(self):
        current_box  = self.get_current_parent('box')
        current_order_item = self.api('exec', 'box', 'search', 
            context={'condition': [('id', '=', current_box)]})[0].get('order_item')
        current_items_per_box = self.api('exec', 'item_set', 'search', 
            {'condition': [('box', '=', self.get_current_parent('box'))]})
        n_current_items = len(current_items_per_box) if current_items_per_box else 0
        n_max_raw_per_box = self.api('exec', 'order_item', 'search', 
            {'condition': [('id', '=', current_order_item)], 'fields': ['no_per_box', 'quantity']})[0]
        n_max_per_box = n_max_raw_per_box.get('no_per_box')
        if n_current_items >= n_max_per_box:
            self.msg.show(self.msg.Error, 'Max items per box count reached.',
                add_msg=f'Max items per box allowed: {n_max_per_box}')

        all_boxes = self.api('exec', 'box', 'search', 
            {'condition': [('order_item', '=', current_order_item)]})
        set_count = 0
        for rec in all_boxes:
            item_sets = self.api('exec', 'item_set', 'search', 
            {'condition': [('box', '=', rec.get('id'))]})
            set_count += len(item_sets) if item_sets else 0
        if set_count == n_max_raw_per_box.get('quantity'):
            self.msg.show(self.msg.Error, 'Max set count reached.')


    def context_set(self):
        self.context.update({'box_id': self.get_current_parent('box')})

    _model = 'item_set'
    
    _menu_bar = False
    _list_view = {
        'first_list': {'source': 'UiItemSetForm'}
    }

    _form_view = {
        'fields': [
            'box',
            'code',
            # 'status',
        ],
        'one2many': {'field': 'parts', 'ui_model':'UiPartForm'}


    }

    