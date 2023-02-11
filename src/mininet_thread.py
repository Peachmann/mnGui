from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

from mininet.net import Containernet
from topos import PlainDualSwitch
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.node import Docker


class MininetThread(QThread):
    """
    The thread which is responsible for running Mininet.
    The topology modifying functions are also here.

    The ping command after the topology modification is needed because
    RYU API does not automatically pick up the host topology change.
    As a consequence, at least 2 hosts always need to be present in the topology.
    """

    refresh_topology_signal = pyqtSignal()
    update_ids_signal = pyqtSignal(dict, dict, dict)
    forward_response = pyqtSignal(str)
    remove_connections_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.topo = PlainDualSwitch()
        c1 = RemoteController('c1')
        self.net = Containernet(topo=self.topo, controller=c1)

    def run(self):
        self.update_ids_signal.emit(self.topo.ids, self.topo.macs, self.topo.switch_info)
        self.net.start()
        self.net.pingAll(timeout=1)
        self.refresh_topology_signal.emit()
        CLI(self.net)


    @pyqtSlot(dict)
    def execute_command(self, values):
        client_name = values['client']
        server_ip = values['server']
        to_hash = values['to_hash']

        client = self.net.get(client_name)
        res = client.cmd(f"curl --connect-timeout 1 {server_ip}/hash/{to_hash}")
        self.forward_response.emit(res)


    @pyqtSlot(dict)
    def add_host(self, values):
        """
        Add host based on values selected in the dialog by the user.
        """

        host_name = values.get('name')
        host_mac = values.get('mac')
        switch = self.net.get(values.get('switch'))
        host_type = values.get('host_type')
        new_host = None

        if host_type == 'Server':
            new_host = self.net.addHost(host_name, cls=Docker, mac=host_mac, dcmd="python app.py", dimage="test_server:latest")
        else:
            new_host = self.net.addHost(host_name, cls=Docker, mac=host_mac, dimage="test_client:latest")
        
        new_link = self.net.addLink(new_host, switch)
        switch.attach(new_link.intf2)

        if new_host.defaultIntf():
            new_host.configDefault()

        self.net.ping([new_host, self.net.hosts[0]], timeout=1)
        self.msleep(500)

        self.refresh_topology_signal.emit()

    @pyqtSlot(str)
    def remove_host(self, host_name):
        host_node = self.net.get(host_name)
        self.net.delHost(host_node)
        self.net.ping([self.net.hosts[0], self.net.hosts[1]], timeout=1)
        self.msleep(500)
        self.refresh_topology_signal.emit()

    @pyqtSlot(dict)
    def add_switch(self, values):
        new_switch = self.net.addSwitch(values['name'], dpid=values['dpid'])

        for switch_name in values['link_to']:
            switch = self.net.get(switch_name)
            link = self.net.addLink(switch, new_switch)
            switch.attach(link.intf1)

        new_switch.start(self.net.controllers)

        self.msleep(500)
        self.refresh_topology_signal.emit()

    @pyqtSlot(str, str, dict)
    def remove_switch(self, switch_name, dpid, switch_info):
        switch_node = self.net.get(switch_name)
        hosts_to_delete = switch_info[dpid]['hosts']

        for host in hosts_to_delete:
            self.remove_connections_signal.emit(host[1])
            host_node = self.net.get(host[0])
            self.net.delHost(host_node)

        self.net.delSwitch(switch_node)
        self.net.ping([self.net.hosts[0], self.net.hosts[1]], timeout=1)
        self.msleep(500)
        self.refresh_topology_signal.emit()
