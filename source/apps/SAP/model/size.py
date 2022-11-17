from source.framework.base_model import Model
from source.framework.fields import Fields

class Size(Model):
    def __init__(self) -> None:
        super().__init__()
    
    _name = 'size'
    _table = 'size'
    _id_column = 'id'
    _init = True
    _get_name_string = '{name}'
    _fields = {
        'id':      Fields.integer('id'),
        'name':    Fields.char('Size', length=10, required=True),
        }
            
    _sql_constraints = [
        ('unique_size_name', 'unique', ['name']),
    ]
   
   
