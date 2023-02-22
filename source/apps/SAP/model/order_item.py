import math

from source.framework.base_model import Model
from source.framework.fields import Fields


class OrderItem(Model):
    def __init__(self) -> None:
        super().__init__()

    def _get_status(self, ids):
        res = dict.fromkeys(ids, str())
        for id in ids:
            order_item = self.read({'ids': [id], 'fields': ['quantity', 'no_per_box'], 'return_object': True})[0]
            n_boxes_required = math.ceil(order_item.quantity / order_item.no_per_box)
            boxes = self.pool.get('api')._model_pool.get('box')().search(
                                              {'condition': [('order_item', '=', id)], 'fields': ['status']})
            n_boxes_now_tot = len(boxes)
            n_boxes_now_ok = 0
            for rec in boxes:
                if rec.get('status'):
                    n_boxes_now_ok += 1
            res.update({id: f'({n_boxes_now_tot} of {n_boxes_required}) required boxes created. \n'
                            f'{n_boxes_now_ok} boxes OK.'})
        return res

    def update_status(self, ids):
        for id in ids:
            order_item = self.read({'ids': [id], 'fields': ['quantity', 'no_per_box'], 'return_object': True})[0]
            n_boxes_required = math.ceil(order_item.quantity / order_item.no_per_box)
            boxes = self.pool.get('api').internal_exec('box', 'search',
                                              {'condition': [('order_item', '=', id)], 'fields': ['status']})
            n_boxes_now_ok = 0
            for rec in boxes:
                if rec.get('status'):
                    n_boxes_now_ok += 1
            if n_boxes_now_ok == n_boxes_required:
                status = True
            else:
                status = False
            self.update({'id': id, 'field_values': {'status': status}})

    _name = 'order_item'
    _table = 'order_item'
    _id_column = 'id'
    _init = True
    _get_name_string = '{model} - {size} ({quantity})'
    _fields = {
        'id': Fields.integer('id'),
        'order_id': Fields.many2one('Order id', relation='order', required=True),
        'model': Fields.many2one('Model', relation='model', required=True),
        'size': Fields.many2one('Size', relation='size', required=True),
        'quantity': Fields.integer('Quantity', required=True),
        'pallet_no': Fields.many2one('Pallet number', relation='pallet'),
        'no_per_box': Fields.integer('Packs per box', required=True),
        'image_required': Fields.boolean('Image required', required=True, default=True),
        'check_weight': Fields.boolean('Weight check required', required=True, default=True),
        'check_length': Fields.boolean('Length check required', required=True, default=True),
        'check_width': Fields.boolean('Width check required', required=True, default=True),
        'check_thickness': Fields.boolean('Thickness check required', required=True, default=True),
        'unique_serial': Fields.boolean('Check serial uniqueness ', required=False, default=True),
        'no_fchecks': Fields.integer('Final check count', required=True),
        'boxes': Fields.one2many('Boxes', relation='box', field='order_item'),
        'status': Fields.boolean('Status', defaul=False),
        'status_disp': Fields.function('Status', func=_get_status, type='char'),
    }


    _sql_constraints = [
        ('unique_orderitem_model_size', 'unique', ['order_id', 'model', 'size']),
    ]

    def get_items(self, order_id):
        return self.search(context={'condition': [('order_id', '=', order_id)], 'return_dict': False})

    def _onchange_model(self, params={}):
        model_id = params.get('args')[0]
        size = list()
        context = {
            'condition': [('model', '=', model_id)],
            'return_dict': False,
            'return_object': False,
            'fields': ['size'],
            'post_proc': False,
        }
        data = self.pool.get('api').internal_exec('model_item', 'search', context=context)
        if data:
            size_ids = list(map(lambda item: item.get('size'), data))
            context = {
                'return_dict': False,
                'return_object': False,
                'ids': size_ids,
                'as_relational': True
            }
            size = self.pool.get('api').internal_exec('size', 'read', context=context)
        return {
            'value': {
                'size': size
            }
        }

    def on_record_change(self, obj):
        if obj:
            self.pool.get('api').internal_exec('order', 'update_status', [obj[0].order_id[0]])
