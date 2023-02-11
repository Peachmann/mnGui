"""
Class used for defining different starting topologies
"""
from mininet.topo import Topo
from mininet.node import Docker

class PlainDualSwitch(Topo):
    """
    Simple topology with 2 switches and 2 connected hosts.

    " " " " " " " " " " " " " " " 
    "                           "
    "  h1 --- s1 --- s2 --- h2  "
    "                           "
    " " " " " " " " " " " " " " "

    """

    def build(self):
        self.macs = {}
        self.switch_info = {}
        self.ids = {'dpid': 2, 'host': 2, 'mac': 2}
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        server = self.addHost('server', cls=Docker, mac="00:00:00:00:00:01", dcmd="python app.py", dimage="test_server:latest")
        client = self.addHost('client', cls=Docker, mac="00:00:00:00:00:02", dimage="test_client:latest")
        
        self.addLink(client, s1)
        self.addLink(s1, s2)
        self.addLink(server, s2)

        self.macs["00:00:00:00:00:01"] = {'host_type': 'Server', 'connected_to': ["00:00:00:00:00:02"]}
        self.macs["00:00:00:00:00:02"] = {'host_type': 'Client', 'connected_to': ["00:00:00:00:00:01"]}

        self.switch_info['1'] = {'name': 's1', 'hosts': [("client", "00:00:00:00:00:02")]}
        self.switch_info['2'] = {'name': 's2', 'hosts': [("server", "00:00:00:00:00:01")]}


class PlainQuadSwitch(Topo):
    """
    Simple topology with 4 switches.
    Client and server are NOT connected by default.

    " " " " " " " " " " " " " " " 
    "                s3 -- h2   "
    "                /          "
    "  h1 -- s1 --- s2 --- s4   "
    "                           "
    " " " " " " " " " " " " " " "

    """

    def build(self):
        self.ids = {'dpid': 4, 'host': 2, 'mac': 2}
        self.switch_info = {}
        self.macs = {}

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        client = self.addHost('client', cls=Docker, mac="00:00:00:00:00:01", dimage="test_client:latest")
        server = self.addHost('server', cls=Docker, mac="00:00:00:00:00:02", dcmd="python app.py", dimage="test_server:latest")
        
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s2, s4)
        self.addLink(client, s1)
        self.addLink(server, s3)

        self.macs["00:00:00:00:00:01"] = {'host_type': 'Client', 'connected_to': []}
        self.macs["00:00:00:00:00:02"] = {'host_type': 'Server', 'connected_to': []}

        self.switch_info['1'] = {'name': 's1', 'hosts': [("client", "00:00:00:00:00:01")]}
        self.switch_info['2'] = {'name': 's2', 'hosts': []}
        self.switch_info['3'] = {'name': 's3', 'hosts': [("server", "00:00:00:00:00:02")]}
        self.switch_info['4'] = {'name': 's4', 'hosts': []}