# Form implementation generated from reading ui file '/home/peach/Uni/mnGui/src/ui/manage_flows.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(374, 329)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.full_layout = QtWidgets.QVBoxLayout()
        self.full_layout.setObjectName("full_layout")
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.form_layout.setHorizontalSpacing(20)
        self.form_layout.setObjectName("form_layout")
        self.switch_label = QtWidgets.QLabel(Dialog)
        self.switch_label.setObjectName("switch_label")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.switch_label)
        self.switch_box = QtWidgets.QComboBox(Dialog)
        self.switch_box.setObjectName("switch_box")
        self.form_layout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.switch_box)
        self.switch_name_label_2 = QtWidgets.QLabel(Dialog)
        self.switch_name_label_2.setObjectName("switch_name_label_2")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.switch_name_label_2)
        self.flow_list = QtWidgets.QListWidget(Dialog)
        self.flow_list.setObjectName("flow_list")
        self.form_layout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.flow_list)
        self.full_layout.addLayout(self.form_layout)
        self.full_layout.setStretch(0, 3)
        self.gridLayout.addLayout(self.full_layout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.add_flow_button = QtWidgets.QPushButton(Dialog)
        self.add_flow_button.setObjectName("add_flow_button")
        self.horizontalLayout_2.addWidget(self.add_flow_button)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.button_box = QtWidgets.QDialogButtonBox(Dialog)
        self.button_box.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.button_box.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.button_box.setCenterButtons(True)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 8, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.button_box.accepted.connect(Dialog.accept) # type: ignore
        self.button_box.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "View Flows"))
        self.switch_label.setText(_translate("Dialog", "Switch"))
        self.switch_name_label_2.setText(_translate("Dialog", "Flow List"))
        self.add_flow_button.setText(_translate("Dialog", "Add Flow"))
