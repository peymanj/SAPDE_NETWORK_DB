# shared methods to handle ui events


from typing import get_args
from source.framework.ui.qt_ui.extended_widgets import *
from PyQt5.QtCore import Qt, QSettings
from source.framework.utilities import tr
from .baseListViewWidget import BaseListViewWidget
from .baseFormViewWidget import BaseFormViewWidget


class Mode:
    create_view = 1
    update_view = 2
    list_view = 3
    form_view = 4


# Represents widget type depending on type of field in model and view
field_type_mapped = {
    'char': {
        Mode.create_view: ExtendedUserRoleLineEdit,
        Mode.form_view: ExtendedUserRoleLineEdit,
        Mode.update_view: ExtendedUserRoleLineEdit,
    },
    'date': {
        Mode.create_view: ExtendedDateEdit,
        Mode.form_view: ExtendedUserRoleLineEdit,
        Mode.update_view: ExtendedDateEdit,
    },
    'datetime': {
        Mode.create_view: ExtendedDateTimeEdit,
        Mode.form_view: ExtendedUserRoleLineEdit,
        Mode.update_view: ExtendedDateTimeEdit,
    },
    'boolean': {
        Mode.create_view: ExtendedCheckBox,
        Mode.form_view: ExtendedCheckBox,
        Mode.update_view: ExtendedCheckBox,
    },
    'many2one': {
        Mode.create_view: ExtendedComboBox,
        Mode.form_view: ExtendedUserRoleLineEdit,
        Mode.update_view: ExtendedComboBox,
    },
    'many2many': {
        Mode.create_view: ExtendedCheckableCombobox,
        Mode.form_view: ExtendedUserRoleLineEdit,
        Mode.update_view: ExtendedCheckableCombobox,
    },
    'integer': {
        Mode.create_view: ExtendedSpinBox,
        Mode.form_view: ExtendedUserRoleLineEdit,
        Mode.update_view: ExtendedSpinBox,
    },
    'binary': {
        Mode.create_view: ExtendedCaptureImageButton,
        Mode.form_view: ExtendedShowImageButton,
        Mode.update_view: ExtendedCaptureImageButton,
    },
    'selection': {
        Mode.create_view: ExtendedComboBox,
        Mode.form_view: ExtendedUserRoleLineEdit,
        Mode.update_view: ExtendedComboBox,
    },
}

# Represents widget properties available for each  fields in each view
field_property_map = {
    Mode.update_view: {
        'readonly': 'setReadOnly',
        'invisible': 'setHidden',
        'max': 'setMaximum',
        'min': 'setMinimum',
    },
    Mode.create_view: {
        'invisible': 'setHidden',
        'readonly': 'setReadOnly',
        'value': 'setValue',
        'max': 'setMaximum',
        'min': 'setMinimum',
    },
    Mode.form_view: {
        'invisible': 'setHidden',
    },
}


def eval_(val):
    try:
        return eval(val)
    except:
        return val


def get_ui_fields(self):
    # getting fields from ui_class file defined for model,
    # separating relationals and non-relationals
    self.ui._form_view = self.ui._update_view if self.ui._update_view else self.ui._form_view
    if self.ui._form_view:
        fields_list_dict = self.ui._form_view.get('fields', None)
        fields_list = list()
        fields_data = dict()
        for item in fields_list_dict:
            if isinstance(item, dict):
                fields_list += list(item.keys())
                fields_data.update(item)
            elif isinstance(item, str):
                fields_list.append(item)
                fields_data.update({item: dict()})

        non_o2m_fields = list(fields_list)
        m2o = list()
        m2m = list()
        o2m = list()
        selection = list()
        res = self.api_get('get_model_fields', {'model': self.model})
        for name, data in res['fields'].items():
            if data['type'] == 'many2one' and name in fields_list:
                m2o.append(name)
            if data['type'] == 'many2many' and name in fields_list:
                m2m.append(name)
            if data['type'] == 'selection' and name in fields_list:
                selection.append(name)
            if data['type'] == 'one2many' and name in fields_list:
                o2m.append(name)
                non_o2m_fields.remove(name)

    class ui_fields:
        def __init__(self, *args) -> None:
            self.m2o = args[0]
            self.o2m = args[1]
            self.m2m = args[2]
            self.selection = args[3]
            self.non_o2m_fields = args[4]
            self.all = args[5]
            self.data = args[6]

    setattr(self, 'ui_fields', ui_fields(
        m2o, o2m, m2m, selection, non_o2m_fields, fields_list, fields_data))


