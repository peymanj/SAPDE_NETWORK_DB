from datetime import datetime

from source.framework.base import Base
from source.framework.framework_models.model.access import Access
from source.framework.framework_models.model.user_access_relation import UserAccessRelation


class AccessManager(Base):
    def __init__(self) -> None:
        super().__init__()
        self.access_model = Access()
        self.access_rel_model = UserAccessRelation()
        self.cache = AccessCache()

    def has_access(self, current_user, model=None, action=None):

        model = model if isinstance(model, str) else model._name
        
        if not model: return False
        if not action: return False
        
        model_access = self._access_exists(model, action)
        if not model_access: return False
        
        if model_access.relation:
            return self.has_access(current_user, model=model, action=model_access.relation) 

        user_access = self._user_has_access(current_user, model_access)
        if not user_access: return False
        return True

    def _access_exists(self, model, action):

        cached_access = self.cache.get_access(model, action)
        if cached_access: return cached_access

        context = {
            'condition': ['and', ('model', '=', model), ('action', '=', action)],
            'return_object': True,
            'return_dict': False,
        }
        acc = self.access_model.search(context=context)
        return self.cache.set_access(model, action,
                                     acc[0] if acc else False)

    def _user_has_access(self, current_user, access):

        cached_access_rel = self.cache.get_access_rel(current_user, access.id)
        if cached_access_rel: return cached_access_rel

        context = {
            'condition': ['and', ('user', '=', current_user), ('access', '=', access.id)],
            'return_object': False,
            'return_dict': False,
        }
        return self.access_rel_model.search(context=context)


class AccessCache:
    def __init__(self) -> None:
        self.access_struct = dict()
        self.access_rel_struct = dict()

    def set_access(self, model, action, obj):
        if not self.access_struct.get(model): self.access_struct[model] = dict()
        self.access_struct[model][action] = (obj, datetime.now())
        return obj

    def get_access(self, model, action):
        model_dict = self.access_struct.get(model)
        if model_dict:
            return self.expire_check(model_dict.get(action))
        else:
            return None

    def set_access_rel(self, user, access, obj):
        if not self.access_rel_struct.get(user): self.access_rel_struct[user] = dict()
        self.access_rel_struct[user][access] = (obj, datetime.now())
        return obj

    def get_access_rel(self, user, access):
        user_dict = self.access_rel_struct.get(user)
        if user_dict:
            return self.expire_check(user_dict.get(access))
        else:
            return None

    def expire_check(self, obj_time_tuple):
        if not obj_time_tuple: return False
        if (datetime.now() - obj_time_tuple[1]).seconds > 300:  # 5 min cache
            return False
        else:
            # print('using_cash')
            return obj_time_tuple[0]
