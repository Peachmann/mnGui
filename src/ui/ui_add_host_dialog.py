# Form implementation generated from reading ui file '/home/peach/Uni/mnGui/src/ui/add_host_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(335, 325)
        self.button_box = QtWidgets.QDialogButtonBox(Dialog)
        self.button_box.setGeometry(QtCore.QRect(80, 270, 181, 32))
        self.button_box.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.button_box.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.setObjectName("button_box")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 20, 281, 251))
        self.layoutWidget.setObjectName("layoutWidget")
        self.full_layout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.full_layout.setContentsMargins(0, 0, 0, 0)
        self.full_layout.setObjectName("full_layout")
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.form_layout.setObjectName("form_layout")
        self.switch_label = QtWidgets.QLabel(self.layoutWidget)
        self.switch_label.setObjectName("switch_label")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.switch_label)
        self.switch_box = QtWidgets.QComboBox(self.layoutWidget)
        self.switch_box.setObjectName("switch_box")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.switch_box)
        self.host_label = QtWidgets.QLabel(self.layoutWidget)
        self.host_label.setObjectName("host_label")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.host_label)
        self.host_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.host_name.setEnabled(False)
        self.host_name.setMaxLength(6)
        self.host_name.setObjectName("host_name")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.host_name)
        self.mac_label = QtWidgets.QLabel(self.layoutWidget)
        self.mac_label.setObjectName("mac_label")
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.mac_label)
        self.mac_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.mac_name.setEnabled(False)
        self.mac_name.setObjectName("mac_name")
        self.form_layout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.mac_name)
        self.full_layout.addLayout(self.form_layout)
        self.checkbox_layout = QtWidgets.QHBoxLayout()
        self.checkbox_layout.setObjectName("checkbox_layout")
        self.auto_name = QtWidgets.QCheckBox(self.layoutWidget)
        self.auto_name.setChecked(True)
        self.auto_name.setObjectName("auto_name")
        self.checkbox_layout.addWidget(self.auto_name, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.full_layout.addLayout(self.checkbox_layout)
        self.full_layout.setStretch(0, 3)
        self.full_layout.setStretch(1, 1)

        self.retranslateUi(Dialog)
        self.button_box.accepted.connect(Dialog.accept) # type: ignore
        self.button_box.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Host"))
        self.switch_label.setText(_translate("Dialog", "Switch"))
        self.host_label.setText(_translate("Dialog", "Host Name"))
        self.mac_label.setText(_translate("Dialog", "MAC"))
        self.auto_name.setText(_translate("Dialog", "AutoFill Name"))
