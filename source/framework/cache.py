from json import loads, dumps
from os import path, getcwd
from datetime import datetime

from source.framework.base import Base


class Cache(Base):
    def __init__(self) -> None:
        super().__init__()
        self.cache_path = path.join(getcwd(), self.pool.get('setting').directories.Cache)
        self.cache_period = self.pool.get('setting').general.cache_period
        self.current_cache = None
        self.load_cache()

    def set(self, symbol_dict):
        symbol = list(symbol_dict.keys())[0]
        value = symbol_dict[symbol]
        time_stamped = {symbol: {'value': value, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}
        self.current_cache.update(time_stamped)
        with open(self.cache_path, 'w', encoding='utf-8-sig') as f:
            f.write(dumps(self.current_cache, ensure_ascii=False))

    def get(self, symbol, default=None):
        obj = self.current_cache.get(symbol, None)
        return obj.get('value') if obj else default 

    def is_updatable(self, symbol):
        obj = self.current_cache.get(symbol, None)
        if obj:
            time = datetime.strptime(obj.get('time'), '%Y-%m-%d %H:%M:%S') 
            dtime = datetime.now() - time
            hours = dtime.total_seconds() / 3600
            return True if hours >= self.cache_period else False
        else:
            return True

    def load_cache(self):
        with open(self.cache_path, 'a+', encoding='utf-8-sig') as f:
            try:
                f.seek(0)
                data = f.read()
                self.current_cache = loads(data)
            except Exception as e:
                self.current_cache = dict()

    