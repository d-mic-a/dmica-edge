"""
Handles Echo Reply
"""

from .discovery_server import DiscoveryServer, DiscoveryHandler


class EchoHandler(DiscoveryHandler):
    """ handle echo requests only """

    def dispatch(self, data):
        """ dispatch the incoming packet """

        packet_type = data['type']
        swarm = self.swarm()
        addr, _ = self.client_address

        if packet_type == 'echo-reply':
            swarm.on_echo_reply(addr, data)
            return

class EchoServer(DiscoveryServer):
    """ echo server class (feed the Handler/name class)"""

    name = "observant-echo"
    handler_class = EchoHandler
