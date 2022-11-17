import inspect
import json
from sys import modules

from source.framework import Base
from source.framework.fields import Many2One, Datetime
from source.framework.access import AccessManager
from source.framework.utilities import return_exception
from .config import apps
from .pool import ModelPool
from source.framework.utilities import tr


class Api(Base):
    def __init__(self) -> None:
        super().__init__()
        self.access_manager = AccessManager()
        self._model_pool = ModelPool()
        self._register_models()
        self._model_relations()

    def authenticate(self, params={}):
        model_obj = self._model_pool.get('user')()
        res = {
            'logged_in': False,
            'active': False,
        }
        data = model_obj.is_valid(params)
        if not data[0]:
            return res
        if not isinstance(res, Exception):
            delattr(data[1], 'password')
            res['logged_in'] = data[1].to_dict()
            if data[1].is_active:
                res['active'] = True
        return res

    def get_init_setting(self, params={}):
        res = {
            'data': False,
            'easys_error': None,
        }
        model = params.get('model')
        if model not in ('user_setting', 'app_setting'):
            res['easys_error'] = "Invalid setting model"
            return res
        model_obj = self._model_pool.get(model)()
        res['data'] = model_obj.get_setting()
        return res

    def get_relations(self, *args, **kwargs):
        return self._relations if hasattr(self, '_relations') else {}

    def get_model_fields(self, params={}):
        model_name = params.get('model')
        res = {
            'fields': False,
            'easys_error': None,
        }
        if not self.access_manager.has_access(params.get('uid'), model=model_name, action='read'):
            res['easys_error'] = 'Access denied.'
        else:
            model_obj = self._get_model(model_name)
            res['fields'] = model_obj.get_fields()
        return res

    def get_model_parameter(self, params={}):
        model_name = params.get('model')
        parameter = params.get('param')
        if not self.access_manager.has_access(params.get('uid'), model=model_name, action='read'):
            raise Exception('Access denied.')
        model_obj = self._get_model(model_name)
        return {parameter: getattr(model_obj, parameter)}

    def get_model_field(self, params={}):
        field_name = params.get('field_name')
        res = self.get_model_fields(params=params)
        if not res['easys_error']:
            res['field'] = res['fields'].get(field_name)
            res.pop('fields')
        return res

    def internal_exec(self, model_name, method_name, context=None):
        model_obj = self._get_model(model_name)
        method = getattr(model_obj, method_name, None)
        if not method:
            print('No method')
        data = method(context)
        return data

    def exec(self, params={}):
        model_name = params.get('model')
        method_name = params.get('method')
        res = {
            'data': False,
            'easys_error': None,
        }
        if not self.access_manager.has_access(params.get('uid'), model=model_name, action=method_name):
            res['easys_error'] = 'Access denied.'
        else:
            model_obj = self._get_model(model_name)
            method = getattr(model_obj, method_name, None)
            context = json.loads(params['context'])
            if not method:
                print('No method')
                res['easys_error'] = f'Unrecognized api method {method}'
            data = method(context)
            if isinstance(data, Exception):
                res['easys_error'] = str(data)
            else:
                res['data'] = data
        return res

    def get_ui_model_access(self, params={}):
        action_mapped = {
            1: 'create',
            2: 'update',
            3: 'list',
            4: 'form',
        }
        ui_model = params.get('ui_model')
        mode = int(params.get('mode'))
        uid = int(params.get('uid'))
        res = {
            'has_access': False,
            'easys_error': None,
        }
        if not self.access_manager.has_access(uid, model=ui_model,
                                              action=action_mapped.get(mode)):
            res['easys_error'] = 'Access denied.'
        else:
            res['has_access'] = True
        return res

    @return_exception
    def api_gate(self, api_method, *args, **kwargs):
        return getattr(self, api_method)(*args, **kwargs)

    @staticmethod
    def _get_app_active_models(app):
        return inspect.getmembers(
            modules[f'source.apps.{app}.model'], inspect.isclass)

    @staticmethod
    def _get_framework_active_models():
        return inspect.getmembers(
            modules[f'source.framework.framework_models.model'], inspect.isclass)

    def _register_models(self):
        self._active_models = list()
        self._active_ui_models = list()
        for app in apps:
            self._active_models.extend(Api._get_app_active_models(app))
        self._active_models.extend(Api._get_framework_active_models())
        for model in self._active_models:
            self._model_pool.set(model[1]._name, model[1])
        for model in self._active_ui_models:
            self.__ui_model_pool.set(model[0], model[1])

    @staticmethod
    def _update_log_columns(model):
        log_fields = {
            'create_user': Many2One('Creator user', relation='user'),
            'create_date': Datetime('Create date'),
            'update_user': Many2One('Last updator user', relation='user'),
            'update_date': Datetime('Last update date'),
        }
        model._fields.update(log_fields)

    def _model_relations(self):  # used for prohibiting Deletion related records
        relations = dict()
        for base_model in self._active_models:
            base_name = base_model[1]._name
            relations[base_name] = list()
            for other_model in self._active_models:
                if other_model[1]._table:
                    for name, obj in other_model[1]._fields.items():
                        if isinstance(obj, Many2One) \
                                and obj.relation == base_name:
                            relations[base_name].append((other_model[1]._name, name))
        self._relations = relations

    def _get_model(self, model_name):
        model_class = self._model_pool.get(model_name)
        if not model_class:
            print('No class')
            return None
        model_obj = model_class()
        if model_obj._log:
            Api._update_log_columns(model_obj)
        return model_obj if model_obj else None

    def get_visible_fields(self, params={}):
        res = {
            'fields': False,
        }
        view_mode = params.get('view_mode')
        model = params.get('model')
        res['fields'] = getattr(getattr(self.pool.get('setting'), model), view_mode)
        return res

    def translate(self, params={}):
        phrase = params.get('phrase')
        if params.get('model_id'):
            translation = self.internal_exec(params.get('model'), 'translate', params)
        else:
            translation = self.internal_exec('translation', 'translate', {'phrase': phrase})

        return {'phrase': phrase, 'translation': translation}