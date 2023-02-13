"""
Classes handling the setup of dialogs (windows which handle user input).
Initialize selections with correct data and connect slots (if it's the case).
"""

from PyQt6.QtWidgets import QDialog, QListWidgetItem, QWidget, QDialogButtonBox
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from ui.ui_flow_details_dialog import Ui_Dialog as FlowDetailsWidget
from ui.ui_add_host_dialog import Ui_Dialog as AddHostDialogUi
from ui.ui_add_switch_dialog import Ui_Dialog as AddSwitchDialogUi
from ui.ui_remove_host_dialog import Ui_Dialog as RemoveHostDialogUi
from ui.ui_remove_switch_dialog import Ui_Dialog as RemoveSwitchDialogUi
from ui.ui_manage_flows import Ui_Dialog as ManageFlowsUi
from ui.ui_add_flow_dialog import Ui_Dialog as AddFlowDialogUi

class AddHostDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = AddHostDialogUi()
        self.ui.setupUi(self)
        self.ui.auto_name.stateChanged.connect(self.update_host_name_field)
        self.mac = 0


    def init_selections(self, switches, ids):
        for switch in switches:
            self.ui.switch_box.addItem(switch['name'])
        
        self.mac = ids['mac']
        if self.mac < 10:
            self.mac = f"0{ids['mac']}" 
            
        self.ui.mac_name.setText(f"00:00:00:00:00:{self.mac}")
        self.update_host_name_field()

    def update_host_name_field(self):
        if self.ui.auto_name.isChecked():
            self.ui.host_name.setEnabled(False)
            self.ui.host_name.setText(f"h{self.mac}")
        else:
            self.ui.host_name.setEnabled(True)
            self.ui.host_name.clear()

class RemoveHostDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = RemoveHostDialogUi()
        self.ui.setupUi(self)
        self.host_and_mac_dict = {}
    
    def init_hosts_and_macs(self, hosts):
        for host in hosts:
            self.ui.host_box.addItem(host['name'])
            self.host_and_mac_dict[host['name']] = host['mac']
        self.ui.host_box.currentTextChanged.connect(self.update_mac)
        self.update_mac()

    def update_mac(self):
        selected_host = self.ui.host_box.currentText()
        self.ui.mac_name.setText(self.host_and_mac_dict[selected_host])

class AddSwitchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = AddSwitchDialogUi()
        self.ui.setupUi(self)
        self.dpid = 0

    def init_selections(self, switches, ids):
        for switch in switches:
            self.ui.switch_list.addItem(QListWidgetItem(switch['name']))
        
        self.dpid = ids['dpid']
        self.ui.dpid_name.setText(str(self.dpid))
        self.update_switch_name_field()
        self.ui.auto_name.stateChanged.connect(self.update_switch_name_field)

    def update_switch_name_field(self):
        if self.ui.auto_name.isChecked():
            self.ui.switch_name.setEnabled(False)
            self.ui.switch_name.setText(f"s{self.dpid}")
        else:
            self.ui.switch_name.setEnabled(True)
            self.ui.switch_name.clear()

class RemoveSwitchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = RemoveSwitchDialogUi()
        self.ui.setupUi(self)
        self.switch_and_dpid_dict = {}

    def init_ui(self, switches):
        for switch in switches:
            self.ui.switch_box.addItem(switch['name'])
            self.switch_and_dpid_dict[switch['name']] = str(int(switch['dpid']))

        self.ui.switch_box.currentTextChanged.connect(self.update_dpid)
        self.update_dpid()

    def update_dpid(self):
        selected = self.ui.switch_box.currentText()
        self.ui.dpid_name.setText(self.switch_and_dpid_dict[selected])

class ManageFlowsDialog(QDialog):
    get_flow_signal = pyqtSignal(str, object)
    delete_flow_signal = pyqtSignal(dict)
    add_flow_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = ManageFlowsUi()
        self.ui.setupUi(self)
        self.switch_and_dpid_dict = {}
        self.detail_widget = FlowDetails(self)
        self.add_flow_dialog = AddFlow(self)
        self.hosts = {}
        

    def get_flows(self, name):
        self.get_flow_signal.emit(self.switch_and_dpid_dict[name], self)

    def init_ui(self, switches):
        for switch in switches:
            self.ui.switch_box.addItem(switch['name'])
            self.switch_and_dpid_dict[switch['name']] = str(int(switch['dpid']))
        
        self.ui.switch_box.currentTextChanged.connect(self.get_flows)
        self.ui.flow_list.itemDoubleClicked.connect(self.display_flow_details)
        self.ui.add_flow_button.clicked.connect(self.init_add_flow)

    def update_flow_box(self, flows):
        self.ui.flow_list.clear()
        flow_id = 1
        for flow in flows:
            title = 'Flow ' + str(flow_id) + ' -> ' + flow['actions'][0]
            flow_id += 1
            item = QListWidgetItem(title)
            item.setData(1, flow)
            self.ui.flow_list.addItem(item)

    def display_flow_details(self, item):
        flow = item.data(1)
        self.detail_widget.ui.actions_box.setText(str(flow['actions']))
        self.detail_widget.ui.match_box.setText(str(flow['match']))
        self.detail_widget.ui.table_text.setText(str(flow['table_id']))
        self.detail_widget.ui.priority_text.setText(str(flow['priority']))
        
        if self.detail_widget.exec():
            req = {'dpid': self.switch_and_dpid_dict[self.ui.switch_box.currentText()],
                'match': flow['match']}
            
            self.delete_flow_signal.emit(req)
            self.get_flows(self.ui.switch_box.currentText())
            print("Deleted flow.")

    def init_add_flow(self):
        mac = self.switch_and_dpid_dict[self.ui.switch_box.currentText()]
        ui = self.add_flow_dialog.ui
        ui.dpid_text.setText(mac)
        ui.destination_box.clear()
        ui.source_box.clear()
        
        for host in self.hosts:
            ui.source_box.addItem(host['mac'])
            ui.destination_box.addItem(host['mac'])

        if self.add_flow_dialog.exec():
            req = {
                'dpid': mac,
                'priority': ui.priority_box.text(),
                'match': {
                    'in_port': ui.in_port_box.text(),
                    'dl_dst': ui.destination_box.currentText(),
                    'dl_src': ui.source_box.currentText()
                },
                'actions': [
                    {
                        'type': 'OUTPUT',
                        'port': ui.out_port_box.text()
                    }
                ]
            }
            
            self.add_flow_signal.emit(req)
            self.get_flows(self.ui.switch_box.currentText())
            print("Added flow.")
    
class FlowDetails(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = FlowDetailsWidget()
        self.ui.setupUi(self)
        self.ui.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Delete Flow")


class AddFlow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = AddFlowDialogUi()
        self.ui.setupUi(self)

    