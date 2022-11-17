from .ui_shared_methods import generate_form_view, get_data_from_db, get_m2m_data,generate_list_view
from source.framework.utilities import tr

def form_set(self, refresh=False):

    if not refresh:
        form_widget = generate_form_view(self, self)
        self.baseFormListLayoutWidgetLayout.addWidget(form_widget, 0, 0, 1, 1)
        set_con_and_layout(self)
    self.set_form_fields(self.form_widget, get_data_from_db(self, id=self.active_id, model=self._model))

    if self.ui_fields.m2m:
        for name in self.ui_fields.m2m:
            ids = get_m2m_data(self, name)
            field_obj = self._fields.get(name)
            target_field = field_obj['target_field']
            feed_model_name = self._fields\
                .get(name)['relation']
            target_model_name = self.api_get('get_model_field', {'model': feed_model_name, 'field_name': target_field})['field']['relation']
            data = self.api('exec', target_model_name, 'read', context={
                'ids': ids, 'return_object': False, 'return_dict': False, 'as_relational': True})
            self.set_form_fields(self.form_widget, {name: data})
    if self.ui._form_view.get('one2many'):
        set_one2many(self, self._form_view.get('one2many'), refresh=refresh)
    elif self.ui._form_view.get('many2many'):
        set_many2many(self, self._form_view.get('many2many'), refresh=refresh)

def set_con_and_layout(self):
    self.form_widget.formActionButtonWidget.setHidden(False)
    self.form_widget.formCommandButtonWidget.setEnabled(False)
    # self.listMainWidget.setHidden(True)
    self.form_widget.formFieldsLabel.setText(tr('Details: ') + tr(self.model.title()))
    
    self.form_widget.formUpdatePushButton.disconnect()
    self.form_widget.formUpdatePushButton.clicked.connect \
            (lambda: self.signal.new_form.emit(self, self,\
                self.Mode.update_view, self.active_id, False))
    self.form_widget.formCreatePushButton.disconnect()
    self.form_widget.formCreatePushButton.clicked.connect \
        (lambda: self.signal.new_form.emit(self, self,\
            self.Mode.create_view, None, False))
    self.form_widget.formDeletePushButton.disconnect()
    self.form_widget.formDeletePushButton.clicked.connect\
        (lambda: self.signal.delete.emit(self.active_id))

def set_one2many(self, o2m_data, refresh=False):
   
    ui_model_name = o2m_data.get('ui_model')
    f_name = o2m_data.get('field')

    if not ui_model_name: return
    if not f_name: return
    
    fobj = self._fields.get(f_name)
    target_field = fobj['field']
    context = {
        'condition': [(target_field, '=', self.active_id)],
        'return_object': False,
        'return_dict': False,
        'post_proc': True,
        }
    data = self.api('exec', fobj['relation'], 'search', context=context)
    # ui_model = self.api('get_ui_model', ui_model_name, self.current_mode)
    ui_model = self.pool.get('ui_connector').generate_form_from_model(self, ui_model_name, self.Mode.list_view, add_nav=False)
    list_widget = generate_list_view(self, ui_model, manual_data=data, refresh=refresh)
    if not refresh:
        self.baseFormListLayoutWidgetLayout.addWidget(list_widget, 1, 0, 1, 1)


def set_many2many(self, m2m_data, refresh=False):
    ui_model_name = m2m_data.get('ui_model')
    f_name = m2m_data.get('field')

    if not ui_model_name: return
    if not f_name: return
    
    fobj = self._fields.get(f_name)
    connector_model_source_field = fobj['source_field']
    connector_model_target_field = fobj['target_field']
    connector_model = fobj['relation']
    target_model_name =  self.api_get('get_model_field', {'model': connector_model,
                                                      'field_name': connector_model_target_field})['field']['relation']
    context = {
        'condition': [(connector_model_source_field, '=', self.active_id)],
        'return_object': False,
        'fields': ['access'],
        'return_dict': False,
        }
    records = self.api('exec', connector_model, 'search', context=context)
    target_ids = list()
    if not records: records = list()
    for rec in records:
        target_ids.append(rec.get(connector_model_target_field))
    context = {
        'ids': target_ids,
        'return_dict': False,
        'return_object': False,
        }
    data = self.api('exec', target_model_name, 'read', context=context)
    ui_model = self.pool.get('ui_connector').generate_form_from_model(self, ui_model_name, self.Mode.list_view, add_nav=False)
    list_widget = generate_list_view(self, ui_model, manual_data=data, refresh=refresh)
    if not refresh:
        self.baseFormListLayoutWidgetLayout.addWidget(list_widget, 1, 0, 1, 1)

