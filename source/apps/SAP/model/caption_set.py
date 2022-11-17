import math

from source.framework.base_model import Model
from source.framework.fields import Fields


class CaptionSet(Model):
    def __init__(self) -> None:
        super().__init__()

    _name = 'caption_set'
    _table = 'caption_set'
    _id_column = 'id'
    _init = True
    _get_name_string = '{name}'
    _fields = {
        'id': Fields.integer('id'),
        'name': Fields.char('Caption set name', length=100),
        'sn1_tr': Fields.char('Serial number 1 caption', length=100),
        'sn2_tr': Fields.char('Serial number 2 caption', length=100),
        'sn3_tr': Fields.char('Serial number 3 caption', length=100),
        'sn4_tr': Fields.char('Serial number 4 caption', length=100),
        'sn5_tr': Fields.char('Serial number 5 caption', length=100),
        'sn6_tr': Fields.char('Serial number 6 caption', length=100),
        'sn7_tr': Fields.char('Serial number 7 caption', length=100),
        'sn8_tr': Fields.char('Serial number 8 caption', length=100),
        'check1_tr': Fields.char('Final check 1 caption', length=100),
        'check2_tr': Fields.char('Final check 2 caption', length=100),
        'check3_tr': Fields.char('Final check 3 caption', length=100),
        'check4_tr': Fields.char('Final check 4 caption', length=100),
        'check5_tr': Fields.char('Final check 5 caption', length=100),
        'check6_tr': Fields.char('Final check 6 caption', length=100),
        'check7_tr': Fields.char('Final check 7 caption', length=100),
        'check8_tr': Fields.char('Final check 8 caption', length=100),
    }


    _sql_constraints = [
        ('unique_caption_set_name', 'unique', ['name']),
    ]

