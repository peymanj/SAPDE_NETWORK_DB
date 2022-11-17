from source.framework.base_model import Model
from source.framework.fields import Fields


class Box(Model):
    def __init__(self) -> None:
        super().__init__()

    _name = 'box'
    _table = 'box'
    _id_column = 'id'
    _init = True
    _get_name_string = '{code}'

    def _get_code(self, context=None):
        if context and context.get('order_item_id'):
            data = self.search({'condition': [('order_item', '=', context.get('order_item_id'))],
                                'fields': ['code']})
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
            order_item_id = self.read({
                'ids': [id],
                'fields': ['order_item'],
                'return_object': True,
                'post_proc': False,
            })[0].order_item
            order_item_obj = self.pool.get('api').internal_exec('order_item', 'read', {
                'ids': [order_item_id],
                'fields': ['quantity', 'no_per_box'],
                'return_object': True,
            })[0]
            n_per_box_req = order_item_obj.no_per_box
            n_items_max = order_item_obj.quantity
            n_boxes_before_this = len(self.search({
                'condition': [
                    'and',
                    ('order_item', '=', order_item_id),
                    ('id', '<', id),
                ]
            }))
            n_per_this_box = min(n_per_box_req, n_items_max - (n_boxes_before_this * n_per_box_req))
            n_per_box_req = self.related_read(context={'id': id, 'field': 'no_per_box'})
            item_sets = self.pool.get('api').internal_exec('item_set', 'search',
                                                  {'condition': [('box', '=', id)], 'fields': ['status']})
            n_items_now_ok = 0
            for rec in item_sets:
                if rec.get('status'):
                    n_items_now_ok += 1
            if n_items_now_ok == n_per_this_box:
                status = True
            else:
                status = False
            self.update({
                'id': id,
                'field_values': {'status': status}
            })

            n_items_now_tot = len(item_sets)
            self.update({
                'id': id,
                'field_values': {
                    'status_disp': f'({n_items_now_tot} of {n_per_this_box}) required items created. \n'
                              f'{n_items_now_ok} items OK.'}
            })

    _fields = {
        'id': Fields.integer('id'),
        'code': Fields.char('Box number', length=120, required=True),
        'order_item': Fields.many2one('Order item', relation='order_item', required=True),
        'item_sets': Fields.one2many('Sets', relation='item_set', field='box'),
        'status': Fields.boolean('Status', default=False),
        'status_disp': Fields.char('Status', length=200, required=False)
    }

    _sql_constraints = [
        ('unique_box_code_order_item', 'unique', ['code', 'order_item']),

    ]

    _default_values = {
        'code': _get_code,
    }

    def create(self, context=None):
        id = super().create(context=context)
        current_box = self.read({'ids': [id], 'return_object': True})[0]
        order_item = self.pool.get('api').internal_exec('order_item', 'search',
                                               {
                                                   'condition': [('id', '=', current_box.order_item[0])],
                                                   'fields': ['no_per_box', 'quantity'],
                                                   'return_object': True,
                                               })[0]

        n_per_box_req = order_item.no_per_box
        n_items_max = order_item.quantity
        n_boxes_before_this = len(self.search({
            'condition': [
                'and',
                ('order_item', '=', current_box.order_item[0]),
                ('id', '<', id),
            ]
        }))
        n_per_this_box = min(n_per_box_req, n_items_max - (n_boxes_before_this * n_per_box_req))

        for i in range(n_per_this_box):
            context = {
                'field_values': {
                    'box': id,
                    'code': i + 1,
                },
                'exec_on_record_change': False
            }
            self.pool.get('api').internal_exec('item_set', 'create', context=context)

    def on_record_change(self, obj):
        if obj:
            self.pool.get('api').internal_exec('order_item', 'update_status', [obj[0].order_item[0]])
