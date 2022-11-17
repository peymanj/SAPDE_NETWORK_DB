
import json
import os
from PyQt5.QtCore import QDir
from pathlib import Path

class ThemeLoader:

    def _replace_variable_to_value(self, contents: str, value_map: dict) -> str:
        for variable_name, color_code in value_map.items():
            # Replace the variable ${main_theme} contained in the svg file name bg the main-theme name.
            if variable_name == "main_theme":
                contents = contents.replace("${main_theme}", color_code)

            # Replace the variable by color code
            contents = contents.replace(f"${variable_name};", f"{color_code};")
        return contents
    
    def compile_stylesheet(self, stylesheet_file, theme_file) -> str:
        try:
            with stylesheet_file.open() as stylesheet_f, theme_file.open() as theme_f:
                stylesheet = stylesheet_f.read()
                value_map = json.load(theme_f)

                stylesheet_compiled = self._replace_variable_to_value(stylesheet, value_map)
                return stylesheet_compiled
        except FileNotFoundError:
            raise FileNotFoundError

    def load(self, theme=1) -> str:
        theme = list(("dark", "light"))[theme-1]
        QDir.addSearchPath('theme_path', "source/framework/ui/qt_ui/theme")
        stylesheet_file = Path(os.path.join(os.path.dirname(__file__), 'template.qss'))
        theme_colormap_file = Path(os.path.join(os.path.dirname(__file__), f'theme/{theme}.json'))
        return self.compile_stylesheet(stylesheet_file, theme_colormap_file)

