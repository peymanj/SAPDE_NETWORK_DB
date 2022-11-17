from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QDateEdit, QDateTimeEdit, QCheckBox, QComboBox, QSpinBox
from PyQt5.QtCore import QDate, QEventLoop, QModelIndex, QLocale, QTimer, pyqtSignal
from .extended_widgets import *
import jinja2
import json
import tempfile
import webbrowser
from source.framework.config import current_app
from source.framework.pool import Pool
from source.framework.utilities import tr as _tr

types = [QDateTimeEdit, QLineEdit, QDateEdit, QCheckBox, QComboBox, QSpinBox, ExtendedLineEdit]


class Mode:
    create_view = 1
    update_view = 2
    list_view = 3
    form_view = 4


class UiBase:
    update_signal = pyqtSignal()
    field_map_dict = dict()  # {ui field name: db field name}
    model = str()
    active_id = None
    _use_template = True
    context = dict()
    pool = Pool
    Mode = Mode

    def __init__(self) -> None:
        super().__init__()
        self.api_obj = None  # limiting api full access in front
        self.setting = self.pool.get('setting')
        self.update_signal.connect(self.refresh)
        self.set_msgbox()

    def set_msgbox(self):
        self.msg = ExtendedMessageBox()

    def get_form_fields(self, base_widget, fields=None):
        if not fields:
            fields = list()
            for obj_name in dir(base_widget):
                if obj_name.endswith('_qwidget'):
                    fields.append(obj_name.replace('_qwidget', ''))

        data = dict()
        for field in fields:
            fval = getattr(base_widget, field + '_qwidget').getValue()
            if fval is not None:
                data.update({field: fval})
        return data

    def set_form_fields(self, base_widget, data=None, set_default=False):
        if data:
            if isinstance(data, dict):
                pass
            elif isinstance(data[0], dict):
                data = data[0]
            elif isinstance(data[0], (tuple, list)):
                pass
        else:
            return

        for key, val in data.items():
            if val is not None:
                obj = getattr(base_widget, key + '_qwidget', None)
                if isinstance(obj, QWidget):
                    obj.setValue(val, set_default=set_default)

    def create(self):
        print('create, please override')

    def update(self):
        print('update, please override')

    def delete(self, id=None):
        print('delete, please override')

    def refresh(self):
        print('refresh, please override')

    # def set_table(self, data, column_source):
    #     headers = [h.strip() for h in getattr(getattr(self.setting, column_source), str(1)).split(',')]
    #     getattr(self, 'firstTableWidget').set_table_widget(data, headers, sort_col='id', order='asc')

    def render_print_template(self, *ares, template_file=None, **kwargs):
        templateLoader = jinja2.FileSystemLoader(searchpath=
                                                 f"source\\apps\\{current_app}\\ui\\templates")
        templateEnv = jinja2.Environment(loader=templateLoader, extensions=['jinja2.ext.loopcontrols'])
        template = templateEnv.get_template(template_file)
        html = template.render(**kwargs)
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
            url = 'file://' + f.name
            f.write(html)
        webbrowser.open(url)

    def api_get(self, endpoint, params):
        res = self.pool.get('ui_connector').api_get(endpoint, params)
        return res

    def api_post(self, endpoint, params):
        res = self.pool.get('ui_connector').api_post(endpoint, params)
        return res

    def api(self, endpoint, model, method, context=None):
        data = {
            'model': None,
            'method': None,
            'context': None,
        }
        def set_model(model):
            data['model'] = model

        def set_method(method):
            data['method'] = method

        def set_context(context={}):
            context.update({'uid': self.pool.get('current_user')['id']})
            data['context'] = json.dumps(context)


        if endpoint == 'exec':
            set_model(model)
            set_method(method)
            set_context(context)

        if method in ('create', 'update', 'copy_cred_file',):
            res = self.api_post(endpoint, params=data)
        else:
            res = self.api_get(endpoint, params=data)
        return res['data']

    def get_current_parent(self, model: str) -> int:
        ui_connector = self.pool.get('ui_connector')
        for i in range(len(ui_connector.open_models), 0, -1):
            item = ui_connector.open_models[i - 1]
            if list(item.keys())[0] == model:
                return item.get(model).active_id
        return None

    def set_current_parent(self, model: str, id: int) -> None:
        ui_connector = self.pool.get('ui_connector')
        for i in range(len(ui_connector.open_models), 0, -1):
            item = ui_connector.open_models[i - 1]
            if list(item.keys())[0] == model:
                item[model].active_id = id
                return None


    def translate(self, phrase, model_id=None):
        return _tr(phrase, model=self._model, model_id=model_id, cache=False)

