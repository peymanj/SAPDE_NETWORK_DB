from os import path
from pyodbc import IntegrityError
from source.framework import Base, fields as base_fields
from source.framework.utilities import log
from .scripts import *
from .sql_connector import Connector
from source.framework.utilities import tr



class DBNotCreated(Exception):
    pass

class DatabaseBackupFailed(Exception):
    pass

class DatabaseRestoreFailed(Exception):
    pass

class Orm(Base):

    def __init__(self):
        self.db_config = self.pool.get('config').database
        self.server = path.join(self.db_config.server, self.db_config.instance)
        self.port = self.db_config.port
        self.log_level = self.db_config.log_level  #log_error_only, log_All
        self.user = 'sa'
        self.old_password = '_!SaP_init_pAsS'
        self.password = 'Sap!_DE23@14_Jk'
        self.initiate(self.db_config.database)
        self.database = self.db_config.database

    def connect(self, database, password):
        log_level = Connector.LOG_ALL if  self.log_level == 'log_all' else Connector.LOG_ERROR_ONLY
        self.connector = Connector(self.server, self.port, database, self.user, password, log_level=log_level)

    def change_password(self, old_pass, new_pass):
        val, stat = self.connector.run_sql(change_password.format(*[new_pass, old_pass]))

    def db_exists(self, database):
        val, stat = self.connector.run_sql(check_db_sql, [database])
        return val[0].get('db_exists')

    def create_db(self, database):
        try:
            val, stat = self.connector.run_sql(create_db_sql.format(*[database] * 5))
        except Exception as e:
            log(e)
            raise DBNotCreated(
                f'Database {self.db_config.database_name} '
                f'on server {self.server} does not exist. '
                'Unable to create database.'
            )
        return stat

    def initiate(self, database):
        self.db_connected = False
        try:
            self.connect('master', self.password)
            self.db_exists(database)
        except:
            self.connect('master', self.old_password)
            self.change_password(self.old_password, self.password)
            self.connect('master', self.password)

        if not self.db_exists(database):
            self.create_db(database)
        self.connect(database, self.password)
        self.db_connected = True

    def exec(self, query, values=None, header=None):
        val, stat = self.connector.run_sql(query, values=values, header=header)
        return val, stat

    def backup_database(self, save_path):
        if '//' in save_path:
            save_path = save_path.replace('/', '\\')
        try:
            val, stat = self.connector.run_sql(backup_database, [self.db_config.database, save_path])
        except Exception as e:
            log(e)
            raise DatabaseBackupFailed(
                f'Unable to generate backup file from Database :{self.db_config.database_name} '
            )
        return stat

    def restore_database(self, file_path):
        self.connect('master', self.password)
        try:
            val, stat = self.connector.run_sql(restore_database.get('su').format(self.db_config.database), ddl=True)
            val, stat = self.connector.run_sql(restore_database.get('off').format(self.db_config.database), ddl=True)
            val, stat = self.connector.run_sql(restore_database.get('res'), [self.db_config.database, file_path], ddl=True)
            val, stat = self.connector.run_sql(restore_database.get('on').format(self.db_config.database), ddl=True)
            val, stat = self.connector.run_sql(restore_database.get('mu').format(self.db_config.database), ddl=True)
            self.connect(self.database, self.password)
        except Exception as e:
            log(e)
            raise DatabaseRestoreFailed(
                f'Unable to restore Database :{self.db_config.database_name} from file {file_path}'
            )
        return stat

    def model_to_db(self, model):

        fields = model._fields
        fields_copy = dict(fields)
        table = model._table
        id_col = model._id_column
        log = model._log

        def field2query(fobj_dict, mode='alter'):
            field_name = list(fobj_dict.keys())[0]
            fobj = fobj_dict.get(field_name)
            sql_type = getattr(fobj, 'sql_type')
            required = getattr(fobj, 'required') if field_name != id_col else True
            length = '(' + str(getattr(fobj, 'length')) + ')' if hasattr(fobj, 'length') else str()
            identity = 'IDENTITY(1,1)' if field_name == id_col else str()
            required = 'NOT NULL' if required else 'NULL'

            if mode == 'alter':
                query = f"ALTER COLUMN [{field_name}] [{sql_type}]{length} {required}"
            if mode == 'create':
                query = f"[{field_name}] [{sql_type}]{length} {identity} {required}, "
            if mode == 'add':
                query = f"ADD [{field_name}] [{sql_type}]{length} {identity} {required}"

            return query

        # check if table exists
        query = f"""
            SELECT 
            CASE 
            WHEN(
                EXISTS(SELECT * FROM sysobjects WHERE name='{table}' AND xtype='U'))
            THEN 'True'
            ELSE 'False'
            END
        """

        val, stat = self.connector.run_sql(query, header=False)
        if not eval(val[0][0]):  # creating table with id column
            id_field_str = field2query({id_col: fields.get(id_col)}, mode='create')
            create_query = f"CREATE TABLE [dbo].[{table}] ({id_field_str})"
            val, stat = self.connector.run_sql(create_query, header=False)

        # reading table columns and altering
        query = f"EXEC sp_columns '{table}'"
        val, stat = self.connector.run_sql(query, header=True)

        field_data = dict()
        for rec in val:  # existing fields in db
            field_data.update({rec.get('COLUMN_NAME'): rec})

        fields = dict(fields)
        fields.pop(id_col, None)

        for fname, obj in fields.items():  # ALtering or adding columns, id excluded
            if not obj.store:
                continue

            if field_data.get(fname):
                query = field2query({fname: obj}, mode='alter')
            else:
                query = field2query({fname: obj}, mode='add')
            query = f"ALTER TABLE [{table}] {query}"
            val, stat = self.connector.run_sql(query, header=True)

        if log:  # creating log fields in db
            log_fields = {
                'create_user': base_fields.Many2One('Creator user', relation='user'),
                'create_date': base_fields.Datetime('Create date'),
                'update_user': base_fields.Many2One('Last updator user', relation='user'),
                'update_date': base_fields.Datetime('Last update date'),
            }

            for fname, obj in log_fields.items():
                if field_data.get(fname):
                    query = field2query({fname: obj}, mode='alter')
                else:
                    query = field2query({fname: obj}, mode='add')
                query = f"ALTER TABLE [{table}] {query}"
                val, stat = self.connector.run_sql(query, header=True)

        # ------------------------------------ constraints
        # drop all constraints
        db_constraints, stat = self.connector.run_sql(get_constraints.format(table), header=False)
        for con in db_constraints:
            query = f"ALTER TABLE [{table}] DROP CONSTRAINT IF EXISTS [{con[0]}]"
            self.connector.run_sql(query, header=False)

        # ---- default ---
        for field_name, obj in fields_copy.items():
            default = getattr(obj, 'default')
            if default is not None:
                query = f"ALTER TABLE [dbo].[{table}] ADD  CONSTRAINT" \
                        f"[DF_{table}_{field_name}]  DEFAULT (({default})) FOR [{field_name}]"
                self.connector.run_sql(query, header=False)

        # other constraints
        sql_constraints = model._sql_constraints
        sql_constraints.append((f'PK_{table}', 'PRIMARY KEY CLUSTERED', [id_col]))

        if sql_constraints:
            for con in sql_constraints:
                name = con[0]
                keyword = con[1]
                fields = ', '.join([f'[{i}]' for i in con[2]])
                query = f"IF OBJECT_ID('{name}') IS NULL " \
                        f"ALTER TABLE [{table}] ADD CONSTRAINT [{name}] {keyword} ({fields}) "
                self.connector.run_sql(query, header=False)

    def read(self, model, context=dict()):
        table = model._table
        id_column = model._id_column
        ids = context.get('ids')
        fields = context.get('fields', list())
        post_proc = context.get('post_proc', True)
        as_relational = context.get('as_relational', False)

        # header = header if not post_proc else True
        # header = header if not as_relational else True
        post_proc = post_proc if not as_relational else False

        # if not fields:
        #     return list()

        if id_column not in fields:
            fields.append(id_column)

        fields_str = ', '.join([f'[{field}]' for field in fields])

        query = f"SELECT {fields_str} FROM [{table}] "
        if ids:
            ids_str = ', '.join([str(id) for id in ids])
            query += f"WHERE {id_column} IN ({ids_str})"
        else:
            if not ids and isinstance(ids, (tuple, list)):
                return list()

        if not table:
            if not model.load_stored_function:
                return []
            query = model.load_stored_function(context=context)
            query = 'Select * From ' + query

        if model._order:
            query += ' Order By ' + model._order

        records, stat = self.connector.run_sql(query, header=True)

        if not records:
            return list()

        if as_relational:
            records = self.read_as_relational(records, model)

        if post_proc and records:
            records = self.read_relational_post_process(model, records, fields)

        return records

    def read_as_relational(self, data, model):
        new_data = list()
        get_name = model.get_name
        id_col = model._id_column
        for rec in data:
            new_data.append((rec.get(id_col), get_name(rec.get(id_col))))
        return new_data

    def read_relational_post_process(self, model, data, fields):
        api = self.pool.get('api')
        for field in fields:
            if model._fields.get(field).relation:
                get_name = api._model_pool.get(model._fields.get(field).relation)().get_name
                for row in range(len(data)):
                    if data[row][field]:
                        data[row][field] = (data[row][field], get_name(data[row][field]))

            if isinstance(model._fields.get(field), base_fields.Selection):
                api = self.pool.get('api')
                func_name = model._fields.get(field).func.__name__
                for row in range(len(data)):
                    if data[row][field] != None:
                        data[row][field] = (data[row][field],
                                            api.internal_exec(model._name, func_name, {'id': data[row][field], 'context': data}))

        return data

    def search_relational_post_process(self, model, data, fields):
        api = self.pool.get('api')
        for field in fields:
            if model._fields.get(field).relation:
                get_name = api._model_pool.get(model._fields.get(field).relation)().get_name
                for row in range(len(data)):
                    if data[row][field]:
                        data[row][field] = (data[row][field], get_name(data[row][field]))
            if isinstance(model._fields.get(field), base_fields.Selection):
                api = self.pool.get('api')
                func_name = model._fields.get(field).func.__name__
                for row in range(len(data)):
                    if data[row][field]:
                        data[row][field] = (data[row][field],
                                            api.internal_exec(model._name, func_name, {'id': data[row][field], 'context': data}))
        return data

    def process_cond(self, cond_list):

        def tup2sql(tup):
            if isinstance(tup, str):
                return tup
            # (field, op, value)
            if isinstance(tup[2], str):
                return f" ([{tup[0]}] {tup[1]} {self.quoted(tup[2])}) "
            elif isinstance(tup[2], list) and tup[1].lower() == 'in':
                return f" ([{tup[0]}] {tup[1]} ({', '.join([str(i) for i in tup[2]])})) "
            elif isinstance(tup[2], bool):
                return f" ([{tup[0]}] {tup[1]} {self.quoted(tup[2])}) "
            else:
                return f" ([{tup[0]}] {tup[1]} {tup[2]}) "

        if not cond_list:
            return None
        if isinstance(cond_list[0], (tuple, list)):
            return [tup2sql(cond_list[0])]

        if isinstance(cond_list[0], str):
            op = cond_list[0]
            if isinstance(cond_list[1], (tuple, list)) or cond_list[1][:2] == ' (':
                cond_list[1] = tup2sql(cond_list[1])
                if isinstance(cond_list[2], (tuple, list)) or cond_list[2][:2] == ' (':
                    cond_list[2] = tup2sql(cond_list[2])
                    cond_list[0] = ' (' + cond_list[1] + op + cond_list[2] + ') '
                    del cond_list[1]
                    del cond_list[1]

                    if 1 == len(cond_list):
                        return cond_list
                    else:
                        x = self.process_cond(cond_list[1:])
                        return cond_list[:1] + x
                else:

                    cond_list = cond_list[:2] + self.process_cond(cond_list[2:])
                    cond_list[2] = ' (' + cond_list[1] + op + cond_list[2] + ') '
                    if 3 == len(cond_list):
                        return [cond_list[2]]
                    else:
                        x = self.process_cond(cond_list[1:])
                        return cond_list[:1] + x

            else:
                x = self.process_cond(cond_list[1:])
                cond_list = cond_list[:1] + x
                return ' (' + cond_list[1] + op + cond_list[2] + ') '
        else:
            return None

    def search(self, model, context=None):
        context = context if context else dict()

        table = model._table
        ids = context.get('ids', None)
        fields = context.get('fields', list())
        id_column = context.get('id_column', 'id')
        post_proc = context.get('post_proc', True)
        condition = context.get('condition', None)  # list of tuples, polish notation
        id_only = context.get('id_only', False)

        if not condition:
            return list()

        # if not fields:
        #     return list()

        if id_column not in fields:
            fields.append(id_column)

        fields_str = ', '.join([f'[{field}]' for field in fields])
        table = f'[{table}]' if table else model.load_stored_function(context=context)
        query = f"SELECT {fields_str} FROM {table} WHERE {self.process_cond(condition)[0]}"

        records, stat = self.connector.run_sql(query, header=True)

        if id_only:
            ids = list()
            if records:
                for rec in records:
                    ids.append(rec.get(id_column))
            return ids
        if post_proc and records:
            records = self.search_relational_post_process(model, records, fields)

        return records

    def quoted(self, val):
        if isinstance(val, str):
            return "'" + val + "'"
        else:
            return "'" + str(val) + "'"

    @staticmethod
    def process_unique_error(ret, model):
        if isinstance(ret, IntegrityError) and 'UNIQUE KEY' in ret.args[1]:
            unique_name = ret.args[1].split("'")[1]
            for tup in model._sql_constraints:
                if tup[0] == unique_name:
                    fields_str = '\n'.join([tr(model._fields.get(f).string) for f in tup[2]])
            ret = Exception(f"Failed to save record.\n\nFollowing fields have duplicate values:\n\n{fields_str}")
        return ret

    def create(self, model, context=dict()):
        table = model._table
        field_values = context.get('field_values', None)
        if not field_values:
            return

        fields = list(field_values.keys())
        vals = list(str(v) for v in field_values.values())
        fields_str = ', '.join(['[' + i + ']' for i in fields])

        for i in range(len(fields)):
            f_obj = model._fields.get(fields[i])
            if getattr(f_obj, 'type').lower() in ('char', 'date', 'datetime', 'binary', 'boolean'):
                vals[i] = self.quoted(vals[i])
        vals_str = ', '.join(vals)

        query = f"INSERT INTO [{table}] ({fields_str}) OUTPUT Inserted.ID VALUES ({vals_str})"
        records, stat = self.connector.run_sql(query, header=False)
        records = Orm.process_unique_error(records, model)
        return records

    def delete(self, model, context=None):
        context = context if context else dict()
        table = model._table
        condition = context.get('condition', None)  # list of tuples, polish notation
        if not condition:
            return None
        query = f"DELETE FROM [{table}] OUTPUT deleted.[id] WHERE {self.process_cond(condition)[0]}"
        records, stat = self.connector.run_sql(query, header=False)

        return records

    def update(self, model, context=dict()):

        table = model._table
        field_values = context.get('field_values', None)
        id = context.get('id', None)
        if not field_values or not id:
            return

        field_str_list = list()
        for field, val in field_values.items():
            f_obj = model._fields.get(field)
            if getattr(f_obj, 'type').lower() in ('char', 'date', 'datetime', 'binary', 'boolean'):
                val = self.quoted(val)
            field_str_list.append('[' + field + '] = ' + str(val))
        fields_str = ', '.join(field_str_list)

        query = f"UPDATE [{table}] SET {fields_str} OUTPUT INSERTED.ID WHERE [{model._id_column}] = {id}"
        records, stat = self.connector.run_sql(query, header=False)
        records = Orm.process_unique_error(records, model)
        return records
