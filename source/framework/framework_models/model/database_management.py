from source.framework.utilities import log
from source.framework.base_model import Model
from source.framework.fields import Fields
from hashlib import sha256, md5

class DatabaseManagement(Model):
    def __init__(self) -> None:
        super().__init__()
    
    _name = 'database_management'
    _init = False

    def backup(self, context={}):
        stat = self.pool.get('orm').backup_database(context.get('save_path'))
        return stat

    def restore(self, context={}):
        stat = self.pool.get('orm').restore_database(context.get('file_path'))
        return stat

    def get_active_db_name(self, context={}):
        return self.pool.get('orm').database

