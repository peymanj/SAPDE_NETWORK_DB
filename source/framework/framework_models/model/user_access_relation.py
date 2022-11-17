from source.framework.utilities import log
from source.framework.base_model import Model
from source.framework.fields import Fields

class UserAccessRelation(Model):
    def __init__(self) -> None:
        super().__init__()
    
    _name = 'user_access_relation'
    _table = 'user_access_relation'
    _id_column = 'id'
    _init = True
    _get_name_string = '{user}: {access}'
    _fields = {
        'id':           Fields.integer('id'),
        'user':         Fields.many2one('User', relation='user', required=True),
        'access':       Fields.many2one('Access', relation='access', required=True),
    }
    
    _sql_constraints = [
        ('unique_access_rel_user_access', 'unique', ['user', 'access']),
    ]
