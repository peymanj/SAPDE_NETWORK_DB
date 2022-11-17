import copy

from source.framework import Base, fields
from source.framework.utilities import log


class Model(Base):
    _name = str()  # name user to get model from pool or api
    _table = str()  # table name used in db for this model
    _id_column = str()  # Pk of the model
    _init = False  # True to auto load model to db in upgrade
    _fields = dict()
    _sql_constraints = list()  # db level constraint
    _constraints = list()  # python level constraint
    _get_name_string = "{id}"  # string returned bt get_name
    _default_values = dict()  # default values loaded in create view
    _log = False  # save create user and date, update user and date
    _order = False

    def __init__(self) -> None:
        super().__init__()
        self.orm = self.pool.get('orm')
        self.classified_fields = self.field_classify()

    def read(self, context={}):
        default_context = {
            'ids': None,
            'fields': None,
            'return_dict': False,
            'post_proc': True,
            'return_object': False,
            'as_relational': False,
        }

        default_context.update(context)
        if default_context.get('as_relational'):
            default_context.update({'return_object': False})

        db_fields = self.get_fields_for_db()
        if default_context.get('fields'):
            default_context_ = copy.deepcopy(default_context)
            for field in default_context.get('fields'):
                if field not in db_fields: default_context_['fields'].remove(field)
            default_context = default_context_
        else:
            default_context['fields'] = db_fields

        data = self.orm.read(self, context=default_context)

        if not default_context.get('as_relational'):
            if context.get('fields'):
                f_fields = list()
                for f in self.get_function_fields():
                    if f in context.get('fields'):
                        f_fields.append(f)
            else:
                f_fields = self.get_function_fields()
            data = self.load_function_fields(data, f_fields)

        if default_context.get('return_dict'):
            if default_context.get('ids'):
                res = dict.fromkeys(default_context.get('ids'), dict())
            else:
                res = dict()
            for rec in data:
                res.update({rec.get(self._id_column): rec})
            data = res

        if default_context.get('return_object'):
            data = self.set_attr(data)

        return data

    def related_read(self, context=None):
        """ get value of a field available
            in parent models connected through many2one fields
        """
        id = context.get('id')
        target_field = context.get('field', '')
        if not target_field or not id:
            return

        for fname, fobj in self._fields.items():
            if type(fobj) in (fields.Many2One,):
                context = {'ids': [id], 'fields': [fname], 'return_object': True, 'post_proc': False}
                data = self.read(context=context)[0]
                rel_field_val = getattr(data, fname)

                if target_field in self.pool.get('api')._model_pool.get(fobj.relation)._fields:
                    context = {'ids': [rel_field_val], 'fields': [target_field], 'return_object': True,
                               'post_proc': False}
                    data = self.pool.get('api').internal_exec(fobj.relation, 'read', context=context)[0]
                    return getattr(data, target_field)
                else:
                    data = self.pool.get('api').internal_exec(fobj.relation,
                                                              'related_read',
                                                              context={'id': rel_field_val, 'field': target_field})
                    return data
        return None

    def get_name(self, id, *args, **kwargs):
        def get_fields(string):
            _fields = list()
            field = str()
            save = False
            for char in string:
                if char == '{':
                    field = str()
                    save = True
                elif char == '}':
                    save = False
                    _fields.append(field)
                else:
                    field += char if save else str()
            return _fields

        _fields = get_fields(self._get_name_string)
        rec = self.read(context={'ids': [id], 'fields': _fields, 'return_dict': True, 'return_object': False})

        try:
            return self._get_name_string.format(
                **{item: rec[id][item] if not isinstance(rec[id][item], tuple) else rec[id][item][1] \
                   for item in _fields})
        except Exception as e:
            log(e)
            return 'Not Available'

    def search(self, context=None):  # context: ids, fields, header, id_column, return_dict, condition
        default_context = {
            'ids': None,
            'fields': None,
            'id_column': 'id',
            'return_dict': False,
            'post_proc': False,
            'condition': None,
            'return_object': False,
            'id_only': False,
        }
        if context:
            default_context.update(context)
        else:
            context = {}

        if default_context.get('id_only'):
            default_context.update({
                'return_object': False,
                'return_dict': False,
                'post_proc': False,
            })

        db_fields = self.get_fields_for_db()
        if default_context.get('fields'):
            default_context_ = copy.deepcopy(default_context)
            for field in default_context.get('fields'):
                if field not in db_fields: default_context_['fields'].remove(field)
            default_context = default_context_
        else:
            default_context['fields'] = db_fields

        data = self.orm.search(self, context=default_context)
        if not context.get('id_only'):
            if context.get('fields'):
                f_fields = list()
                for f in self.get_function_fields():
                    if f in context.get('fields'):
                        f_fields.append(f)
            else:
                f_fields = self.get_function_fields()
            data = self.load_function_fields(data, f_fields)

        if default_context.get('return_dict'):
            if default_context.get('ids'):
                res = dict.fromkeys(default_context.get('ids'), dict())
            else:
                res = dict()
            for rec in data:
                res.update({rec.get(self._id_column): rec})
            data = res

        if default_context.get('return_object'):
            data = self.set_attr(data)

        return data

    def set_attr(self, data):
        class DataObj:
            def __init__(self, field_val_dict):
                if not isinstance(field_val_dict, dict):
                    return
                for key, val in field_val_dict.items():
                    setattr(self, key, val)

            def to_dict(self):
                return self.__dict__

        if not data:
            return data

        if isinstance(data, list):
            res = list()
            for rec in data:
                if isinstance(rec, dict):
                    res.append(DataObj(rec))
            return res

        if isinstance(data, dict):
            res = dict()
            for id, rec in data.items():
                if isinstance(rec, dict):
                    res.update({id: DataObj(rec)})
            return res
        return None

    def create(self, context=None):
        default_context = {
            'field_values': None,
            'exec_on_record_change': True,
        }
        if context:
            default_context.update(context)
        else:
            context = {}

        # Removing identity id_column to avoid sql error
        try:
            new_fields = context.get('field_values').pop(self._id_column)
            context.update({'field_values', new_fields})
        except:
            pass

        db_fields = self.get_fields_for_db()
        if default_context.get('field_values'):
            default_context_ = copy.deepcopy(default_context)
            for field in default_context.get('field_values').keys():
                if field not in db_fields:
                    default_context_['field_values'].pop(field)
            default_context = default_context_
        else:
            log('No fields to create record in db.')
            return None

        item_id = self.orm.create(self, context=self.add_log_columns(default_context, mode='create'))
        if isinstance(item_id, list):
            item_id = item_id[0][0]
            if default_context.get('exec_on_record_change'):
                obj = self.read({'ids': [item_id], 'return_object': True, 'post_proc': True})
                self.on_record_change(obj)
        return item_id

    def update(self, context=None):
        default_context = {
            'field_values': None,
            'id': None,
            'exec_on_record_change': True,
        }
        if context:
            default_context.update(context)
        else:
            context = {}

        try:
            new_fields = context.get('field_values').pop(self._id_column)
            context.update({'field_values', new_fields})
        except:
            pass

        db_fields = self.get_fields_for_db()
        if default_context.get('field_values'):
            default_context_ = copy.deepcopy(default_context)
            for field in default_context.get('field_values').keys():
                if field not in db_fields:
                    default_context_['field_values'].pop(field)
            default_context = default_context_
        else:
            log('No fields to create record in db.')
            return None

        item_id = self.orm.update(self, context=self.add_log_columns(default_context, mode='update'))
        if isinstance(item_id, list):
            item_id = item_id[0][0]
            if default_context.get('exec_on_record_change'):
                obj = self.read({'ids': [item_id], 'return_object': True})
                self.on_record_change(obj)
        return item_id

    def delete(self, context=None):
        default_context = {
            'condition': None,
            'exec_on_record_change': True,
        }
        if context:
            default_context.update(context)
        else:
            context = {}

        search_context = {'condition': default_context.get('condition'), 'return_object': True, 'post_proc': True}
        obj = self.search(search_context)

        item_id = self.orm.delete(self, context=default_context)
        if isinstance(item_id, list):
            item_id = item_id[0][0]
            if default_context.get('exec_on_record_change'):
                self.on_record_change(obj)
        return item_id

    def add_log_columns(self, context, mode):  # mode = create, update
        if not self._log:
            return context

        import datetime
        if mode == 'create':
            context['field_values'].update(
                {
                    'create_user': context.get('uid'),
                    'create_date': datetime.datetime.now().replace(microsecond=0),
                    'update_user': context.get('uid'),
                    'update_date': datetime.datetime.now().replace(microsecond=0),
                }
            )
        elif mode == 'update':
            context['field_values'].update(
                {
                    'update_user': context.get('uid'),
                    'update_date': datetime.datetime.now().replace(microsecond=0),
                }
            )
        return context

    def get_available_code(self, id_list):
        def is_integer(val):
            try:
                int(val)
                return True
            except:
                return False

        if any(not is_integer(i) for i in id_list):
            return False
        else:
            id_list = [int(i) for i in id_list]

        func = lambda i: int(i)
        id_list.sort(key=func)
        if not id_list:
            return 1
        try:
            for i in range(1, max(id_list) + 1):
                if i not in id_list:
                    return i
            return i + 1
        except:
            return 1

    def search_in_tuple_list(self, tup_list, id, index=0):
        if not id:
            return tup_list
        # ids = [ids] if isinstance(ids, int) else ids
        res = None
        for tup in tup_list:
            if tup[index] == id:
                res = tup[1]
        return res

    def load_stored_function(self, context):
        pass

    def init(self):
        pass

    def drop_function_if_exists(self, fname):
        query = f'''
        IF EXISTS (
            SELECT * FROM sysobjects WHERE id = object_id(N'{fname}') 
            AND xtype IN (N'FN', N'IF', N'TF')
        )
        DROP FUNCTION {fname}
        '''
        try:
            self.orm_exec(query)
        except:
            pass

    def orm_exec(self, query, values=None, header=True):
        res, stat = self.pool.get('orm').exec(query, values=values, header=header)
        return res

    def get_defaults(self, context=None):
        defaults = self._default_values
        if not defaults: return dict()

        defaults_copy = dict(defaults)
        for field, value in defaults.items():
            if callable(value):
                value = getattr(self, value.__name__)
                defaults_copy.update({field: value(context=context)})
        return defaults_copy

    def load_function_fields(self, data, field_names):
        id_column = self._id_column

        # Extract ids:
        ids = list()
        for rec in data:
            if rec:
                ids.append(rec.get(id_column) if isinstance(rec, dict) else rec)
        if not ids or not field_names:
            return data
        functions_data = dict()
        for name in field_names:
            functions_data.update({name: self._fields.get(name).func(self, ids)})
        for i in range(len(data)):
            for f_name, val_dict in functions_data.items():
                data[i].update({f_name: val_dict.get(data[i][id_column])})
        return data

    def get_function_fields(self):
        return list(self.classified_fields['func_stored'].keys()) \
               + list(self.classified_fields['func_not_stored'].keys())

    def field_classify(self):
        fields_classified = dict()
        fields_classified['o2m'] = dict()
        fields_classified['m2o'] = dict()
        fields_classified['m2m'] = dict()
        fields_classified['func_stored'] = dict()
        fields_classified['func_not_stored'] = dict()
        fields_classified['non_relational_fields'] = dict()

        for key, val in self._fields.items():
            if type(self._fields[key]) == fields.Many2One:
                fields_classified['m2o'][key] = self._fields[key]
            elif type(self._fields[key]) == fields.One2Many:
                fields_classified['o2m'][key] = self._fields[key]
            elif type(self._fields[key]) == fields.Many2Many:
                fields_classified['m2m'][key] = self._fields[key]
            elif type(self._fields[key]) == fields.Function:
                if self._fields[key].store:
                    fields_classified['func_stored'][key] = self._fields[key]
                else:
                    fields_classified['func_not_stored'][key] = self._fields[key]
            else:
                fields_classified['non_relational_fields'][key] = self._fields[key]
        return fields_classified

    def get_fields_for_db(self):
        return list(self.classified_fields['m2o'].keys()) \
               + list(self.classified_fields['non_relational_fields'].keys()) \
               + list(self.classified_fields['func_stored'].keys())

    def on_record_change(self, obj: list) -> None:
        pass

    def get_field(self, f_name):
        return self._fields.get(f_name).to_dict()

    def get_fields(self):
        return {f_name: obj.to_dict() for f_name, obj in self._fields.items()}

    def translate(self, params={}):
        phrase = params.get('phrase')
        return self.pool.get('api').internal_exec('translation', 'translate', {'phrase': phrase})
