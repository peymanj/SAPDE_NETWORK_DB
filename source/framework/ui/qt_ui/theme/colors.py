from source.framework.pool import Pool

class ColorManager:

    def __init__(self) -> None:
        init_setting = Pool.get('user_setting')
        if init_setting and init_setting.get('theme'):
            self.theme_index = init_setting.get('theme')
        else:
            self.theme_index = 2 # light theme default
            
    def get_color(self, obj_name, prop_name, custom_color=False, theme_based=True):
        if theme_based:

            if self.theme_index == 1: theme = 'dark'  # dark theme is active
            elif self.theme_index == 2: theme = 'light'
            else: theme = 'light'  # default light theme

            if custom_color: theme = custom_color 
            return colors.get(obj_name).get(prop_name).get(theme)
     


colors = {
    'ExtendedNavLabel': {
        'background': {'light': '#e8f8ff' , 'dark': '#002d42'},
    },
    'WeightSpinBox': {
        'background': {'light': '#d5eef7' , 'dark': '#022152'},
    }

}