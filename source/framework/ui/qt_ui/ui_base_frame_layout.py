from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from source.framework.utilities import tr
from .extended_widgets import *
from .ui_base import Mode, UiBase
from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt
from .baseFrameForm import BaseFrameForm


class UiBaseFrameLayout(QMainWindow, UiBase):

    def __init__(self, signal):
        super(UiBaseFrameLayout, self).__init__()
        self.signal = signal
        BaseFrameForm().setupUi(self)

    def add_nav_button(self, stack_index, ui_class, id, mode):
        navPushButton = ExtendedNavPushButton(self.navigationBarWidget)
        # navPushButton.setObjectName(model + '_nav_pushbutton')
        if mode == self.Mode.list_view:
            navPushButton.setText(tr('All: ') + tr(ui_class._model))
        elif mode == self.Mode.form_view:
            cuurent_name = self.api('exec', ui_class._model, 'read', {'ids': [id], 'as_relational': True})[0][1]
            navPushButton.setText(tr(ui_class._model) + ': ' + str(cuurent_name))
        elif mode == self.Mode.create_view:
            navPushButton.setText(tr('New: ') + tr(ui_class._model))
        elif mode == self.Mode.update_view:
            navPushButton.setText(tr('Edit: ') + tr(ui_class._model))

        navPushButton.setValue(stack_index)
        navPushButton.clicked.connect(lambda: self.navigate(navPushButton.getValue()))
        setattr(self, 'nav_pushbutton_' + str(stack_index), navPushButton)
        self.horizontalLayout.addWidget(navPushButton)

    def navigate(self, index):
        self.stackedWidget.setCurrentIndex(index)
        for i in range(self.stackedWidget.count() - 1, index, -1):
            self.stackedWidget.removeWidget(self.stackedWidget.widget(i))
            self.horizontalLayout.itemAt(i).widget().deleteLater()
            self.pool.get('ui_connector').stack_index -= 1

    def reset_navigation(self):
        n_pages = self.stackedWidget.count()
        for i in range(n_pages, 0, -1):
            self.stackedWidget.removeWidget(self.stackedWidget.widget(i - 1))
            self.horizontalLayout.itemAt(i - 1).widget().deleteLater()
        self.pool.get('ui_connector').stack_index = 0

    def set_elements(self, ui_shared):
        self.ui_shared = ui_shared
        self.set_post_menu_bar()
        self.setWindowTitle(tr('app_name'))
        icon = QIcon()
        icon.addFile('source/icons/app_logo.png', QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

    def set_pre_menu_bar(self):

        menu_obj = self.menuBar
        created_menues = dict()
        file_menu = menu_obj.addMenu('File')
        created_menues['File'] = file_menu

        return created_menues

    def set_post_menu_bar(self):

        pre = self.set_pre_menu_bar()
        created_menues = self.set_base_menu_bar(pre)

        menu_obj = self.menuBar
        file_menu = created_menues['File']

        # action = QAction('Setting', self)
        # action.triggered.connect\
        #     (lambda: self.signal.setting_view.emit())
        # setting = file_menu.addAction(action)
        # created_menues['Setting'] = setting

        action = QAction('Exit', self)
        action.triggered.connect \
            (lambda: self.signal.exit_view.emit())
        exit = file_menu.addAction(action)
        created_menues['Exit'] = exit

    def set_base_menu_bar(self, created_menues):
        def connector(self, data):
            def func():
                if data.get('view'):
                    view = getattr(self.Mode, data.get('view'))
                else:
                    view = self.Mode.list_view

                self.pool.get('ui_connector').base_signals.new_form.emit(self, data.get('action'), view, None, True)

            return func

        menu_bar_dict = self.ui_shared._menu_bar
        menu_obj = self.menuBar

        if menu_bar_dict:
            while len(menu_bar_dict) > 0:
                menu_bar_dict_ = dict(menu_bar_dict)
                for name, data in menu_bar_dict_.items():
                    if name in created_menues:
                        menu_bar_dict.pop(name)
                        continue

                    create = False
                    if not data.get('parent'):
                        create = True
                        parent = menu_obj
                    else:
                        if data.get('parent') in created_menues:
                            create = True
                            parent = created_menues.get(data.get('parent'))
                    if create:
                        if data.get('action'):
                            self.action_ = data.get('action')
                            action = QAction(tr(name), self)
                            #     action.setShortcut("Ctrl+Q")
                            action.setStatusTip(tr('Leave The App'))
                            action.triggered.connect(connector(self, data))
                            parent.addAction(action)
                            created_menues[name] = action
                        else:
                            menu = parent.addMenu(name)
                            created_menues[name] = menu

                        menu_bar_dict.pop(name)

        else:
            self.menuBar.setHidden(True)

        return created_menues

    def closeEvent(self, event):
        qm = QMessageBox
        if qm.question(self, 'Exiting', "You are about to exit app. Are you sure?", qm.Yes | qm.No) == qm.Yes:
            event.accept()  # let the window close
        else:
            event.ignore()