def add_field_to_form(self, name, form_widget, form_layout):
    field_obj = self._fields.get(name)

    ftype = field_obj['type']
    fclass = field_type_mapped.get(ftype).get(self.current_mode)
    if fclass:
        field_widget = fclass(objectName=name)
        label = ExtendedLabel(self.translate(field_obj['string'], self.get_current_parent('order')) + ':')
        form_layout.addRow(label, field_widget)
        setattr(form_widget, name + '_label', label)
        setattr(form_widget, name + '_qwidget', field_widget)
        try:
            getattr(form_widget, name + '_qwidget').setAlignment(Qt.AlignCenter)
        except Exception as e:
            pass

        if self.current_mode in (Mode.create_view, Mode.update_view):
            if ftype == 'many2one':
                init_m2o(self, name, form_widget)
            if ftype == 'many2many':
                init_m2m(self, name, form_widget)
            if ftype == 'selection':
                init_selection(self, name, form_widget)

        set_on_change(self, name, field_widget, form_widget)
        set_widget_prop(self, name, field_widget, label)


def set_widget_prop(self, name, field_widget, label):
    ui_field_data = self.ui_fields.data.get(name)
    if self.current_mode == self.Mode.form_view:
        field_widget.setReadOnly(True)
    for prop, val in ui_field_data.items():
        prop = field_property_map.get(self.current_mode).get(prop, None)
        if prop:
            getattr(field_widget, prop)(eval_(val))

        if ui_field_data.get('invisible', False):
            label.setHidden(True)


def onchange_function_parser(self, string):
    f_name = string.split('(')[0].strip()
    try:
        # f = self.api('get_model_field', context={'model': self.model, 'field_name': f_name})['field']
        # if not f:
        #     raise TypeError
        fields_str = string.split('(')[1].split(')')[0]
        fields = fields_str.split(',')
        for i in range(len(fields)):
            fields[i] = fields[i].strip()
            if fields[i] not in self._fields.keys():
                raise TypeError
        return f_name, fields
    except:
        return None, None


def return_process(self, data, form_widget):
    prop_mapped = {  # processing  data returned from onchange action in model
        'value': 'setValue',
        'readonly': 'setReadOnly',
        'invisible': 'setHidden',
    }

    for prop, fields_data in data.items():
        if prop_mapped.get(prop, None):
            try:
                val = eval(val)
            except:
                pass
            for field, val in fields_data.items():
                getattr(getattr(form_widget, field + '_qwidget'), prop_mapped.get(prop))(val)
        if prop.lower() == 'domain':
            for field, val in fields_data.items():
                # field_obj = self._fields.get(field)
                data = get_m2o_data(self, field, val)
                getattr(getattr(form_widget, field + '_qwidget'), prop_mapped.get(prop))(data)


def onchange_handler(self, f, fields, form_widget):
    def func():
        fields_ = list(fields)
        data = self.get_form_fields(form_widget, fields_)
        for i in range(len(fields_)):
            fields_[i] = data.get(fields_[i])
        context = {
            'field_values': self.get_form_fields(form_widget),
            'id': self.active_id,
        }
        ret = self.api('exec', self._model, f, {'args': fields_})
        return_process(self, ret, form_widget)

    return func


def function_parser(self, string):
    f_name = string.split('(')[0].strip()
    try:
        f = self.api_get('get_model_field', {'model': self.model, 'field_name': f_name})['field']
        if not f:
            raise TypeError
        fields_str = string.split('(')[1].split(')')[0]
        fields = fields_str.split(',')
        for i in range(len(fields)):
            fields[i] = fields[i].strip()
            if fields[i] not in self._fields.keys():
                raise TypeError
        return f, fields
    except:
        return None, None


def set_on_change(self, name, field_widget, form_widget):
    if 'onchange' in self.ui_fields.data.get(name):
        func, args = onchange_function_parser(self, self.ui_fields.data.get(name).get('onchange'))
        field_widget.setOnChange(onchange_handler(self, func, args, form_widget))


