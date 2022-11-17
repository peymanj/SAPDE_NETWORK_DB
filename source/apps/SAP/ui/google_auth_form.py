# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GoogleAuthLoadForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from source.framework.ui.qt_ui import ExtendedMessageBox
from .google_auth_help_form import GoogleAuthHelpForm
from genericpath import isfile

class GoogleAuthForm(QtWidgets.QMainWindow):
    def setupUi(self, parent):
        self.form_parent = parent
        self.setObjectName("GoogleAuth")
        self.resize(482, 80)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.pathLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.pathLineEdit.setObjectName("pathLineEdit")
        self.horizontalLayout_2.addWidget(self.pathLineEdit)
        self.browsePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.browsePushButton.setObjectName("browsePushButton")
        self.horizontalLayout_2.addWidget(self.browsePushButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.submitPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.submitPushButton.setObjectName("submitPushButton")
        self.horizontalLayout.addWidget(self.submitPushButton)
        self.helpPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.helpPushButton.setObjectName("helpPushButton")
        self.horizontalLayout.addWidget(self.helpPushButton)
        self.cancelPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.browsePushButton.clicked.connect(self.get_path)
        self.cancelPushButton.clicked.connect(self.close)
        self.submitPushButton.clicked.connect(self.save_file)

        self.helpPushButton.clicked.connect(self.show_help)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def get_path(self):
        self.cred_path = QtWidgets.QFileDialog.\
            getOpenFileNames(self, "Select credentional file", QtCore.QDir.currentPath(), "JSON Files (*.json)")
        if self.cred_path:
            self.pathLineEdit.setText(self.cred_path[0][0])
        
        
    def show_help(self):
        self.help_form = GoogleAuthHelpForm()
        self.help_form.setupUi()
        self.help_form.show()

    def save_file(self):
        self.msg = ExtendedMessageBox()
        cred_path = self.pathLineEdit.text()
        if not cred_path:
            self.msg.show(self.msg.Error, 'Invalid file path.')
        with open(cred_path, 'r') as f:
            fstring = f.readlines()
            if fstring:
                self.form_parent.api('exec', 'order', 'copy_cred_file', context={'file': fstring[0]})
                self.close()
            else:
                self.msg.show(self.msg.Error, 'Invalid file content')

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("GoogleAuth", "Google API credentials required"))
        self.label.setText(_translate("GoogleAuth", "Credential file path:"))
        self.browsePushButton.setText(_translate("GoogleAuth", "Browse"))
        self.submitPushButton.setText(_translate("GoogleAuth", "Submit"))
        self.helpPushButton.setText(_translate("GoogleAuth", "Help"))
        self.cancelPushButton.setText(_translate("GoogleAuth", "Cancel"))