import os

from source.framework.base_model import Model
from source.framework.fields import Fields
from base64 import urlsafe_b64decode


class Part(Model):
    def __init__(self) -> None:
        super().__init__()

    _name = 'part'
    _table = 'part'
    _id_column = 'id'
    _init = True
    _get_name_string = '{id} - {side}'
    _log = True

    def _side_selection(self, params={}):
        id = params.get('id')
        data = [
            (1, 'Front'),
            (2, 'Back'),
        ]
        return self.search_in_tuple_list(data, id)

    def _current_user(self, context=None):
        return context.get('uid')

    _fields = {
        'id': Fields.integer('id'),
        'item_set': Fields.many2one('Set', relation='item_set', required=True, search=False),
        'side': Fields.selection('Side', func=_side_selection, required=True),  # 1: front  ,    2: back
        'image': Fields.binary('Image'),
        'weight': Fields.integer('Weight'),
        'sn1': Fields.char('Serial number 1', length=100, required=True),
        'sn2': Fields.char('Serial number 2', length=100),
        'sn3': Fields.char('Serial number 3', length=100),
        'sn4': Fields.char('Serial number 4', length=100),
        'sn5': Fields.char('Serial number 5', length=100),
        'sn6': Fields.char('Serial number 6', length=100),
        'sn7': Fields.char('Serial number 7', length=100),
        'sn8': Fields.char('Serial number 8', length=100),
        'check1': Fields.boolean('Final check 1'),
        'check2': Fields.boolean('Final check 2'),
        'check3': Fields.boolean('Final check 3'),
        'check4': Fields.boolean('Final check 4'),
        'check5': Fields.boolean('Final check 5'),
        'check6': Fields.boolean('Final check 6'),
        'check7': Fields.boolean('Final check 7'),
        'check8': Fields.boolean('Final check 8'),
        'check_user': Fields.many2one('Last Checker User', relation='user'),
    }

    _sql_constraints = [
        # ('unique_part_sn', 'unique', ['sn1']),
        ('unique_part_item_set_side', 'unique', ['item_set', 'side'])
    ]

    _default_values = {
        'check_user': _current_user,
    }

    def on_record_change(self, obj):
        if obj:
            self.pool.get('api').internal_exec('item_set', 'update_status', [obj[0].item_set[0]])

    def create(self, context=None):
        self.save_img_to_disk(context)
        return super().create(context=context)

    def update(self, context=None):
        self.save_img_to_disk(context)
        return super().update(context=context)

    def save_img_to_disk(self, context):
        if context and context.get('field_values').get('image'):
            vals = context.get('field_values')
            img_name = 'IMG'
            for i in range(5):
                if vals.get('sn' + str(i+1)):
                    img_name += f'-SN{i+1}-' + vals.get('sn' + str(i+1))
            img_name += '.png'

            order_id = self.pool.get('api').internal_exec('item_set', 'related_read', context={'id': vals.get('item_set'), 'field': 'order_id'})
            order_name = self.pool.get('api').internal_exec('order', 'read', {'ids': [order_id], 'fields': ['code']})[0].get('code')
            img_path = os.path.join(self.pool.get('config').directories.image_folder, order_name)
            os.makedirs(img_path, exist_ok=True)
            img_full_path = os.path.join(img_path, img_name)
            with open(img_full_path, "wb") as f:
                f.write(urlsafe_b64decode(vals.get('image')))

    def translate(self, params={}):
        order = self.pool.get('api').internal_exec(
            'order', 'read', context={'ids': [params.get('model_id')], 'post_proc': False})[0]
        caption_set_id = order.get('caption_set')

        phrase = params.get('phrase').lower()
        translation = str()

        if caption_set_id:
            caption_set = self.pool.get('api').internal_exec(
                'caption_set', 'read', context={'ids': [caption_set_id]})[0]

            if 'serial number' in phrase.lower():
                phrase = phrase.replace('serial', 'sn').replace('number', '').replace(' ', '') + '_tr'
            elif 'check' in phrase.lower():
                phrase = phrase.replace('final', '').replace(' ', '') + '_tr'
            translation = caption_set.get(phrase)
        return translation or super(Part, self).translate(params=params)


