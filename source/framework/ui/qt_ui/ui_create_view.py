from source.framework.utilities import tr
from .ui_shared_methods import set_m2m_data, load_defaults, generate_form_view, \
    set_relationals_from_parent, check_required_fields


def create_set(self):
    form_widget = generate_form_view(self, self)
    self.baseFormListLayoutWidgetLayout.addWidget(form_widget, 0, 0, 1, 1)
    set_con_and_layout(self)
    load_defaults(self)
    set_relationals_from_parent(self)

def set_con_and_layout(self):
    self.form_widget.formActionButtonWidget.setHidden(True)
    self.form_widget.formCommandButtonWidget.setEnabled(True)
    self.form_widget.formFieldsLabel.setText(tr('New') + ': ' + tr(self.model.title()))
    self.save_method = save
    self.save_and_create_new_method = save_and_create_new
    self.form_widget.formCancelPushButton.clicked.connect(self.signal.close_form.emit)
    self.form_widget.formSavePushButton.disconnect()
    self.form_widget.formSavePushButton.clicked.connect(self.save)

def save_procedure(self, form_data):
    non_m2m_form_data = dict(form_data)
    for field in form_data:
        if field in self.ui_fields.m2m:
            set_m2m_data(self, field, form_data.get(field))
            non_m2m_form_data.pop(field)
    context = {'field_values': non_m2m_form_data,}
    id = self.api('exec', self.model, 'create', context=context)

def close_after_save(self):
    self.signal.refresh.emit()

def save(self):
    form_data = check_required_fields(self)
    save_procedure(self, form_data)
    close_after_save(self)

def save_and_create_new(self):
    self.save()
    id = self.reopen_create_preprocess()
    if id:
        self.set_current_parent('item_set', id)
        self.signal.new_form.emit(self.form_parent, self, self.Mode.create_view, None, False)


    
