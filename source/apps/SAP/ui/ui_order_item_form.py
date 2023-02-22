from source.framework.ui.qt_ui.ui_base_class import UiBaseClass

class UiOrderItemForm(UiBaseClass):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_layout(self):

        set_id = self.get_form_fields(self.form_widget, ['item_set']).get('item_set')
        order_item_id = self.api('exec', 'item_set', 'related_read', context={'id': set_id, 'field': 'order_item'})
        self.order_item = self.api('exec', 'order_item', 'read',
                                   {'ids': [order_item_id], 'post_proc': False, 'return_object': False})[0]

        self.check_list = list()
        for i in range(8):
            if i >= self.order_item['no_fchecks']:
                getattr(self.form_widget, 'check' + str(i + 1) + '_qwidget').setHidden(True)
                getattr(self.form_widget, 'check' + str(i + 1) + '_label').setHidden(True)
            else:
                self.check_list.append(getattr(self.form_widget, 'check' + str(i + 1) + '_qwidget').getValue())


        if not self.order_item['image_required']:
            getattr(self.form_widget, 'image_qwidget').setEnabled(False)

        if not self.order_item['check_weight']:
            getattr(self.form_widget, 'weight_qwidget').setEnabled(False)

        self.model_size_rel = self.api('exec', 'model_item', 'search',
                                       {'condition': ['and', ('model', '=', self.order_item['model']),
                                                      ('size', '=', self.order_item['size'])],
                                        'post_proc': False, 'return_object': False})[0]
        self.set_serials()

    _menu_bar = False
    _model = 'order_item'

    _list_view = {
        'first_list': {'source': 'UiOrderItemForm'}
    }

    _form_view = {
        'fields': [
            'order_id',
            {'model': {'onchange': '_onchange_model(model)'}},
            {'size': {'default': False}},
            {'quantity': {'min': 1}},
            'pallet_no',
            {'no_per_box': {'min': 1, 'max': 50}},
            {'no_fchecks': {'max': 8}},
            'image_required',
            'check_weight',
            'check_length',
            'check_width',
            'check_thickness',
            'unique_serial',
            # 'status_disp',
        ],
        'one2many': {'field': 'boxes', 'ui_model':'UiBoxForm'}

    }
