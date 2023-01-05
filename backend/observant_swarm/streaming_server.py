"""
Audio Streaming Server
"""

#import threading
import gi
gi.require_version("Gst", "1.0")

from gi.repository import Gst #pylint: disable=wrong-import-position


class StreamingServer:#(threading.Thread):
    """ GStreamer streaming server wrapper:
        - allow add/remove new sources
    """

    inited = False

    @staticmethod
    def global_init():
        """ ensure gi is property inited at start """
        if StreamingServer.inited:
            return

        Gst.init(None)
        StreamingServer.inited = True

    def __init__(self, address, port_range=(5000,6000), sink='autoaudiosink'):
        StreamingServer.global_init()

        #super().__init__(name="observant-swarm streamer")
        self.__port_range = port_range
        self.__address = address

        self.__pipeline = Gst.parse_launch(f'audiomixer name=entrypoint ! audioconvert ! {sink}')
        self.__sink = self.__pipeline.get_by_name('entrypoint')

        self.__clients = {}

    def set_address(self, addr):
        """ set the address to listen to """
        self.__address = addr


    def _find_port(self):
        """ get the next avail port """
        for port in range(*self.__port_range):
            if port not in self.__clients:
                return port
        return None

    def allocate_client(self) -> int:
        """ create a new source/port for the client and return it """

        port = self._find_port()
        desc = f'udpsrc address={self.__address} port={port} caps="application/x-rtp" '\
                '! rtpjitterbuffer latency=10 ! rtppcmudepay ! mulawdec'

        source = Gst.parse_bin_from_description(desc, True)

        self.__pipeline.add(source)

        self.__sink.request_pad_simple(f"sink_{port}")
        source.link(self.__sink)
        source.set_state(Gst.State.PLAYING)
        self.__pipeline.set_state(Gst.State.PLAYING)

        self.__clients[port] = source
        return port

    def close_client(self, port:int):
        """ remove the port """
        source = self.__clients[port]
        source.set_state(Gst.State.NULL)
        self.__pipeline.remove(source)
        self.__sink.remove_pad(self.__sink.get_static_pad(f'sink_{port}'))
        del self.__clients[port]

        if not self.__clients:
            self.__pipeline.set_state(Gst.State.NULL)
