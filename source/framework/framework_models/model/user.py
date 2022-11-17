from source.framework.utilities import log
from source.framework.base_model import Model
from source.framework.fields import Fields
from hashlib import sha256, md5


class User(Model):
    def __init__(self) -> None:
        super().__init__()

    _name = 'user'
    _table = 'user'
    _id_column = 'id'
    _init = True
    _get_name_string = '{fullname} ({username})'
    _fields = {
        'id': Fields.integer('id'),
        'fullname': Fields.char('Name', length=100, required=True),
        'username': Fields.char('Username', length=50, required=True),
        'password': Fields.char('Password', length=100, required=False),
        'access_level': Fields.integer('Access level'),
        'is_active': Fields.boolean('Active status', required=True, default=True),
        'access': Fields.many2many('Access', relation='user_access_relation',
                                   source_field='user', target_field='access')
    }

    _sql_constraints = [
        ('unique_user_name', 'unique', ['username']),
    ]

    def is_valid(self, data):
        try:
            pass_enc = self.encrypt_password(data.get('password') or str())
            condition = ['and', ('username', 'like', data.get('username') or str()), ('password', 'like', pass_enc)]
            user_obj = self.search(context={'condition': condition, 'return_dict': False, 'return_object': True})
            user_obj = user_obj[0] if user_obj else user_obj

            if user_obj:
                current_user = self.read(context={'ids': [getattr(user_obj, self._id_column)], \
                                                  'as_relational': True})[0]
            return (current_user, user_obj) if user_obj else (None, False)
        except Exception as e:
            log(e)
            return (None, e)

    def encrypt_password(self, password):
        sha1_pass = sha256(password.encode()).hexdigest()
        md5_pass = md5(sha1_pass.encode()).hexdigest()
        return md5_pass

    def create(self, context=None):
        context['field_values']['password'] = self.encrypt_password(context['field_values']['password'])
        current_user_level = self.pool.get('api').internal_exec('user', 'search',
                                    {'fields': ['access_level'], 'condition': [('id', '=', context.get('uid'))]})
        context['field_values'].update({'access_level': current_user_level[0].get('access_level') + 1})
        return super().create(context=context)

    def read(self, context=None):
        res = super().read(context=context)
        if isinstance(res, dict) and res.get('password'):
            res.pop("password")
        if isinstance(res, list):
            for rec in res:
                if isinstance(rec, dict) and rec.get('password'):
                    rec.pop("password")
        return res

    def update(self, context=None):
        if context['field_values']['password']:
            context['field_values']['password'] = self.encrypt_password(context['field_values']['password'])
        else:
            context['field_values'].pop("password")
        return super().update(context=context)
