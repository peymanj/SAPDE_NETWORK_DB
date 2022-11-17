from source.framework.base import Base
import inspect
from .config import current_app
from sys import modules
from importlib.machinery import SourceFileLoader

import source.framework.framework_models.model as base_models
from source.framework.framework_models.security.access import model_access_dict, view_access_dict

MODEL_ACCESS = 1
UI_ACCESS = 2


class FrameworkUpgrade(Base):
    def __init__(self) -> None:
        super().__init__()
        self.orm = self.pool.get('orm')

    def start(self):
        self.upgrade_models()

    def set_access(self):
        self.create_super_user()
        self.update_access_table()
        self.set_super_user_access()

    def get_models(self):
        models = list()
        Models = inspect.getmembers(base_models, inspect.isclass)
        for name, obj in Models:
            if inspect.isclass(obj) and hasattr(obj, '_init'):
                if obj._init:
                    models.append(obj)
        return models

    def upgrade_models(self):
        for model in self.get_models():
            if model._table:
                self.orm.model_to_db(model)
            self.run_init_method(model)

    def update_access_table(self):

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
                        ]
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
                        }
                    }
                    if relation:
                        context['field_values'].update({'relation': relation})
                    access_obj.create(context=context)

        access_model_obj = base_models.Access()
        insert_access(access_model_obj, model_access_dict, MODEL_ACCESS)
        insert_access(access_model_obj, view_access_dict, UI_ACCESS)

    def create_super_user(self):
        query = """     
            IF NOT EXISTS (SELECT * FROM [user] WHERE username='superuser')
                INSERT INTO [user] (username, fullname, password, access_level) VALUES ('superuser', 'Super User', 'bf077a62b2dffd8add96a92aa5c5efe9', 0);
            IF NOT EXISTS (SELECT * FROM [user] WHERE username='admin')
                INSERT INTO [user] (username, fullname, password, access_level) VALUES ('admin', 'System Administrator', 'ddf55f1bf1e2edf05232e268211f9bcd', 1);
        """
        # SuperPeym@n
        #1

        self.orm.exec(query)

    def set_super_user_access(self):
        user_model = base_models.User()
        for username in ('superuser', 'admin',):
            super_user = user_model.search({'condition': [('username', 'like', username)], 'return_object': True})[0]
            access_model = base_models.Access()
            accesses = access_model.read({'return_dict': False})
            access_rel_model = base_models.UserAccessRelation()
            for ac in accesses:
                context = {
                    'condition': ['and', ('user', '=', super_user.id), ('access', '=', ac.get('id'))],
                    'return_object': False,
                    'return_dict': False,
                    'post_proc': False,
                }
                if not access_rel_model.search(context=context):
                    context = {
                        'field_values': {
                            'user': super_user.id,
                            'access': ac.get('id'),
                        },
                        'exec_on_record_change': False,
                    }
                    access_rel_model.create(context=context)

    def run_init_method(self, model):
        model().init()
