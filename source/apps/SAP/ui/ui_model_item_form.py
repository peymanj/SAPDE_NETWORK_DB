from source.framework.ui.qt_ui.ui_base_class import UiBaseClass

class UiModelItemForm(UiBaseClass):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_layout(self):
        n_parts = self.get_form_fields(self.form_widget, ['n_parts']).get('n_parts')
        var_fields = ['weight_disp_', 'length_disp_', 'width_disp_',  'thickness_disp_', 'no_serials_']
        for i in range(1, 5):
            if i > n_parts:
                for field in var_fields:
                    getattr(self.form_widget, field + str(i) + '_qwidget').setValue(False)
                    getattr(self.form_widget, field + str(i) + '_qwidget').setHidden(True)
                    getattr(self.form_widget, field + str(i) + '_label').setHidden(True)
            else:
                for field in var_fields:
                    getattr(self.form_widget, field + str(i) + '_qwidget').setHidden(False)
                    getattr(self.form_widget, field + str(i) + '_label').setHidden(False)
    def create_init(self):
        getattr(self.form_widget, 'n_parts_qwidget').valueChanged.connect(self.set_layout)
        self.set_layout()
        return super().create_init()

    def update_init(self):
        getattr(self.form_widget, 'n_parts_qwidget').valueChanged.connect(self.set_layout)
        self.set_layout()
        return super().update_init()

    def form_init(self):
        self.set_layout()
        return super().form_init()

    _menu_bar = False
    _model = 'model_item'
    
    _list_view = {
        'first_list': {'source': 'UiModelItemForm'}
    }

    _form_view = {
        'fields': [
            'model',
            'size',
            {'n_parts': {'min': 1, 'max': 4}},
            'weight_disp_1',
            'length_disp_1',
            'width_disp_1',
            'thickness_disp_1',
            {'no_serials_1': {'min': 1, 'max': 8}},
            'weight_disp_2',
            'length_disp_2',
            'width_disp_2',
            'thickness_disp_2',
            {'no_serials_2': {'min': 1, 'max': 8}},
            'weight_disp_3',
            'length_disp_3',
            'width_disp_3',
            'thickness_disp_3',
            {'no_serials_3': {'min': 1, 'max': 8}},
            'weight_disp_4',
            'length_disp_4',
            'width_disp_4',
            'thickness_disp_4',
            {'no_serials_4': {'min': 1, 'max': 8}},
        ]

    }

    