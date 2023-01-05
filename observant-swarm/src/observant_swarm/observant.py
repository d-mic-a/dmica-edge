"""
Observant Swarm Library: Observant Class
@author: Florian Delizy
@license: M.I.T.
"""

import json
import socket

STREAMING = "streaming"
IDLE = "idle"

class Observant: #pylint: disable=too-many-instance-attributes
    """ Swarm: manage the observants """

    def __init__(self, swarm, address, beacon):
        self.__position = (0, 0, 0) # x,y,z
        self.__hwid = None
        self.__address = address
        self.__port = 0xfee1    #default obs port for commands
        self.__swarm = swarm
        self.__lit = False

        self.__streaming_port = None
        self.update_from_beacon(beacon, force=True)

        self.__protocol = None

    def update_from_beacon(self, beacon, force=False):
        """ update from beacon data (if force, update the hwid)"""
        data = beacon
        if isinstance(data, str):
            data = json.loads(beacon)

        if not isinstance(data, dict) or 'id' not in data:
            raise ValueError("Invalid Beacon data")

        if data['id'] != self.__hwid:
            if not force:
                raise KeyError(
                        f"invalid hw id, expected {self.__hwid} but found {data[id]} instead"
                )
            self.__hwid = data['id']

        self.__position = data['position']
        self.__port = data['port']
        self.__lit = data['lit']

    def address(self):
        """ get the address """
        return self.__address

    def port(self):
        """ get the port """
        return self.__port


    def position(self) -> tuple:
        """ get the position of the observant """
        return self.__position

    def hwid(self):
        """ get the hwid """
        return self.__hwid

    def _send_command(self, cmd):
        """ send a command to the observer and gets the result """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = json.dumps(cmd)

        sock.sendto(bytes(data, "utf-8"), (self.__address, self.__port))

        ret = sock.recv(4096<<10) # commands are small, except list_commands
        return json.loads(ret)


    def send_command(self, cmd, **kwargs):
        """ send a command to the observer """

        spec = self.get_command_spec(cmd)['args_spec']
        args = None

        if spec:
            args = {}
            for key, cls in spec.items():
                if key not in kwargs:
                    raise ValueError(f"missing argument {key}")
                try:
                    args[key] = cls(kwargs[key])
                except ValueError as exc:
                    raise ValueError(
                        f"invalid value {kwargs[key]} for arg {key} expected type {cls.__name__}",
                    ) from exc

        return self._send_command({'cmd': cmd, 'args': args})


    def _list_protocol(self):
        """ list the protocol and saves the description """
        # list-protocol is the entry point for the protocol, this command must ALWAYS be supported
        data = self._send_command({'cmd': 'list-commands', 'args': None})

        if data['result'] != 'success':
            raise ValueError(f"observant: unable to list protocol '{data['message']}'")

        # healthy default:
        self.__protocol = {}

        allowed_types = {cls.__name__: cls for cls in (int, float, str, bool)}

        for spec in data['data']:
            name = spec['name']
            args = {}
            for key, typename in spec['args_spec'].items():
                if typename not in allowed_types:
                    args[key] = str #default to str
                else:
                    args[key] = allowed_types[typename]

            self.__protocol[name] = {'name': name, 'doc': spec['doc'], 'args_spec': args}

    def protocol(self, refresh=False):
        """ get the protocol """

        if not self.__protocol or refresh:
            self._list_protocol()

        return self.__protocol

    def get_command_spec(self, cmd):
        """ get the command spec by name from the protocol """

        if cmd not in self.protocol():
            raise IndexError(f"command not found {cmd}")

        return self.protocol()[cmd]

    def is_lit(self) -> bool:
        """ check if the observant is lit """
        return self.__lit

    def switch_light(self, enabled:bool):
        """ switch on/off the light by protocol """
        self.send_command('switch-light', enabled=enabled)


    def is_streaming(self) -> int:
        """ return True if the observant is streaming """
        return self.__streaming_port is not None

    def streaming_port(self) -> (int, None):
        """ return the current streaming port or None """
        return self.__streaming_port

    def start_streaming(self):
        """ start the streaming, and request the observant to do so """
        if self.is_streaming():
            return

        port = self.__streaming_port = self.__swarm.request_streaming(self)
        self.send_command('start-streaming', port=port)
        # now call the observant with a command?

    def stop_streaming(self):
        """ stop the streaming port and request the observant to comply """
        if not self.is_streaming():
            return

        self.__swarm.terminate_streaming(self)
        self.__streaming_port = None
        self.send_command('stop-streaming')


    def __str__(self):
        return f"observant-{self.__hwid} [{self.__address}]"

# vim: set sw=4 expandtab ts=4 ai cindent:
