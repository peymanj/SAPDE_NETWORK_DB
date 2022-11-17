from source.framework.ui.qt_ui.extended_widgets import *
from PyQt5.QtCore import Qt, QSettings
from source.framework.utilities import tr
from .ui_shared_methods import set_m2m_data, get_data_from_db, generate_form_view, check_required_fields



def update_set(self):
    form_widget = generate_form_view(self, self)    
    self.baseFormListLayoutWidgetLayout.addWidget(form_widget, 0, 0, 1, 1)
    set_con_and_layout(self)
    data = get_data_from_db(self, self.active_id, self._model)[0]
    non_rel_data = dict(data)
    for field in data:
        if field in self.ui_fields.m2o:
            non_rel_data.pop(field)
            field_widget = getattr(self.form_widget, field  + '_qwidget').set_current_item(data.get(field))
        if field in self.ui_fields.selection:
            non_rel_data.pop(field)
            field_widget = getattr(self.form_widget, field  + '_qwidget').set_current_item(data.get(field))
        elif field in self.ui_fields.m2m:
            non_rel_data.pop(field) 
    self.set_form_fields(self.form_widget, non_rel_data)


def set_con_and_layout(self):
    self.form_widget.formActionButtonWidget.setHidden(True)
    self.form_widget.formCommandButtonWidget.setEnabled(True)
    self.form_widget.formFieldsLabel.setText(tr('Edit') + ': ' + tr(self.model.title()))
    self.save_method = save
    self.form_widget.formCancelPushButton.clicked.connect(self.signal.close_form.emit)
    self.form_widget.formSavePushButton.disconnect()
    self.form_widget.formSavePushButton.clicked.connect(self.save)

# def set_update_data(self):
#     self.set_form_fields(self.form_widget, get_data_from_db(self, self.active_id))

def save(self):
    form_data = check_required_fields(self)
    non_m2m_form_data = dict(form_data)
    for field in form_data:
        if field in self.ui_fields.m2m:
            set_m2m_data(self, field, form_data.get(field))
            non_m2m_form_data.pop(field)
    
    context = {
            'field_values': non_m2m_form_data,
            'id': self.active_id,
        }
    self.api('exec', self.model, 'update', context=context)
    for f, v in form_data.items():
        if self._fields.get(f)['local_data']:
            QSettings('sapde', 'sapde').setValue(f, v)
    self.signal.refresh.emit()
