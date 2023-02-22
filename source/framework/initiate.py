import sys
from os import getenv, path, environ

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from datetime import datetime
from source.framework.utilities import exception_handler, log
from source.framework.framework_models.ui.splash import SplashScreen
from source.framework.ui.qt_ui.theme.theme_loader import ThemeLoader
from source.framework.pool import Pool as pool, UiModelPool
from source.framework.ui.qt_ui.ui_connector import UiConnector
from source.framework.framework_models.ui.ui_login import UiLogin
from source.framework.setting import Setting
from source.framework.ui.qt_ui.theme.theme_loader import ThemeLoader
from source.framework.ui.qt_ui.extended_widgets import ExtendedMessageBox
import argparse
from source.framework.sql_orm import Orm
from source.framework.framework_upgrade import FrameworkUpgrade
from source.framework.app_upgrade import AppUpgrade
from source.framework.api import Api


config_path = path.join(getenv('LOCALAPPDATA'), r"sap\config\config.ini")
setting_path = path.join(getenv('LOCALAPPDATA'), r"sap\config\setting.ini")
environ['QT_QUICK_CONTROLS_STYLE'] = (sys.argv[1] if len(sys.argv) > 1 else "Default")



sys.excepthook = exception_handler
class Initiate():

    @staticmethod
    def start(args):
        app = QApplication(sys.argv)

        # argparse
        parser = argparse.ArgumentParser(description="EasysErp Argument Parser",
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("-d", "--debug", action="store_true", help="Run in debug mode. No splash Screen.")
        parser.add_argument("-u", "--upgrade", action="store_true", help="Upgrade Database")
        args = parser.parse_args()
        init_args = vars(args)
        pool.set(init_args.get('debug'), 'debug')
        config = pool.set(Setting(config_path), 'config')
        setting = pool.set(Setting(setting_path), 'setting')
        orm = pool.set(Orm(), 'orm')
        api = pool.set(Api(), 'api')
        pool.set(UiModelPool.init(), 'ui_models')
        now = datetime.now()
        splash_screen = SplashScreen()
        splash_screen.show()

        def upgrade():
            app_upgrade_obj = AppUpgrade()
            framework_upgrade_obj = FrameworkUpgrade()

            app_upgrade_obj.start()
            framework_upgrade_obj.start()

            app_upgrade_obj.set_access()
            framework_upgrade_obj.set_access()

        if init_args.get('upgrade'):
            start_time = datetime.now()
            log('Initiating upgrade ...', print_msg=True)
            upgrade()
            end_time = datetime.now()
            log('Upgrade completed in {}'.format(end_time - start_time), print_msg=True)

        splash_time = 0.2 if (init_args.get('debug') or init_args.get('upgrade')) else 5
        while (datetime.now() - now).seconds < splash_time:
            QApplication.processEvents()

        ui_connector = pool.set(UiConnector(), 'ui_connector')

        user_setting = ui_connector.api_get('get_init_setting', {'model': 'user_setting'})['data']
        user_setting = pool.set(user_setting, 'user_setting')

        if user_setting and user_setting.get('theme'):
            app.setStyleSheet(ThemeLoader().load(user_setting.get('theme')))
        else:
            app.setStyleSheet(ThemeLoader().load(2))
        splash_screen.close()

        ui_login = UiLogin()
        ui_login.login_signal.connect(ui_login.close)
        ui_login.login_signal.connect(lambda: print('loggged'))
        ui_login.login_signal.connect(ui_connector.initiate_app)
        ui_login.show()

        sys.exit(app.exec_())
