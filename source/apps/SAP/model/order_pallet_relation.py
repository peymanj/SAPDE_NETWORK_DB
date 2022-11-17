from source.framework.base_model import Model
from source.framework.fields import Fields

class OrderPalletRelation(Model):
    def __init__(self) -> None:
        super().__init__()
    
    _name = 'order_pallet_relation'
    _table = 'order_pallet_relation'
    _id_column = 'id'
    _init = True
    _get_name_string = 'Order-Pallet relation: {code}'
    _fields = {
        'id':               Fields.integer('id'),
        'order':            Fields.many2one('Order', relation='order', required=True),
        'pallet':           Fields.many2one('Pallet', relation='pallet' , required=True),
    }
    
    _sql_constraints = [
        ('unique_order_pallet', 'unique', ['order', 'pallet']),
    ]
   