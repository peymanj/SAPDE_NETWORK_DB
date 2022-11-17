from source.framework.base_model import Model
from source.framework.fields import Fields

class ModelItem(Model):
    def __init__(self) -> None:
        super().__init__()
    
    _name = 'model_item'
    _table = 'model_item'
    _id_column = 'id'
    _init = True
    _get_name_string = '{model} ({size})'
    _fields = {
        'id':               Fields.integer('id'),
        'model':            Fields.many2one('Model', relation='model', required=True),
        'size':             Fields.many2one('Size', relation='size', required=True),
        'min_weight_front': Fields.integer('Min front part weight'),
        'max_weight_front': Fields.integer('Max front part weight'),
        'min_weight_back':  Fields.integer('Min back part weight'),
        'max_weight_back':  Fields.integer('Max back part weight'),
        'no_front_serials': Fields.integer('Front part serial count', required=False, default=2),
        'no_back_serials':  Fields.integer('Back part serial count', required=False, default=2),
        }
    
    _sql_constraints = [
        ('unique_model_item_model_size', 'unique', ['model', 'size']),
    ]
   
   
