# Form implementation generated from reading ui file '/home/peach/Uni/mnGui/src/ui/main_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.central_widget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy)
        self.central_widget.setObjectName("central_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(-1, -1, 0, -1)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName("main_layout")
        self.sidebar_frame = QtWidgets.QFrame(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidebar_frame.sizePolicy().hasHeightForWidth())
        self.sidebar_frame.setSizePolicy(sizePolicy)
        self.sidebar_frame.setMinimumSize(QtCore.QSize(0, 92))
        self.sidebar_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.sidebar_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.sidebar_frame.setObjectName("sidebar_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.sidebar_frame)
        self.verticalLayout.setSpacing(23)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sidebar_layout = QtWidgets.QVBoxLayout()
        self.sidebar_layout.setObjectName("sidebar_layout")
        self.topology_label = QtWidgets.QLabel(self.sidebar_frame)
        self.topology_label.setObjectName("topology_label")
        self.sidebar_layout.addWidget(self.topology_label, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.create_helper = QtWidgets.QTabWidget(self.sidebar_frame)
        self.create_helper.setObjectName("create_helper")
        self.tab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.tab.setToolTip("")
        self.tab.setToolTipDuration(-1)
        self.tab.setStatusTip("")
        self.tab.setAutoFillBackground(False)
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.button_layout = QtWidgets.QVBoxLayout()
        self.button_layout.setSpacing(0)
        self.button_layout.setObjectName("button_layout")
        self.add_host_button = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_host_button.sizePolicy().hasHeightForWidth())
        self.add_host_button.setSizePolicy(sizePolicy)
        self.add_host_button.setObjectName("add_host_button")
        self.button_layout.addWidget(self.add_host_button)
        self.remove_host_button = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_host_button.sizePolicy().hasHeightForWidth())
        self.remove_host_button.setSizePolicy(sizePolicy)
        self.remove_host_button.setObjectName("remove_host_button")
        self.button_layout.addWidget(self.remove_host_button)
        self.gridLayout_2.addLayout(self.button_layout, 0, 0, 1, 1)
        self.create_helper.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_2.sizePolicy().hasHeightForWidth())
        self.tab_2.setSizePolicy(sizePolicy)
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.button_layout_2 = QtWidgets.QVBoxLayout()
        self.button_layout_2.setSpacing(0)
        self.button_layout_2.setObjectName("button_layout_2")
        self.add_switch_button = QtWidgets.QPushButton(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_switch_button.sizePolicy().hasHeightForWidth())
        self.add_switch_button.setSizePolicy(sizePolicy)
        self.add_switch_button.setObjectName("add_switch_button")
        self.button_layout_2.addWidget(self.add_switch_button)
        self.remove_switch_button = QtWidgets.QPushButton(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_switch_button.sizePolicy().hasHeightForWidth())
        self.remove_switch_button.setSizePolicy(sizePolicy)
        self.remove_switch_button.setObjectName("remove_switch_button")
        self.button_layout_2.addWidget(self.remove_switch_button)
        self.gridLayout_3.addLayout(self.button_layout_2, 0, 0, 1, 1)
        self.create_helper.addTab(self.tab_2, "")
        self.sidebar_layout.addWidget(self.create_helper)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.sidebar_layout.addItem(spacerItem)
        self.flows_label = QtWidgets.QLabel(self.sidebar_frame)
        self.flows_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.flows_label.setObjectName("flows_label")
        self.sidebar_layout.addWidget(self.flows_label, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.add_flow_btn = QtWidgets.QPushButton(self.sidebar_frame)
        self.add_flow_btn.setEnabled(False)
        self.add_flow_btn.setObjectName("add_flow_btn")
        self.sidebar_layout.addWidget(self.add_flow_btn)
        self.remove_flow_btn = QtWidgets.QPushButton(self.sidebar_frame)
        self.remove_flow_btn.setEnabled(False)
        self.remove_flow_btn.setObjectName("remove_flow_btn")
        self.sidebar_layout.addWidget(self.remove_flow_btn)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.sidebar_layout.addItem(spacerItem1)
        self.refresh_button = QtWidgets.QPushButton(self.sidebar_frame)
        self.refresh_button.setObjectName("refresh_button")
        self.sidebar_layout.addWidget(self.refresh_button)
        self.sidebar_layout.setStretch(1, 2)
        self.sidebar_layout.setStretch(2, 2)
        self.sidebar_layout.setStretch(5, 1)
        self.verticalLayout.addLayout(self.sidebar_layout)
        self.main_layout.addWidget(self.sidebar_frame)
        self.canvas_widget = CanvasWidget(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas_widget.sizePolicy().hasHeightForWidth())
        self.canvas_widget.setSizePolicy(sizePolicy)
        self.canvas_widget.setObjectName("canvas_widget")
        self.main_layout.addWidget(self.canvas_widget)
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 3)
        self.gridLayout.addLayout(self.main_layout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAdd_Host = QtGui.QAction(MainWindow)
        self.actionAdd_Host.setObjectName("actionAdd_Host")

        self.retranslateUi(MainWindow)
        self.create_helper.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.topology_label.setText(_translate("MainWindow", "Topology"))
        self.add_host_button.setText(_translate("MainWindow", "Add Host"))
        self.remove_host_button.setText(_translate("MainWindow", "Remove Host"))
        self.create_helper.setTabText(self.create_helper.indexOf(self.tab), _translate("MainWindow", "Host"))
        self.add_switch_button.setText(_translate("MainWindow", "Add Switch"))
        self.remove_switch_button.setText(_translate("MainWindow", "Remove Switch"))
        self.create_helper.setTabText(self.create_helper.indexOf(self.tab_2), _translate("MainWindow", "Switch"))
        self.flows_label.setText(_translate("MainWindow", "Flows"))
        self.add_flow_btn.setText(_translate("MainWindow", "Add Flow"))
        self.remove_flow_btn.setText(_translate("MainWindow", "Remove Flow"))
        self.refresh_button.setText(_translate("MainWindow", "Refresh"))
        self.actionAdd_Host.setText(_translate("MainWindow", "Add Host"))
from .canvas_widget import CanvasWidget
