# Form implementation generated from reading ui file '/home/peach/Uni/mnGui/src/ui/remove_host_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 172)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.full_layout = QtWidgets.QVBoxLayout()
        self.full_layout.setObjectName("full_layout")
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.form_layout.setObjectName("form_layout")
        self.host_label = QtWidgets.QLabel(Dialog)
        self.host_label.setObjectName("host_label")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.host_label)
        self.host_box = QtWidgets.QComboBox(Dialog)
        self.host_box.setObjectName("host_box")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.host_box)
        self.mac_label = QtWidgets.QLabel(Dialog)
        self.mac_label.setObjectName("mac_label")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.mac_label)
        self.mac_name = QtWidgets.QLineEdit(Dialog)
        self.mac_name.setEnabled(False)
        self.mac_name.setObjectName("mac_name")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.mac_name)
        self.full_layout.addLayout(self.form_layout)
        self.full_layout.setStretch(0, 3)
        self.gridLayout.addLayout(self.full_layout, 0, 0, 1, 1)
        self.button_box = QtWidgets.QDialogButtonBox(Dialog)
        self.button_box.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.button_box.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.button_box.accepted.connect(Dialog.accept) # type: ignore
        self.button_box.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Remove Host"))
        self.host_label.setText(_translate("Dialog", "Host Name"))
        self.mac_label.setText(_translate("Dialog", "MAC"))
