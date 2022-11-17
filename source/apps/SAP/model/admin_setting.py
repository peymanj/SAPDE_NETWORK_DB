from source.framework.base_model import Model
from source.framework.fields import Fields


class AdminSetting(Model):
    def __init__(self) -> None:
        super().__init__()

    _name = 'admin_setting'
    _table = 'admin_setting'
    _id_column = 'id'
    _init = True
    _get_name_string = '{id}'

    _fields = {
        'id': Fields.integer('id'),
        'master_password': Fields.char('Master password', length=100, required=True),
    }

    def create(self, context=None):
        if self.read():
            return None
        return super().create(context=context)

    def delete(self, context=None):
        return None

    def get_setting(self):
        context = {'return_object': False, 'post_proc': False}
        setting = self.read(context=context)
        return setting[0] if setting else setting

    def master_pass_check(self, context=None):
        password = context.get('password')
        setting = self.get_setting()
        return True if setting and password == setting['master_password'] else False
