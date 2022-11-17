from source.framework.base import Base
import inspect
from .config import apps
from importlib import import_module
from source.framework.framework_models.model.access import Access
from .framework_upgrade import UI_ACCESS, MODEL_ACCESS

class AppUpgrade(Base):
    def __init__(self) -> None:
        super().__init__()
        self.orm = self.pool.get('orm')

    def start(self):
        self.upgrade_models()

    def set_access(self):
        for app in apps:
            self.update_access_table(app)

    def get_models(self, app):
        models = list()
        module = import_module(f'source.apps.{app}.model')
        Models = inspect.getmembers(module, inspect.isclass)
        for name, obj in Models:
            if inspect.isclass(obj) and hasattr(obj, '_init'):
                if obj._init:
                    models.append(obj)                    
        return models

    def upgrade_models(self):
        for app in apps:
            for model in self.get_models(app):
                if model._table:
                    self.orm.model_to_db(model)
                self.run_init_method(model)

    def update_access_table(self, app):
    
        def insert_access(access_obj, access_file, access_type):
            for model, access_dict in access_file.items():
                for action, val in access_dict.items():
                    if isinstance(val, dict):
                        name = val.get('name')
                        relation = val.get('relation')
                    else: 
                        name = val
                        relation = None
                        
                    if not name:
                        return

                    context = {
                        'condition': [
                            'and',
                            ('model', '=', model),
                            ('action', '=', action),
                        ],
                        'post_proc': False,
                    }
                    ac = access_obj.search(context=context)
                    if ac:
                        continue

                    context = {
                        'field_values': {
                            'model': model,
                            'action': action,
                            'name': name,
                            'access_type': access_type,
                        },
                        'exec_on_record_change': False,
                    }
                    if relation:
                        context['field_values'].update({'relation': relation})
                    access_obj.create(context=context)
        
        access_model_obj = Access()
        module = import_module(f'source.apps.{app}.security.access')
        
        model_access_file = getattr(module, 'model_access_dict')
        insert_access(access_model_obj, model_access_file, MODEL_ACCESS)

        model_access_file = getattr(module, 'view_access_dict')
        insert_access(access_model_obj, model_access_file, UI_ACCESS)

    def set_super_user_access(self, app):
        module = import_module(f'source.apps.{app}.model')
        Models = inspect.getmembers(module, inspect.isclass)
        user_model = Models.User()
        for username in ('superuser', 'admin',):
            super_user = user_model.search({'condition': [('username', 'like', username)], 'return_object': True})[0]
            access_model = Models.Access()
            accesses = access_model.read({'return_dict': False})
            access_rel_model = Models.UserAccessRelation()
            for ac in accesses:
                context = {
                    'condition': ['and', ('user', '=', super_user.id), ('access', '=', ac.get('id'))],
                    'return_object': False,
                    'return_dict': False,
                }
                if not access_rel_model.search(context=context):
                    context = {
                        'field_values':{
                            'user': super_user.id,
                            'access': ac.get('id'),
                        }
                    }
                    access_rel_model.create(context=context)

    def run_init_method(self, model):
        model().init()
