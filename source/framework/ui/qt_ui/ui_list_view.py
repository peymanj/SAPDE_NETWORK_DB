from .ui_shared_methods import get_ui_fields
from .ui_shared_methods import generate_list_view


def list_set(self, refresh=False):
    get_ui_fields(self)
    list_view = getattr(self.ui, '_list_view', None) 
    if not list_view: return

    meta_data = list_view.get('first_list', None)
    if meta_data.get('source'):
        access = self.api_get('get_ui_model_access', {'ui_model': meta_data.get('source'), 'mode': self.current_mode})
        source_ui_class = self.pool.get('ui_models').get(meta_data.get('source'))
    if not source_ui_class: return
    list_widget = generate_list_view(self, self, refresh=refresh)
    set_con_and_layout(self)
    if not refresh:
        self.baseFormListLayoutWidgetLayout.addWidget(list_widget, 0, 0, 1, 1)
    
def set_con_and_layout(self):
    # self.form_widget.formActionButtonWidget.setHidden(False)
    # self.form_widget.formCommandButtonWidget.setEnabled(False)
    # # self.listMainWidget.setHidden(True)
    # self.form_widget.formFieldsLabel.setText(tr('Details: ') + tr(self.model.title()))
    pass


