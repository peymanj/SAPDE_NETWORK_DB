from source.framework.base_model import Model
from source.framework.fields import Fields

class Model(Model):
    def __init__(self) -> None:
        super().__init__()
    
    _name = 'model'
    _table = 'model'
    _id_column = 'id'
    _init = True
    _get_name_string = '{name}'
    _fields = {
        'id':       Fields.integer('id'),
        'name':     Fields.char('Model', length=120, required=True),
        }
    
    _sql_constraints = [
        ('unique_model_name', 'unique', ['name']),
    ]
   
   
