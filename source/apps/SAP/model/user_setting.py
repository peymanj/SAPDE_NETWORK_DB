from PyQt5.QtMultimedia import QCameraInfo
from source.framework.base_model import Model
from source.framework.fields import Fields


class UserSetting(Model):
    def __init__(self) -> None:
        super().__init__()

    _name = 'user_setting'
    _table = 'user_setting'
    _id_column = 'id'
    _init = True
    _get_name_string = '{id}'

    def _theme_selection(self, params={}):
        id = params.get('id')
        data = [
            (1, 'Dark'),
            (2, 'Light'),
        ]
        return self.search_in_tuple_list(data, id)

    _fields = {
        'id': Fields.integer('id'),
        'theme': Fields.selection('Theme', func=_theme_selection, required=True),
        'user': Fields.many2one('User', relation='user', required=True, search=False),
    }

    def create(self, context=None):
        uid = context.get('uid')
        if self.search({'conditions': [('user', '=', uid)]}):
            return None
        context['field_values'].update(user=uid)
        return super().create(context=context)

    def delete(self, context=None):
        return None
        # return super().delete(context=context)

    def get_setting(self):
        context = {'return_object': False, 'post_proc': False}
        setting = self.read(context=context)
        return setting[0] if setting else setting



