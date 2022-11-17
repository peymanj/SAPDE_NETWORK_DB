from PyQt5 import QtCore
from PyQt5 import QtWidgets
from source.framework.intergration.port import port_read
from source.framework.ui.qt_ui.theme.colors import ColorManager
from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *
from source.framework.intergration.port.port_read import PortRead
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette

from source.framework.utilities import tr


class UiPartForm(UiBaseClass):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_init(self):
        save_and_new_button = QtWidgets.QPushButton(self.form_widget.formCommandButtonWidget)
        save_and_new_button.setMinimumSize(QtCore.QSize(75, 0))
        self.form_widget.formHorizontalLayout_2.insertWidget(2, save_and_new_button)
        save_and_new_button.setText(tr("Save and create new"))
        save_and_new_button.clicked.connect(self.save_and_create_new)

        self.port_read = PortRead()
        self.port_read.data_signal.connect(self.receive_weight)
        self.weight_qwidget = getattr(self.form_widget, 'weight_qwidget')
        self.weight_qwidget.focus_in_signal.connect(
            lambda: QTimer.singleShot(500, self.start_weight_thread))
        self.weight_qwidget.focus_out_signal.connect(self.stop_weight_thread)
        self.weight_qwidget.setMaximum(100000)
        getattr(self.form_widget, 'side_qwidget').currentIndexChanged.connect(self.set_serials)
        self.set_layout()

        item_set_id = self.get_current_parent('item_set')
        parts = self.api('exec', 'part', 'search', {'condition': [('item_set', '=', item_set_id)]})
        if len(parts) == 0:
            index = 0
        elif len(parts) == 1 and parts[0].get('side') == 1:
            index = 1
        elif len(parts) == 1 and parts[0].get('side') == 2:
            index = 0
        else:
            index = 0
        self.form_widget.side_qwidget.setCurrentIndex(index)
        return super().create_init()

    def update_init(self):
        self.port_read = PortRead()
        self.port_read.data_signal.connect(self.receive_weight)
        self.weight_qwidget = getattr(self.form_widget, 'weight_qwidget')
        self.weight_qwidget.focus_in_signal.connect(
            lambda: QTimer.singleShot(500, self.start_weight_thread))
        self.weight_qwidget.focus_out_signal.connect(self.stop_weight_thread)
        self.weight_qwidget.setMaximum(100000)
        getattr(self.form_widget, 'side_qwidget').currentIndexChanged.connect(self.set_serials)
        self.set_layout()
        return super().update_init()

    def form_init(self):
        self.weight_qwidget = getattr(self.form_widget, 'weight_qwidget')
        self.set_layout()
        return super().form_init()

    def start_weight_thread(self):
        self.current_color = self.weight_qwidget.palette().color(QPalette.Base).name()
        color = ColorManager().get_color
        self.weight_qwidget.setStyleSheet(f"QSpinBox {{background-color : {color('WeightSpinBox', 'background')};}}")
        QTimer.singleShot(100, self.port_read.start)

    def receive_weight(self, weight):
        weight = int(float(weight) * 1000)
        getattr(self.form_widget, 'weight_qwidget').setValue(weight)

    def stop_weight_thread(self):
        self.port_read.stop()
        self.weight_qwidget.setStyleSheet("QSpinBox {{background-color : {}; }}".format(self.current_color))

    def set_layout(self):

        set_id = self.get_form_fields(self.form_widget, ['item_set']).get('item_set')
        order_item_id = self.api('exec', 'item_set', 'related_read', context={'id': set_id, 'field': 'order_item'})
        self.order_item = self.api('exec', 'order_item', 'read',
                                   {'ids': [order_item_id], 'post_proc': False, 'return_object': False})[0]

        self.check_list = list()
        for i in range(8):
            if i >= self.order_item['no_fchecks']:
                getattr(self.form_widget, 'check' + str(i + 1) + '_qwidget').setHidden(True)
                getattr(self.form_widget, 'check' + str(i + 1) + '_label').setHidden(True)
            else:
                self.check_list.append(getattr(self.form_widget, 'check' + str(i + 1) + '_qwidget').getValue())


        if not self.order_item['image_required']:
            getattr(self.form_widget, 'image_qwidget').setEnabled(False)

        if not self.order_item['check_weight']:
            getattr(self.form_widget, 'weight_qwidget').setEnabled(False)

        self.model_size_rel = self.api('exec', 'model_item', 'search',
                                       {'condition': ['and', ('model', '=', self.order_item['model']),
                                                      ('size', '=', self.order_item['size'])],
                                        'post_proc': False, 'return_object': False})[0]
        self.set_serials()

    def set_serials(self, val=None):
        val = getattr(self.form_widget, 'side_qwidget').getValue()
        n_serials = 0
        if val == 1:  # front
            n_serials = self.model_size_rel['no_front_serials']
        elif val == 2:  # back
            n_serials = self.model_size_rel['no_back_serials']
        for i in range(8):
            if i >= n_serials:
                getattr(self.form_widget, 'sn' + str(i + 1) + '_qwidget').setValue(False)
                getattr(self.form_widget, 'sn' + str(i + 1) + '_qwidget').setHidden(True)
                getattr(self.form_widget, 'sn' + str(i + 1) + '_label').setHidden(True)
            else:
                getattr(self.form_widget, 'sn' + str(i + 1) + '_qwidget').setHidden(False)
                getattr(self.form_widget, 'sn' + str(i + 1) + '_label').setHidden(False)

        for i in range(n_serials - 1):
            widget = getattr(self.form_widget, 'sn' + str(i + 1) + '_qwidget')
            if not widget.return_press_connected:
                widget.returnPressed.connect(lambda: self.focusNextPrevChild(True))
                widget.return_press_connected = True



    def validate(self):
        def ask_for_pass():
            text, ok = QInputDialog.getText(self, tr('Grant Access'),
                                            tr('Password:'), QLineEdit.Password)
            if ok:
                if self.api('exec', 'admin_setting', 'master_pass_check', context={'password': text}):
                    return True
                else:
                    self.msg.show(self.msg.Error, 'Invalid password.')
            else:
                return False

        self.weight_qwidget = getattr(self.form_widget, 'weight_qwidget')
        if self.weight_qwidget.isEnabled():

            val = getattr(self.form_widget, 'side_qwidget').getValue()
            if val == 1:  # front
                min_weight = self.model_size_rel['min_weight_front']
                max_weight = self.model_size_rel['max_weight_front']
            elif val == 2:  # back
                min_weight = self.model_size_rel['min_weight_back']
                max_weight = self.model_size_rel['max_weight_back']

            if int(self.weight_qwidget.getValue()) > int(max_weight):
                if self.msg.show(self.msg.Question, 'Part over weight, submit?',
                                 add_msg=f'max allowd weight: {max_weight} gr'):
                    if not ask_for_pass():
                        return False
                else:
                    return False

            if int(self.weight_qwidget.getValue()) < int(min_weight):
                if self.msg.show(self.msg.Question, 'Part under weight, submit?',
                                 add_msg=f'min allowd weight: {min_weight} gr'):
                    if not ask_for_pass():
                        return False
                else:
                    return False

        if self.order_item['image_required']:
            if not getattr(self.form_widget, 'image_qwidget').val:
                self.msg.show(self.msg.Error, 'Image not loaded')

        # for i in range(8):
        #     if not getattr(self.form_widget, 'sn' + str(i + 1) + '_qwidget').isHidden():
        #         if not getattr(self.form_widget, 'sn' + str(i + 1) + '_qwidget').getValue():
        #             self.msg.show(self.msg.Error, 'Serial required')

        return True

    def save(self):
        if not self.validate():
            return
        self.check_list_new = list()
        for i in range(8):
            if i < self.order_item['no_fchecks']:
                self.check_list_new.append(getattr(self.form_widget, 'check' + str(i + 1) + '_qwidget').getValue())
        if self.check_list != self.check_list_new:
            curr_user = self.pool.get('current_user')
            self.set_form_fields(self.form_widget, {
                'check_user': (curr_user['id'],
                               f"{curr_user['fullname']} ({curr_user['username']})")})
        return super().save()

    def save_and_create_new(self):
        if not self.validate():
            return
        self.check_list_new = list()
        for i in range(8):
            if i < self.order_item['no_fchecks']:
                self.check_list_new.append(getattr(self.form_widget, 'check' + str(i + 1) + '_qwidget').getValue())
        if self.check_list != self.check_list_new:
            curr_user = self.pool.get('current_user')
            self.set_form_fields(self.form_widget, {
                'check_user': (curr_user['id'],
                               f"{curr_user['fullname']} ({curr_user['username']})")})
        return super().save_and_create_new()

    def reopen_create_preprocess(self):
        box_id = self.get_current_parent('box')
        item_sets = self.api('exec', 'item_set', 'search',
                             {'condition': [('box', '=', box_id)], 'id_only': True})
        item_sets = sorted(item_sets)
        for id in item_sets:
            if self.get_current_parent('item_set') <= id:
                parts = self.api('exec', 'part', 'search', {'condition': [('item_set', '=', id)]})
                if len(parts) < 2:
                    return id
        return False

    _model = 'part'

    _menu_bar = False
    _list_view = {
        'first_list': {'source': 'UiPartForm'}
    }

    _form_view = {
        'fields': [
            'item_set',
            'side',
            'image',
            {'weight': {'max': 10000}},
            'sn1',
            'sn2',
            'sn3',
            'sn4',
            'sn5',
            'sn6',
            'sn7',
            'sn8',
            'check1',
            'check2',
            'check3',
            'check4',
            'check5',
            'check6',
            'check7',
            'check8',
            {'check_user': {'invisible': True}},
        ],

    }
