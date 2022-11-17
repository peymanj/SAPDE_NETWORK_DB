# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'baseListViewWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from source.framework.ui.qt_ui.extended_widgets import *


class BaseListViewWidget(QtWidgets.QWidget):
    def setupUi(self, BaseListViewWidget):
        BaseListViewWidget.setObjectName("BaseListViewWidget")
        BaseListViewWidget.resize(640, 252)
        BaseListViewWidget.listGridLayout_3 = QtWidgets.QGridLayout(BaseListViewWidget)
        BaseListViewWidget.listGridLayout_3.setContentsMargins(0, 0, 0, 0)
        BaseListViewWidget.listGridLayout_3.setObjectName("listGridLayout_3")
        BaseListViewWidget.listMainWidget = QtWidgets.QWidget(BaseListViewWidget)
        BaseListViewWidget.listMainWidget.setObjectName("listMainWidget")
        BaseListViewWidget.listGridLayout = QtWidgets.QGridLayout(BaseListViewWidget.listMainWidget)
        BaseListViewWidget.listGridLayout.setContentsMargins(0, 0, 0, 0)
        BaseListViewWidget.listGridLayout.setObjectName("listGridLayout")
        BaseListViewWidget.listLine_4 = QtWidgets.QFrame(BaseListViewWidget.listMainWidget)
        BaseListViewWidget.listLine_4.setFrameShape(QtWidgets.QFrame.HLine)
        BaseListViewWidget.listLine_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        BaseListViewWidget.listLine_4.setObjectName("listLine_4")
        BaseListViewWidget.listGridLayout.addWidget(BaseListViewWidget.listLine_4, 0, 0, 1, 1)
        BaseListViewWidget.listLabel = ExtendedNavLabel(BaseListViewWidget.listMainWidget)
        BaseListViewWidget.listLabel.setObjectName("listLabel")
        BaseListViewWidget.listGridLayout.addWidget(BaseListViewWidget.listLabel, 1, 0, 1, 1)
        BaseListViewWidget.listLine_5 = QtWidgets.QFrame(BaseListViewWidget.listMainWidget)
        BaseListViewWidget.listLine_5.setFrameShape(QtWidgets.QFrame.HLine)
        BaseListViewWidget.listLine_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        BaseListViewWidget.listLine_5.setObjectName("listLine_5")
        BaseListViewWidget.listGridLayout.addWidget(BaseListViewWidget.listLine_5, 2, 0, 1, 1)
        BaseListViewWidget.listButtonMainWidget = QtWidgets.QWidget(BaseListViewWidget.listMainWidget)
        BaseListViewWidget.listButtonMainWidget.setObjectName("listButtonMainWidget")
        BaseListViewWidget.listGridLayout_2 = QtWidgets.QGridLayout(BaseListViewWidget.listButtonMainWidget)
        BaseListViewWidget.listGridLayout_2.setContentsMargins(0, 0, 0, 0)
        BaseListViewWidget.listGridLayout_2.setObjectName("listGridLayout_2")
        BaseListViewWidget.listMainTopButtonLayout = QtWidgets.QHBoxLayout()
        BaseListViewWidget.listMainTopButtonLayout.setObjectName("listMainTopButtonLayout")
        BaseListViewWidget.listActionButtonWidget = QtWidgets.QWidget(BaseListViewWidget.listButtonMainWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BaseListViewWidget.listActionButtonWidget.sizePolicy().hasHeightForWidth())
        BaseListViewWidget.listActionButtonWidget.setSizePolicy(sizePolicy)
        BaseListViewWidget.listActionButtonWidget.setObjectName("listActionButtonWidget")
        BaseListViewWidget.listHorizontalLayout = QtWidgets.QHBoxLayout(BaseListViewWidget.listActionButtonWidget)
        BaseListViewWidget.listHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        BaseListViewWidget.listHorizontalLayout.setObjectName("listHorizontalLayout")
        BaseListViewWidget.listCreatePushButton = QtWidgets.QPushButton(BaseListViewWidget.listActionButtonWidget)
        BaseListViewWidget.listCreatePushButton.setMinimumSize(QtCore.QSize(75, 0))
        BaseListViewWidget.listCreatePushButton.setDefault(False)
        BaseListViewWidget.listCreatePushButton.setObjectName("listCreatePushButton")
        BaseListViewWidget.listHorizontalLayout.addWidget(BaseListViewWidget.listCreatePushButton)
        BaseListViewWidget.listUpdatePushButton = QtWidgets.QPushButton(BaseListViewWidget.listActionButtonWidget)
        BaseListViewWidget.listUpdatePushButton.setMinimumSize(QtCore.QSize(75, 0))
        BaseListViewWidget.listUpdatePushButton.setObjectName("listUpdatePushButton")
        BaseListViewWidget.listHorizontalLayout.addWidget(BaseListViewWidget.listUpdatePushButton)
        BaseListViewWidget.listDeletePushButton = QtWidgets.QPushButton(BaseListViewWidget.listActionButtonWidget)
        BaseListViewWidget.listDeletePushButton.setMinimumSize(QtCore.QSize(75, 0))
        BaseListViewWidget.listDeletePushButton.setObjectName("listDeletePushButton")
        BaseListViewWidget.listHorizontalLayout.addWidget(BaseListViewWidget.listDeletePushButton)
        BaseListViewWidget.listOptionsToolButton = QtWidgets.QPushButton(BaseListViewWidget.listActionButtonWidget)
        BaseListViewWidget.listOptionsToolButton.setMinimumSize(QtCore.QSize(75, 0))
        BaseListViewWidget.listOptionsToolButton.setObjectName("listOptionsToolButton")
        BaseListViewWidget.listHorizontalLayout.addWidget(BaseListViewWidget.listOptionsToolButton)
        BaseListViewWidget.listMainTopButtonLayout.addWidget(BaseListViewWidget.listActionButtonWidget)
        BaseListViewWidget.listCommandButtonWidget = QtWidgets.QWidget(BaseListViewWidget.listButtonMainWidget)
        BaseListViewWidget.listCommandButtonWidget.setObjectName("listCommandButtonWidget")
        BaseListViewWidget.listHorizontalLayout_2 = QtWidgets.QHBoxLayout(BaseListViewWidget.listCommandButtonWidget)
        BaseListViewWidget.listHorizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        BaseListViewWidget.listHorizontalLayout_2.setObjectName("listHorizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(103, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        BaseListViewWidget.listHorizontalLayout_2.addItem(spacerItem)
        BaseListViewWidget.listMainTopButtonLayout.addWidget(BaseListViewWidget.listCommandButtonWidget)
        BaseListViewWidget.listGridLayout_2.addLayout(BaseListViewWidget.listMainTopButtonLayout, 0, 0, 1, 1)
        BaseListViewWidget.listGridLayout.addWidget(BaseListViewWidget.listButtonMainWidget, 3, 0, 1, 1)
        BaseListViewWidget.listTableWidgetLayout = QtWidgets.QHBoxLayout()
        BaseListViewWidget.listTableWidgetLayout.setObjectName("listTableWidgetLayout")
        BaseListViewWidget.listFirstTableWidget = ExtendedQTableWidget(BaseListViewWidget.listMainWidget)
        BaseListViewWidget.listFirstTableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        BaseListViewWidget.listFirstTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        BaseListViewWidget.listFirstTableWidget.setAlternatingRowColors(True)
        BaseListViewWidget.listFirstTableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        BaseListViewWidget.listFirstTableWidget.setObjectName("listFirstTableWidget")
        BaseListViewWidget.listFirstTableWidget.setColumnCount(0)
        BaseListViewWidget.listFirstTableWidget.setRowCount(0)
        BaseListViewWidget.listTableWidgetLayout.addWidget(BaseListViewWidget.listFirstTableWidget)
        BaseListViewWidget.listGridLayout.addLayout(BaseListViewWidget.listTableWidgetLayout, 4, 0, 1, 1)
        BaseListViewWidget.listGridLayout_3.addWidget(BaseListViewWidget.listMainWidget, 0, 0, 1, 1)
        # spacerItem1 = QtWidgets.QSpacerItem(20, 66, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # BaseListViewWidget.listGridLayout_3.addItem(spacerItem1, 1, 0, 1, 1)

        self.retranslateUi(BaseListViewWidget)
        QtCore.QMetaObject.connectSlotsByName(BaseListViewWidget)

    def retranslateUi(self, BaseListViewWidget):
        _translate = QtCore.QCoreApplication.translate
        BaseListViewWidget.setWindowTitle(_translate("BaseListViewWidget", "Form"))
        BaseListViewWidget.listLabel.setText(_translate("BaseListViewWidget", "TextLabel"))
        BaseListViewWidget.listCreatePushButton.setText(_translate("BaseListViewWidget", "New"))
        BaseListViewWidget.listUpdatePushButton.setText(_translate("BaseListViewWidget", "Edit"))
        BaseListViewWidget.listDeletePushButton.setText(_translate("BaseListViewWidget", "Delete"))
        BaseListViewWidget.listOptionsToolButton.setText(_translate("BaseListViewWidget", "Options"))
from source.framework.ui.qt_ui.extended_widgets.extended_table_widget import ExtendedQTableWidget
