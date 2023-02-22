from source.framework.base_model import Model
from source.framework.fields import Fields


class ItemSet(Model):
    def __init__(self) -> None:
        super().__init__()

    _name = 'item_set'
    _table = 'item_set'
    _id_column = 'id'
    _init = True
    _get_name_string = '{code}'

    def _get_code(self, context=None):

        if context and context.get('box_id'):
            data = self.search({'condition': [('box', '=', context.get('box_id'))],
                                'fields': ['code'], })

            ids = list()
            if data:
                for rec in data:
                    ids.append(rec.get('code'))
            id = self.get_available_code(ids)
            return id
        else:
            return 1

    def update_status(self, ids):
        for id in ids:
            parts = self.pool.get('api').internal_exec('part', 'search',
                                              {'condition': [('item_set', '=', id)], 'id_only': True})
            order_item_id = self.pool.get('api')\
                .internal_exec('item_set', 'related_read',
                    context={'id': id, 'field': 'order_item'})
            order_item = self.pool.get('api').internal_exec(
                'order_item', 'read', context={'ids': [order_item_id], 'post_proc': False})[0]
            model = order_item['model']
            size = order_item['size']
            model_item = self.pool.get('api')\
                .internal_exec('model_item', 'search',
                                  {'condition': ['and', ('model', '=', model), ('size', '=', size)]})
            if len(parts) >= model_item[0]['n_parts']:
                status = True
            else:
                status = False
            self.update({'id': id, 'field_values': {'status': status}})

    _fields = {
        'id': Fields.integer('id'),
        'code': Fields.integer('Set number', required=True),
        'box': Fields.many2one('Box number', relation='box', required=True, search=False),
        'parts': Fields.one2many('Parts', relation='part', field='Item_set'),
        'status': Fields.boolean('Status', default=False),
    }

    _sql_constraints = [
        ('unique_item_set_box_code', 'unique', ['code', 'box']),
    ]

    _default_values = {
        'code': _get_code,
    }

    def on_record_change(self, obj):
        if obj:
            self.pool.get('api').internal_exec('box', 'update_status', [obj[0].box[0]])
