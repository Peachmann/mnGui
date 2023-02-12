import sys
import requests
import logging
import re
from dialogs import AddHostDialog, AddSwitchDialog, RemoveHostDialog, RemoveSwitchDialog, ManageFlowsDialog
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from json import JSONDecodeError
from mininet_thread import MininetThread

from ui.ui_main_window import Ui_MainWindow

sys.path.append(".")

RYU_URL = 'http://0.0.0.0:8080/'
VERSION = '0.1'

LINKS_URL = RYU_URL + 'v1.0/topology/links'
SWITCHES_URL = RYU_URL + 'v1.0/topology/switches'
HOSTS_URL = RYU_URL + 'v1.0/topology/hosts'
GET_FLOWS_URL = RYU_URL + 'stats/flow/'

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main Window handling core app.
    """

    # Setup logging
    logger = logging.getLogger('Main')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    add_host_signal = pyqtSignal(dict)
    remove_host_signal = pyqtSignal(str)
    add_switch_signal = pyqtSignal(dict)
    remove_switch_signal = pyqtSignal(str, str, dict)

    ids = {'dpid': 0, 'host': 0, 'mac': 0}
    links = {}
    switches = {}
    hosts = {}
    switch_info = {}

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(F"MnGUI v{VERSION}")

        # Setup Mininet Thread with required Slots and Signals
        self.mininet_thread = MininetThread(parent=self)
        self.mininet_thread.refresh_topology_signal.connect(self.refresh_topology)
        self.mininet_thread.update_ids_signal.connect(self.update_ids)
        self.add_host_signal.connect(self.mininet_thread.add_host)
        self.remove_host_signal.connect(self.mininet_thread.remove_host)
        self.add_switch_signal.connect(self.mininet_thread.add_switch)
        self.remove_switch_signal.connect(self.mininet_thread.remove_switch)
        self.mininet_thread.start()

        # Setup API Slots and Signals
        self.add_host_button.clicked.connect(self.load_add_host_dialog)
        self.remove_host_button.clicked.connect(self.load_remove_host_dialog)
        self.add_switch_button.clicked.connect(self.load_add_switch_dialog)
        self.remove_switch_button.clicked.connect(self.load_remove_switch_dialog)
        self.manage_flow_btn.clicked.connect(self.load_manage_flows_dialog)
        self.refresh_button.clicked.connect(self.refresh_topology)

    def load_add_host_dialog(self):
        dialog = AddHostDialog(self)
        dialog.init_selections(self.switches, self.ids)

        if dialog.exec():
            new_host = {}
            new_host['name'] = dialog.ui.host_name.text()
            new_host['mac'] = dialog.ui.mac_name.text()
            new_host['switch'] = dialog.ui.switch_box.currentText()

            for _, value in self.switch_info.items():
                if value['name'] == new_host['switch']:
                    value['hosts'].append((new_host['name'], new_host['mac']))

            self.add_host_signal.emit(new_host)
            self.logger.info("Adding host.")
        else:
            self.logger.info("Canceled add host process.")

    def load_remove_host_dialog(self):
        dialog = RemoveHostDialog(self)
        dialog.init_hosts_and_macs(self.hosts)
        
        if dialog.exec():
            mac = dialog.ui.mac_name.text()
            for _, value in self.switch_info.items():
                for connection in value['hosts']:
                    if connection[1] == mac:
                        value['hosts'].remove(connection)
                    break

            self.remove_host_signal.emit(dialog.ui.host_box.currentText())
            self.logger.info("Removed host.")
        else:
            self.logger.info("Canceled remove host process.")

    def load_add_switch_dialog(self):
        dialog = AddSwitchDialog(self)
        dialog.init_selections(self.switches, self.ids)

        if dialog.exec():
            new_switch = {}
            new_switch['link_to'] = [switch.text() for switch in dialog.ui.switch_list.selectedItems()]
            new_switch['name'] = dialog.ui.switch_name.text()
            new_switch['dpid'] = dialog.ui.dpid_name.text()
            self.switch_info[new_switch['dpid']] = {'name': new_switch['name'], 'hosts': []}
            self.add_switch_signal.emit(new_switch)
            self.logger.info("Adding switch.")
        else:
            self.logger.info("Canceled add switch process.")

    def load_remove_switch_dialog(self):
        dialog = RemoveSwitchDialog(self)
        dialog.init_ui(self.switches)

        if dialog.exec():
            copy = self.switch_info.copy()
            self.switch_info.pop(dialog.ui.dpid_name.text())
            self.remove_switch_signal.emit(dialog.ui.switch_box.currentText(), dialog.ui.dpid_name.text(), copy)
            self.logger.info("Removed switch.")
        else:
            self.logger.info("Canceled remove switch process.")

    def load_manage_flows_dialog(self):
        dialog = ManageFlowsDialog(self)
        dialog.init_ui(self.switches)
        dialog.get_flow_signal.connect(self.get_flow_request)

        if dialog.exec():
            self.logger.info("Managed flows.")
        else:
            self.logger.info("Canceled flow management process.")

    @pyqtSlot(str, object)
    def get_flow_request(self, dpid, dialog):
        response = requests.get(GET_FLOWS_URL + dpid)
        dialog.update_flow_box(response.json()[dpid])

    @pyqtSlot(dict, dict)
    def update_ids(self, ids, sw_info):
        self.ids.update(ids)
        self.switch_info.update(sw_info)

    @pyqtSlot()
    def refresh_topology(self):
        self.switches.clear()
        self.hosts.clear()
        self.links.clear()
        self.switches, self.hosts, self.links = self.get_full_topology()

        for switch in self.switches:
            port_name = switch['ports'][0]['name']
            switch['name'] = re.findall("([-.\w]+)-eth[\d]+", port_name)[0]

            current_dpid = int(switch['dpid'])
            if current_dpid == self.ids['dpid']:
                self.ids['dpid'] += 1

        # Add names of hosts for detailed view
        host_names = {}
        for host in self.mininet_thread.net.hosts:
            host_names[host.MAC()] = host.name
            
            try:
                current_mac = int(str(host.MAC()).rsplit(':', 1)[-1])
                if current_mac == self.ids['mac']:
                    self.ids['mac'] += 1
            except:
                self.logger.info("Dropped leftover host.")

        for host in self.hosts:
            name = host_names.get(host['mac'])
            host['name'] = name

        # Remove leftovers not picked up by RYU
        to_remove = []
        for host in self.hosts:
            if host['name'] is None:
                to_remove.append(host)

        for host in to_remove:
            self.hosts.remove(host)

        self.canvas_widget.networkPlot(self.switches, self.hosts, self.links)
        self.logger.info("Topology updated.")

    @pyqtSlot()
    def get_full_topology(self):
        links = requests.get(LINKS_URL)
        switches = requests.get(SWITCHES_URL)
        hosts = requests.get(HOSTS_URL)

        try:
            links_dict = links.json()
            switches_dict = switches.json()
            hosts_dict = hosts.json()
        except JSONDecodeError:
            self.logger.error('Response could not be serialized')

        return switches_dict, hosts_dict, links_dict

    def closeEvent(self, event):
        try:
            self.logger.info('Killing Mininet thread')
            if self.mininet_thread.isRunning():
                self.mininet_thread.net.stop()
                self.mininet_thread.quit()

        except Exception as ex_quit:
            self.logger.exception(ex_quit)

class MnGui():
    """
    Driver function.
    """

    def __init__(self, *args, **kwargs):
        super(MnGui, self).__init__(*args, **kwargs)
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        sys.exit(app.exec())

MnGui()