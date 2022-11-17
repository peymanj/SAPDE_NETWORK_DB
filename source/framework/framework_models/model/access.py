from source.framework.utilities import log
from source.framework.base_model import Model
from source.framework.fields import Fields

class Access(Model):
    def __init__(self) -> None:
        super().__init__()
    
    _name = 'access'
    _table = 'access'
    _id_column = 'id'
    _init = True
    _get_name_string = '{name}: {name}'
    _fields = {
        'id':       Fields.integer('id'),
        'model':    Fields.char('Model', length=100, required=True),
        'action':   Fields.char('Action', length=50, required=True),
        'name':     Fields.char('Access name', length=100, required=True),
        'relation': Fields.char('Relation', length=100, required=False),
        'access_type': Fields.integer('Access type'),
    }
    
    _sql_constraints = [
        ('unique_access_model_action', 'unique', ['model', 'action']),
    ]