def get_m2o_data(self, name, domain=None):
    field_obj = self._fields.get(name)
    context = {'as_relational': True, 'return_object': False, 'return_dict': False}
    id = self.get_current_parent(field_obj['relation'])
    if id:
        context.update({'ids': [id]})
        data = self.api('exec', field_obj['relation'], 'read', context=context)
        return data

    if domain:
        context.update({'condition': domain})
        data = self.api('exec', field_obj['relation'], 'search', context=context)
    else:
        data = self.api('exec', field_obj['relation'], 'read', context=context)
    return data


def get_m2m_data(self, name):
    field_obj = self._fields.get(name)
    source_field = field_obj['source_field']
    target_field = field_obj['target_field']
    context = {'return_object': False, 'return_dict': False}
    condition = [(source_field, '=', self.active_id)]
    context.update({'condition': condition})
    data = self.api('exec', field_obj['relation'], 'search', context=context)
    ids = list()
    if data:
        for rec in data:
            ids.append(rec.get(target_field))
    return ids


def set_m2m_data(self, name: str, ids: list):
    field_obj = self._fields.get(name)

    current_ids = get_m2m_data(self, name)
    for id in ids:  # creating newly added records in dest M2M table
        if id not in current_ids:
            context = {'field_values': {
                field_obj['source_field']: self.active_id,
                field_obj['target_field']: id
            },
            }
            self.api('exec', field_obj['relation'], 'create', context=context)
        else:
            current_ids.remove(id)
    for id in current_ids:
        condition = [(field_obj['target_field'], '=', id)]
        context = {'condition': condition}
        self.api('exec', field_obj['relation'], 'delete', context=context)


def init_m2o(self, name, form_widget):
    if 'domain' in self.ui_fields.data.get(name):
        data = get_m2o_data(self, name, self.ui_fields.data.get('domain'))
    else:
        data = get_m2o_data(self, name)
    getattr(form_widget, name + '_qwidget').setValue(data)


def init_m2m(self, name, form_widget):
    field_widget = getattr(form_widget, name + '_qwidget')
    field_obj = self._fields.get(name)
    target_field = field_obj['target_field']
    feed_model_name = \
    self.api('get_model_field', {'model': field_obj['relation'], 'field_name': target_field})['field']['relation']

    context = {'as_relational': True, 'return_object': False, 'return_dict': False}
    if 'domain' in self.ui_fields.data.get(name):
        domain = self.ui_fields.data.get(name).get('domain')
        context.update({'condition': domain})
        data = self.api('exec', feed_model_name, 'search', context=context)
    else:
        data = self.api('exec', feed_model_name, 'read', context=context)
    field_widget.setValue(data)

    if self.current_mode in (Mode.update_view,):
        field_widget.set_checked(get_m2m_data(self, name))


def init_selection(self, name, form_widget):
    method_name = self._fields.get(name)['func']
    local_data = self._fields.get(name)['local_data']
    if local_data:
        data = getattr(self.ui, local_data)()
    else:
        context = {'order_id': self.get_current_parent('order')}
        data = self.api('exec', self.model, method_name, context)
    getattr(form_widget, name + '_qwidget').setValue(data)


def load_defaults(self):
    defaults = self.api('exec', self.model, 'get_defaults', context=self.context)
    self.set_form_fields(self.form_widget, defaults, set_default=True)


def get_data_from_db(self, id=None, model=None, condition=None):
    self.context.update({'return_object': False, 'return_dict': False, 'post_proc': True})
    if id:
        self.context.update({'ids': [id]})
        data = self.api('exec', model, 'read', context=self.context)
    if condition:
        self.context.update({'condition': condition})
        data = self.api('exec', model, 'search', context=self.context)
    else:
        data = self.api('exec', model, 'read', context=self.context)
        if data:
            if self.current_mode in (self.Mode.form_view, self.Mode.update_view):
                id_col = self.api_get('get_model_parameter', {'model': model, 'param': '_id_column'})['_id_column']
                self.active_id = data[0].get(id_col)

    for f, meta in self._fields.items():
        if meta['local_data']:
            for i in range(len(data)):
                if f in data[i]:
                    id = QSettings('sapde', 'sapde').value(f)
                    data[i][f] = getattr(self.ui, meta['local_data'])(id=id) if id else False
    return data
    #


