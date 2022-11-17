from source.framework.base_model import Model
from source.framework.fields import Fields

class Pallet(Model):
    def __init__(self) -> None:
        super().__init__()
    
    _name = 'pallet'
    _table = 'pallet'
    _id_column = 'id'
    _init = True
    _get_name_string = '{code}'
    _fields = {
        'id':               Fields.integer('id'),
        'code':             Fields.char('Pallet number', length=100, required=True),
    }
    
    _sql_constraints = [
        ('unique_pallet_code', 'unique', ['code']),
    ]
   