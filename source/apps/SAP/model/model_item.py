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
        
        'min_weight_1': Fields.integer('Min part 1 weight'),
        'min_weight_2': Fields.integer('Min part 2 weight'),
        'min_weight_3': Fields.integer('Min part 3 weight'),
        'min_weight_4': Fields.integer('Min part 4 weight'),
        'max_weight_1': Fields.integer('Max part 1 weight'),
        'max_weight_2': Fields.integer('Max part 2 weight'),
        'max_weight_3': Fields.integer('Max part 3 weight'),
        'max_weight_4': Fields.integer('Max part 4 weight'),

        'min_width_1': Fields.integer('Min part 1 width'),
        'min_width_2': Fields.integer('Min part 2 width'),
        'min_width_3': Fields.integer('Min part 3 width'),
        'min_width_4': Fields.integer('Min part 4 width'),
        'max_width_1': Fields.integer('Max part 1 width'),
        'max_width_2': Fields.integer('Max part 2 width'),
        'max_width_3': Fields.integer('Max part 3 width'),
        'max_width_4': Fields.integer('Max part 4 width'),

        'min_length_1': Fields.integer('Min part 1 length'),
        'min_length_2': Fields.integer('Min part 2 length'),
        'min_length_3': Fields.integer('Min part 3 length'),
        'min_length_4': Fields.integer('Min part 4 length'),
        'max_length_1': Fields.integer('Max part 1 length'),
        'max_length_2': Fields.integer('Max part 2 length'),
        'max_length_3': Fields.integer('Max part 3 length'),
        'max_length_4': Fields.integer('Max part 4 length'),

        'min_thickness_1': Fields.integer('Min part 1 thickness'),
        'min_thickness_2': Fields.integer('Min part 2 thickness'),
        'min_thickness_3': Fields.integer('Min part 3 thickness'),
        'min_thickness_4': Fields.integer('Min part 4 thickness'),
        'max_thickness_1': Fields.integer('Max part 1 thickness'),
        'max_thickness_2': Fields.integer('Max part 2 thickness'),
        'max_thickness_3': Fields.integer('Max part 3 thickness'),
        'max_thickness_4': Fields.integer('Max part 4 thickness'),
        
        'n_parts': Fields.integer('Part Count'),

        'weight_disp_1': Fields.char('Part 1 weight', length=200, required=False),
        'weight_disp_2': Fields.char('Part 2 weight', length=200, required=False),
        'weight_disp_3': Fields.char('Part 3 weight', length=200, required=False),
        'weight_disp_4': Fields.char('Part 4 weight', length=200, required=False),

        'width_disp_1': Fields.char('Part 1 width', length=200, required=False),
        'width_disp_2': Fields.char('Part 2 width', length=200, required=False),
        'width_disp_3': Fields.char('Part 3 width', length=200, required=False),
        'width_disp_4': Fields.char('Part 4 width', length=200, required=False),

        'length_disp_1': Fields.char('Part 1 length', length=200, required=False),
        'length_disp_2': Fields.char('Part 2 length', length=200, required=False),
        'length_disp_3': Fields.char('Part 3 length', length=200, required=False),
        'length_disp_4': Fields.char('Part 4 length', length=200, required=False),

        'thickness_disp_1': Fields.char('Part 1 thickness', length=200, required=False),
        'thickness_disp_2': Fields.char('Part 2 thickness', length=200, required=False),
        'thickness_disp_3': Fields.char('Part 3 thickness', length=200, required=False),
        'thickness_disp_4': Fields.char('Part 4 thickness', length=200, required=False),

        'no_serials_1': Fields.integer('Part 1 serial count', required=False, default=2),
        'no_serials_2': Fields.integer('Part 2 serial count', required=False, default=2),
        'no_serials_3': Fields.integer('Part 3 serial count', required=False, default=2),
        'no_serials_4': Fields.integer('Part 4 serial count', required=False, default=2),

        }

    @staticmethod
    def get_min_max(string):
        delimiter = ':'
        str_list = string.split(delimiter)
        if len(str_list) != 2:
            raise Exception("Invalid range format.\nExample: 100:200")
        min_val = str_list[0].strip()
        max_val = str_list[1].strip()
        try:
            min_val = int(min_val)
            max_val = int(max_val)
        except:
            raise Exception('Invalid range value.\nExample: 100:200')
        if max_val < min_val:
            raise Exception("Invalid range.\n Max value cannot be lower that min value")
        return min_val, max_val

    def get_data_from_string(self, vals):
        n_parts = vals.get('n_parts')
        var_fields = ['weight', 'width', 'length', 'thickness']
        for i in range(1, 5):
            for f in var_fields:
                if i <= n_parts:
                    disp_name = f + '_disp_' + str(i)
                    if vals.get(disp_name):
                        vals['min_' + f + '_' + str(i)], vals['max_' + f + '_' + str(i)] = \
                            self.get_min_max(vals.get(disp_name))
        return vals

    def create(self, context=None):
        context['field_values'] = self.get_data_from_string(context.get('field_values'))
        super().create(context=context)

    def update(self, context=None):
        context['field_values'] = self.get_data_from_string(context.get('field_values'))
        super().update(context=context)

    _sql_constraints = [
        ('unique_model_item_model_size', 'unique', ['model', 'size']),
    ]
   
   
