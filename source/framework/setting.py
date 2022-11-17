from configparser import ConfigParser


class SettingItem:
    def __init__(self, items_dict):
        for key in items_dict:
            setattr(self, key.lower(), self._to_number(items_dict[key]))
            
    def _to_number(self, n):
        try: 
            n = int(n) 
        except:
            try:
                n = float(n)
            except:
                pass
        finally:
            return n

class Setting:
    def __init__(self, config_path):
        super(Setting, self).__init__()
        self.config_path = config_path
        self.load()

    def load(self):
        config = ConfigParser(inline_comment_prefixes=";")
        config.read(self.config_path, encoding='utf-8-sig')
        sections = config.sections()
        # items = {}
        for section in sections:
            items_dict = dict(config.items(section))
            # items[section.lower()] = setting_item(items_dict)
            setattr(self, section.lower(), SettingItem(items_dict))
    # locals().update(items)