def generate_list_view(self, ui_model, manual_data=None,
                       active_id_name='active_id', condition=None, refresh=False):
    qtreewidget_name = 'listFirstTableWidget'
    if not refresh:
        list_widget = BaseListViewWidget()
        list_widget.setupUi(list_widget)
    else:
        list_widget = self.list_widget

    model = ui_model._model
    if not model:
        return
    model_fields = self.api_get('get_model_fields', {'model': model})['fields']

    if manual_data or isinstance(manual_data, (tuple, list)):
        self.list_data = manual_data
    else:
        self.list_data = get_data_from_db(self, model=model, condition=condition)
    headers = [h.strip() for h in self.api_get('get_visible_fields', {'model': model, 'view_mode': '1'}) \
        ['fields'].split(',')]
    order_id = self.get_current_parent('order')
    getattr(list_widget, qtreewidget_name) \
        .set_table_widget(self.list_data,
                          headers,
                          sort_col='id',
                          order='asc',
                          search_signal=self.signal.open_search,
                          model_fields=model_fields,
                          model=model,
                          order_id=order_id,
                          )
    list_widget.listLabel.setText(tr(model).title())
    if refresh:
        return list_widget

    get_active_id = list_widget.listFirstTableWidget.get_active_id  # method

    methods = {
        'Create': lambda: self.signal.new_form.emit(self, ui_model,
                                                    ui_model.Mode.create_view, None, False),
        'Edit': lambda: self.signal.new_form.emit(self, ui_model,
                                                  ui_model.Mode.update_view, get_active_id(), False),
        'Delete': lambda: ui_model.signal.delete.emit(get_active_id()),
        'Refresh': ui_model.refresh,
    }
    list_widget.listCreatePushButton.disconnect()
    list_widget.listUpdatePushButton.disconnect()
    list_widget.listDeletePushButton.disconnect()
    list_widget.listCreatePushButton.clicked.connect(methods.get('Create'))
    list_widget.listUpdatePushButton.clicked.connect(methods.get('Edit'))
    list_widget.listDeletePushButton.clicked.connect(methods.get('Delete'))

    getattr(list_widget, qtreewidget_name).connect_context_menu(methods, model_fields)
    getattr(list_widget, qtreewidget_name).doubleClicked.disconnect()
    getattr(list_widget, qtreewidget_name).doubleClicked.connect(
        lambda: self.signal.new_form.emit(self, type(ui_model).__name__,
                                          self.Mode.form_view, get_active_id(), False))
    if not refresh:
        self.list_widget = list_widget
    return list_widget


def generate_form_view(self, ui_model):
    get_ui_fields(self)
    form_widget = BaseFormViewWidget()
    form_widget.setupUi(form_widget)
    form_layout = form_widget.formFieldLayout
    if self.ui_fields.non_o2m_fields:
        for name in self.ui_fields.non_o2m_fields:
            add_field_to_form(self, name, form_widget, form_layout)
    self.form_widget = form_widget
    return form_widget


def set_relationals_from_parent(self):
    if self.ui_fields.m2o:
        model_fields = self.api_get('get_model_fields', {'model': self.model})['fields']
    else:
        return

    for field in self.ui_fields.m2o:
        f_obj = model_fields.get(field)
        parent_id = self.get_current_parent(f_obj['relation'])

        if not parent_id: continue
        data = self.api('exec', f_obj['relation'], 'read', {'ids': [parent_id], 'as_relational': True})
        self.set_form_fields(self.form_widget, {field: data})
        getattr(self.form_widget, field + '_qwidget').setCurrentIndex(0)


def check_required_fields(self):
    form_data = self.get_form_fields(self.form_widget)
    failed_fields = []
    for f in form_data:
        f_data = self._fields.get(f)
        if f_data.get('required') and f_data.get('type') != 'boolean' and not form_data.get(f):
            failed_fields.append(self.translate(f_data.get('string'), self.get_current_parent('order')) + '\n')
    if failed_fields:
        self.msg.show(self.msg.Error, 'Required fields:', add_msg=''.join(failed_fields))
    return form_data
