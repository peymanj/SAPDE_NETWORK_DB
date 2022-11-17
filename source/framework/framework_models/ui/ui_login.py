from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from source.framework.ui.qt_ui.ui_base import UiBase
from source.framework.utilities import tr
from .loginForm import LoginForm



class UiLogin(QMainWindow, UiBase):
    login_signal = pyqtSignal()
    field_map_dict = {
        'usernameLineEdit': 'username',
        'passwordLineEdit': 'password',
    }
    _use_template = False

    def __init__(self):
        super(UiLogin, self).__init__()
        LoginForm().setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.password_qwidget.showEye()
        self.loginPushButton.clicked.connect(self.validate)
        self.cancelPushButton.clicked.connect(self.close)
        self.model = 'user'
        
        
    def show(self):
        super().show()
        self.username_qwidget.setFocus()


    def set_form_data(self, data):
        if not data['logged_in']:
            self.messageLabel.setText(tr("Incorrect username or password"))
        elif not data['active']:
            self.messageLabel.setText(tr("User is not active."))
        else:
            self.login_signal.emit()

    def validate(self):
        form_data = self.get_form_fields(self, ['username', 'password'])
        res = self.api_post('login', form_data)
        if res.get('logged_in'):
            self.pool.set(res.get('logged_in'), 'current_user')
        self.set_form_data(res)

        


    