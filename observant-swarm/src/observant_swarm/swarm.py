"""
Observant Swarm Library
@author: Florian Delizy
@license: M.I.T.
"""

import threading
import ipaddress
import json

from typing import Tuple

import psutil

from .observant import Observant
from .discovery_server import DiscoveryServer
from .streaming_server import StreamingServer
from .echo_server import EchoServer
from .echo_request_queue import EchoRequestQueue

class SwarmWatcher: # pylint: disable=too-few-public-methods
    """
    wraps all callbacks from the Swarm
    - overides callbacks with your own.
    """

    def on_observant_connected(self, swarm, observant):
        """ called when an observant is connected to the swarm (first connection) """


class Swarm: #pylint: disable=too-many-instance-attributes,too-many-public-methods
    """ Swarm: manage the observants """

    def __init__(self, addr:Tuple[str, int], bcast:Tuple[str,int]=None, sports=(0xdead, 0xdeed)): #pylint: disable=too-many-arguments
        """
        Creates a swarm, listening on addr:port (as well as a discovery thread)
        @param addr (tuple (addr, port)): listening IP address (CIDR notation)
        @param bcast (tuple (addr, port)): UDP port to listen to

        """

        self.__addr = None
        self.__bcast = None
        self.__port = None
        self.__dport = None
        self.__multicast_address = ("224.0.0.1", 0xfee1)
        self.__streaming_server = None

        self.set_address(addr, bcast)


        self.__observants = {}
        self.__obs_lock = threading.Lock()

        self.__watchers = []
        self.__watch_lock = threading.Lock()

        self.__discovery_server = DiscoveryServer(self, (self.__bcast, self.__dport))
        self.__streaming_server = StreamingServer(self.__addr, sports)

        self.__sports = sports

        self.__streamers_lock = threading.Lock()
        self.__streamers = {}


        self.__echo_requests = {}
        self.__request_lock = threading.Lock()

        self.__echo_server = None
        self.__echo_server_lock = threading.Lock()


    def set_address(self, addr, bcast):
        """
        find the addr in the network list, check the broadcast
        """

        self.__addr = addr[0]
        self.__port = addr[1]
        if self.__streaming_server:
            self.__streaming_server.set_address(self.__addr)

        self.set_broadcast(bcast)

    def set_broadcast(self, bcast=None):
        """ set the broadcast, or find the right broadcast from the system """

        addr = None
        port = 0xfeed

        if bcast is not None:
            addr, port = bcast

        self.__dport = port

        if addr is not None:
            self.__bcast = addr
            return

        interfaces = psutil.net_if_addrs()
        myip = self.__addr

        for _, addrs in interfaces.items():
            # Iterate over the addresses for the interface
            for addr in addrs:
                # Check if the address is the one we're looking for
                if addr.address == myip:
                    netmask = addr.netmask
                    network = ipaddress.IPv4Network(myip + "/" + netmask, strict=False)
                    self.__bcast = str(network.network_address)
                    return

        self.__bcast = "0.0.0.0" # if not found, defaulting to all


    def streaming_range(self):
        """ return the streaming port range """
        return self.__sports

    def observants(self):
        """ return a list of observants """
        with self.__obs_lock:
            return self.__observants.values()

    def observant(self, hwid):
        """ get an observant by id """
        with self.__obs_lock:
            return self.__observants[hwid]


    def register_watcher(self, watcher):
        """ add a watcher to the list (thread safe) """
        with self.__watch_lock:
            self.__watchers.append(watcher)

    def _add_observant(self, obs):
        """
        - add an Observant
        - deduplicates
        - and notify watchers

        - takes ownership of the object
        """

        with self.__obs_lock:
            key = obs.uniqueID()
            if key in self.__observants:
                return
            self.__observants[key] = obs

        self.__notify_watchers("observant_connected", obs)


    def on_beacon(self, addr, beacon):
        """ called by the discover thread (in thread context) """

        hwid = beacon['id']
        obs = None
        new = False

        with self.__obs_lock:
            if hwid not in self.__observants:
                obs = Observant(self, addr, beacon)
                self.__observants[hwid] = obs
                new = True
            else:
                obs = self.__observants[hwid]

        obs.update_from_beacon(beacon)
        if new:
            self.__notify_watchers("observant_connected", obs)

        return obs

    def request_streaming(self, obs:Observant) -> int:
        """ return the port to stream on """
        hwid = obs.hwid()

        with self.__streamers_lock:
            if hwid not in self.__streamers:
                self.__streamers[hwid] = self.__streaming_server.allocate_client()
            return self.__streamers[hwid] # avoid duplicates


    def terminate_streaming(self, obs:Observant):
        """ close the streaming port for client """
        with self.__streamers_lock:
            port = self.__streamers[obs.hwid()]
            self.__streaming_server.close_client(port)
            del self.__streamers[obs.hwid()]

    def streamers(self):
        """ get the list of active streamers """
        ret = []
        with self.__obs_lock:
            with self.__streamers_lock:
                for hwid  in self.__streamers:
                    ret.append(self.__observants[hwid])
        return ret


    def __notify_watchers(self, name, *args):
        """ shortcut to notify all watchers """
        with self.__watch_lock:
            for watcher in self.__watchers:
                func = getattr(watcher, f"on_{name}")
                func(self, *args)

    def start_discovery(self):
        """ start the swarm management thread (async) """
        self.__discovery_server.start()

    def stop_discovery(self):
        """ stop the swarm management thread (async) """
        self.__discovery_server.shutdown()

    def is_discovering(self):
        """ True if the discovery thread is started """
        return self.__discovery_server.is_alive()

    def join(self):
        """ joins all the thread and quit """
        self.__discovery_server.join()

    def __str__(self):
        return f"SWARM[{self.__addr}:{self.__port}]"

    def address(self):
        """ return a an address tuple """
        return (self.__addr, self.__port)

    def multicast_address(self):
        """ return the multicast address and port """
        return self.__multicast_address

    def set_multicast_address(self, address):
        """ set the multicast address """
        self.__multicast_address = address

    def broadcast_address(self):
        """ return the broadcast address used for discovery """
        return (self.__bcast, self.__dport)

    def start_echo_server(self):
        """ start the echo reply server """
        with self.__echo_server_lock:
            if self.__echo_server is None:
                self.__echo_server = EchoServer(self, (self.__addr, self.__dport))

        self.__echo_server.start()

    def echo_request(self, position:Tuple[float, float, float], goals:dict, timeout=None):
        """ start a request, and returns on end of request goals.
        goals is a dict containing
        {
            'count': (int) returns when a number of count observant has responded (at least),
            'distance': (float) returns when at least one observant within distance responded,
            'xy-distance': (float) returns when at least one observant within distance responded,
            'elevation': (float) returns when at least one observant within distance responded,
        }
        goals are cumulative.
        """

        request = EchoRequestQueue(position, goals)
        request_id = request.request_id()

        with self.__request_lock:
            self.__echo_requests[request_id] = request

        self.start_echo_server()
        request.broadcast(self.__addr, self.__multicast_address)
        request.wait(timeout)

        self.stop_echo_server()

        with self.__request_lock:
            del self.__echo_requests[request_id]

        return request



    def stop_echo_server(self):
        """ stop the echo server """
        with self.__echo_server_lock:
            if self.__echo_server is not None:
                self.__echo_server.shutdown()
                self.__echo_server.join()
                self.__echo_server = None

    def echo_server_running(self):
        """ checks if the server is running """
        return self.__echo_server is not None and self.__echo_server.is_alive()

    def on_echo_reply(self, addr, data):
        """ get the info from reply to echo request """

        info = json.dumps(data, default=str, indent=4)
        print(f"got echo reply\n{info}")

        obs = self.on_beacon(addr, data) # echo-reply is also a beacon data

        request = None
        request_id = data['request_id']
        with self.__request_lock:
            request = self.__echo_requests.get(request_id)

        if request is None:
            print(f"WARNING: got echo-reply with unknown request {request_id}")
            return

        request.on_echo_reply(obs, data)


# vim: set sw=4 expandtab ts=4 ai cindent:
