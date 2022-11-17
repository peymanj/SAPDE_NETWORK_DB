from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal, Qt
from source.framework.ui.qt_ui.ui_base_class_wizard import UiBaseClassWizard
from source.framework.ui.qt_ui.icon.icons import IconManager
from .databaseManagmentForm import DatabaseManagementForm
from source.framework.framework_models.ui.userAccessForm import UserAccessForm
from PyQt5.QtWidgets import QFileDialog


class UiDatabaseManagementForm(QMainWindow, UiBaseClassWizard):
    login_signal = pyqtSignal()
    field_map_dict = {
        'usernameLineEdit': 'username',
        'passwordLineEdit': 'password',
    }
    _use_template = False
    _model = 'database_management'

    def __init__(self):
        super(UiDatabaseManagementForm, self).__init__()
        DatabaseManagementForm().setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.set_form_data()
        self.set_connections()
        self.show()


    def set_connections(self):
        self.cancelRestore_qwidget.clicked.connect(self.close)
        self.restore_qwidget.clicked.connect(self.restore)
        self.cancelBackup_qwidget.clicked.connect(self.close)
        self.backup_qwidget.clicked.connect(self.backup)
        self.restore_qwidget.clicked.connect(self.restore)
        self.browseButtonRestore_qwidget.clicked.connect(self.get_bkp_file_path)
        self.browseButtonBackup_qwidget.clicked.connect(self.get_folder_path)

    def show(self):
        super().show()

    def set_form_data(self):
        icon = IconManager().get_icon('folder', theme_based=False)
        self.browseButtonBackup_qwidget.setIcon(icon)
        self.browseButtonRestore_qwidget.setIcon(icon)
        active_db_name = self.api('exec', 'database_management', 'get_active_db_name', context={})
        self.dbNameRestore_qwidget.setText(active_db_name)
        self.dbNameBackup_qwidget.setText(active_db_name)

    def backup(self):
        file_path = self.backupLocation_qwidget.text()
        self.setEnabled(False)
        try:
            if file_path:
                stat = self.api('exec', 'database_management', 'backup',
                                             {'save_path': file_path})
                if stat:
                    self.msg.show(self.msg.Info, 'Backup Successful.')
                    self.close()
                else:
                    self.msg.show(self.msg.Error, 'Unable to backup database.')
            else:
                self.msg.show(self.msg.Error, 'Invalid address.')
        except:
            self.setEnabled(True)

    def restore(self):
        file_path = self.backupFile_qwidget.text()
        self.setEnabled(False)
        try:
            if file_path:
                stat = self.api('exec', 'database_management', 'restore',
                                             {'file_path': file_path})
                if stat:
                    self.msg.show(self.msg.Info, 'Restore Successful. Restart the app.')
                    self.close()
                else:
                    self.msg.show(self.msg.Error, 'Unable to restore database.')
            else:
                self.msg.show(self.msg.Error, 'Invalid address.')
        except:
            self.setEnabled(True)

    def get_folder_path(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save as ...", "",
                                                   "Backup Files (*.bak);;All Files (*)")
        if file_name:
            self.backupLocation_qwidget.setText(file_name)

    def get_bkp_file_path(self):
        file_name, _ = QFileDialog.getOpenFileName(self,"Select backup file ...", "",
                                                  "Backup Files (*.bak);;All Files (*)")
        if file_name:
            self.backupFile_qwidget.setText(file_name)

