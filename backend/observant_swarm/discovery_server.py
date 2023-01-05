"""
Discovery: listen to observant beacons
"""

import socketserver
import json
import threading

class DiscoveryHandler(socketserver.BaseRequestHandler):
    """ Observant Discovery server, start listenning and wait for beacons"""

    def swarm(self):
        """ shortcut """
        return self.server.swarm

    def handle(self):
        """ handle a request (one instance per request) """
        raw_data = self.request[0].strip()
        addr, _ = self.client_address
        name = self.server.name

        if not raw_data:
            print(f"{name}: invalid raw data from {addr} skipping)")
            return

        try:
            data = json.loads(raw_data)
        except json.decoder.JSONDecodeError as exc:
            print(f"{name}: got invalid JSON packet from {addr}: {exc}")
            return

        if 'id' not in data or 'type' not in data:
            print(f"{name}: invalid JSON beacon/echo from {addr}: {data:r}")

        self.dispatch(data)


    def dispatch(self, data):
        """ dispatch the incoming packet """
        packet_type = data['type']
        swarm = self.swarm()
        addr, _ = self.client_address

        if packet_type == 'beacon':
            swarm.on_beacon(addr, data)
            return

        print(f"unsupported async {packet_type} packet received")



class DiscoveryServer(socketserver.UDPServer, threading.Thread):
    """ server, binds the port, handle the low level protocol (UDP), binds the handler """

    name = "observant-discovery"
    handler_class = DiscoveryHandler

    def __init__(self, swarm, server_address):

        socketserver.UDPServer.__init__(self, server_address, self.handler_class)
        threading.Thread.__init__(self, name=self.name)

        self.swarm = swarm
        self.daemon = True

    def run(self):
        """ run the thread till the stop is requested """
        self.serve_forever()

    # def verify_request(request, client_address):
    #     """ overriden """
    #     return True
