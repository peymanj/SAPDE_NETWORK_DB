from source.framework.utilities import log
from source.framework.base_model import Model
from source.framework.fields import Fields


class Translation(Model):
    def __init__(self) -> None:
        super().__init__()

    _name = 'translation'
    _table = 'translation'
    _id_column = 'id'
    _init = True
    _get_name_string = '{phrase} -> {translation}'
    _fields = {
        'id': Fields.integer('id'),
        'phrase': Fields.char('Phrase', length=500, required=True),
        'translation': Fields.char('Translation', length=500, required=True),
    }

    _sql_constraints = [
        ('unique_phrase', 'unique', ['Phrase']),
    ]

    def translate(self, params):
        phrase = params.get('phrase')
        if not phrase:
            return ""

        try:
            phrase = phrase.replace("'", "''") # escaping single quote in t-sql
            ids = self.search({'condition': [('phrase', '=', phrase)]})
        except Exception as e:
            ids = None

        if not ids:
            return phrase
        else:
            return ids[0].get('translation')
