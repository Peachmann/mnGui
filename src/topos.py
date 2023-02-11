"""
Class used for defining different starting topologies
"""
from mininet.topo import Topo
from mininet.node import Docker

class SingleSwitchTopo(Topo):

    def __init__(self):
        super().__init__()
        self.ids = {'dpid': 1, 'host': 2, 'mac': 2}

    def build(self):
        self.s1 = self.addSwitch('s1')

        h1 = self.addHost('h1', mac="00:00:00:00:11:11")
        h2 = self.addHost('h2', mac="00:00:00:00:11:12")

        self.addLink(h1, self.s1)
        self.addLink(h2, self.s1)

class DualSwitchTopo(Topo):

    def __init__(self):
        super().__init__()
        self.ids = {'dpid': 2, 'host': 3, 'mac': 3}
        
    def build(self):
        self.macs = {}
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1', mac="00:00:00:00:00:01")
        h2 = self.addHost('h2', mac="00:00:00:00:00:02")
        h3 = self.addHost('h3', mac="00:00:00:00:00:03")

        self.addLink(s1, s2)
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)

        # TODO Automate this
        self.macs["00:00:00:00:00:01"] = []
        self.macs["00:00:00:00:00:02"] = []
        self.macs["00:00:00:00:00:03"] = []

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
        #client2 = self.addHost('client2', cls=Docker, ip="10.0.0.3", mac="00:00:00:00:00:03", dimage="test_client:latest")
        
        self.addLink(client, s1)
        #self.addLink(client2, s1)
        self.addLink(s1, s2)
        self.addLink(server, s2)

        self.macs["00:00:00:00:00:01"] = {'host_type': 'Server', 'connected_to': ["00:00:00:00:00:02"]}
        self.macs["00:00:00:00:00:02"] = {'host_type': 'Client', 'connected_to': ["00:00:00:00:00:01"]}
        #self.macs["00:00:00:00:00:03"] = {'host_type': 'client', 'ip': '10.0.0.3', 'connected_to': []}

        self.switch_info['1'] = {'name': 's1', 'hosts': [("client", "00:00:00:00:00:02")]}
        self.switch_info['2'] = {'name': 's2', 'hosts': [("server", "00:00:00:00:00:01")]}


class PlainQuadSwitch(Topo):
    """
    Simple topology with 4 switches.
    Showcases that hosts can only reach allowed ones.

    " " " " " " " " " " " " " " " 
    "                s3         "
    "               /           "
    "    s1 ---- s2 --- s4      "
    "                           "
    " " " " " " " " " " " " " " "

    """

    def __init__(self):
        super().__init__()
        self.ids = {'dpid': 2, 'host': 0, 'mac': 0}
        self.macs = {}

    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s2, s4)