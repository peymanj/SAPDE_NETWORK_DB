from source.framework.base import Base


class Fields(Base):
    def __init__(self) -> None:
        super().__init__()

    def integer(*args, **kwargs):
        return Integer(*args, **kwargs)

    def date(*args, **kwargs):
        return Date(*args, **kwargs)

    def datetime(*args, **kwargs):
        return Datetime(*args, **kwargs)

    def char(*args, **kwargs):
        return Char(*args, **kwargs)

    def boolean(*args, **kwargs):
        return Boolean(*args, **kwargs)

    def binary(*args, **kwargs):
        return Binary(*args, **kwargs)

    def selection(*args, **kwargs):
        return Selection(*args, **kwargs)

    def many2one(*args, **kwargs):
        return Many2One(*args, **kwargs)

    def one2many(*args, **kwargs):
        return One2Many(*args, **kwargs)

    def many2many(*args, **kwargs):
        return Many2Many(*args, **kwargs)

    def function(*args, **kwargs):
        return Function(*args, **kwargs)


class Field:
    type = None
    string = None
    required = False
    relation = False
    model = None
    default = None
    store = True
    sql_type = None
    display = None
    search = True
    local_data = False

    def __init__(self, *args, **kwargs):
        self.set_positionals(*args)
        self.set_optionals(**kwargs)

    def set_positionals(self, *args):
        self.string = args[0]

    def set_optionals(self, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs.get(key))

    def to_dict(self):
        params = {}
        items = {k: v for k, v in Field.__dict__.items() if not k.startswith('__') and not callable(v)}
        items.update(self.__dict__)
        for name, val in items.items():
            if not callable(val):
                params[name] = val
            else:
                params[name] = val.__name__
        return params


class Integer(Field):
    def __init__(self, *args, **kwargs):
        self.sql_type = 'int'
        self.type = 'integer'
        super().__init__(*args, **kwargs)


class Date(Field):
    def __init__(self, *args, **kwargs):
        self.sql_type = 'date'
        self.type = 'date'
        super().__init__(*args, **kwargs)


class Datetime(Field):
    def __init__(self, *args, **kwargs):
        self.sql_type = 'datetime'
        self.type = 'datetime'
        super().__init__(*args, **kwargs)


class Char(Field):
    def __init__(self, *args, **kwargs):
        self.length = 1
        self.sql_type = 'nvarchar'
        self.type = 'char'
        super().__init__(*args, **kwargs)


class Many2One(Field):
    def __init__(self, *args, **kwargs):
        self.type = 'many2one'
        self.sql_type = 'int'
        super().__init__(*args, **kwargs)


class One2Many(Field):
    def __init__(self, *args, **kwargs):
        self.many = None
        self.type = None
        self.field = None
        self.store = False
        super().__init__(*args, **kwargs)


class Boolean(Field):
    def __init__(self, *args, **kwargs):
        self.sql_type = 'bit'
        self.type = 'boolean'
        if kwargs.get('default') is not None:
            if isinstance(kwargs.get('default'), bool):
                self.default = int(kwargs.get('default'))
            kwargs.pop('default')
        super().__init__(*args, **kwargs)


class Binary(Field):
    def __init__(self, *args, **kwargs):
        self.length = 'MAX'
        self.sql_type = 'nvarchar'
        self.type = 'binary'
        super().__init__(*args, **kwargs)


class Selection(Field):
    def __init__(self, *args, **kwargs):
        self.func = None
        self.relation = None
        self.sql_type = 'int'
        self.type = 'selection'
        super().__init__(*args, **kwargs)


class Many2Many(Field):
    def __init__(self, *args, **kwargs):
        self.type = 'many2many'
        self.source_field = None
        self.target_field = None
        self.store = False
        super().__init__(*args, **kwargs)


class Function(Field):
    def __init__(self, *args, **kwargs):
        self.func = None
        self.type = 'function'
        save_type = kwargs.get('store') or str()
        self.sql_type = getattr(Fields, save_type)(str()).sql_type if save_type else None
        self.store = True if save_type else False
        super().__init__(*args, **kwargs)
