from PyQt6.QtCore import QThread, pyqtSignal
import gevent.pywsgi
import gevent.queue
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.wsgi import WsgiServerTransport
from tinyrpc.server.gevent import RPCServerGreenlets
from tinyrpc.dispatch import RPCDispatcher
import json

class RPCThread(QThread):
    """
    Thread resposible for recieving topology discovery data.
    """
    create_flow_signal = pyqtSignal(dict)
    remove_flow_signal = pyqtSignal(dict)
    get_allowed_connections = pyqtSignal()

    def __init__(self,  parent=None):
        QThread.__init__(self, parent)
        self.rpc_server = None
        self.wsgi_server = None
        self.dispatcher = RPCDispatcher()
        self.allowed_connections = {}

    def run(self):
        
        transport = WsgiServerTransport(queue_class=gevent.queue.Queue)

        self.wsgi_server = gevent.pywsgi.WSGIServer(('127.0.0.1', 5000), transport.handle)
        gevent.spawn(self.wsgi_server.start())

        self.rpc_server = RPCServerGreenlets(transport, JSONRPCProtocol(), self.dispatcher)

        @self.dispatcher.public
        def process_flow_data(value):
            
            flow_data = json.loads(value)

            dpid = flow_data['dpid']
            source = None
            destination = None
            in_port = None
            out_port = None

            for match in flow_data['OFPFlowMod']['match']['OFPMatch']['oxm_fields']:
                value = match['OXMTlv']['value']
                field = match['OXMTlv']['field']

                if field == 'eth_dst':
                    destination = value
                    continue
                
                if field == 'eth_src':
                    source = value
                    continue

                if field == 'in_port':
                    in_port = value
                    continue
                

            for action in flow_data['OFPFlowMod']['instructions'][0]['OFPInstructionActions']['actions']:
                if 'OFPActionOutput' in action:
                    out_port = action['OFPActionOutput']['port']

            self.get_allowed_connections.emit()

            if destination in self.allowed_connections[source]:
                create_json = {
                    "dpid": dpid,
                    "priority": 1,
                    "match":{
                        "in_port": in_port,
                        "dl_dst": destination,
                        "dl_src": source
                    },
                    "actions":[
                        {
                            "type": "OUTPUT",
                            "port": out_port
                        }
                    ]
                }

                self.create_flow_signal.emit(create_json)
                print(f"Added flow in switch DPID {dpid} from {source} to {destination} (Ports: {in_port} -> {out_port})")
            else:
                print("Communication is not allowed between these containers!")

            return "Response."

        self.rpc_server.serve_forever()

    def add_connection(self, src, dst):
        print(" xddddddddd vdvsdds")
        return

    def remove_connection(self, src, dst):
        return