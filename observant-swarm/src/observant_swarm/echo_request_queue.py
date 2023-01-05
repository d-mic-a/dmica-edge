""" echo request queue, implements the request waiting and Id mechanism """

import uuid
import threading
import socket
import json

class EchoRequestQueue:
    """Queue requests, and release (out of wait) when conditions are met """

    def __init__(self, position, goals: dict):

        self.__position = position
        self.__condition = threading.Condition()
        self.__lock = threading.Lock()
        self.__goals = goals

        self.__results = []
        self.__id = str(uuid.uuid4())

    def set_goalds(self, goals: dict):
        """ set the request goals """
        self.__goals = goals

    def result_stats(self):
        """ return stats about current results """
        data = {
            'count': 0,
            'distance': None,
            'xy-distance': None,
            'elevation': None,
        }

        with self.__lock:
            data['count'] = len(self.__results)

            if not self.__results:
                return data


            for order in ('distance', 'xy-distance', 'elevation'):
                mapping = {data[0][order]: data[1] for data in self.__results}
                keys = sorted(mapping.keys())
                data[order] = tuple((k, mapping[k]) for k in keys)

            return data

    def results(self):
        """ raw results """
        with self.__lock:
            return self.__results[:]

    def request_id(self):
        """ get the request ID (hashable) """
        return self.__id

    def wait(self, timeout=None):
        """ wait for request to complete """
        with self.__condition:
            self.__condition.wait(timeout)

    def broadcast(self, address, multicast_address):
        """ send the request on the network """

        data = json.dumps({
            'cmd': 'echo-request',
            'args': {
                'x': self.__position[0],
                'y': self.__position[1],
                'z': self.__position[2],
                'request_id': self.__id,
            }
        }, default=str)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

        sock.bind((address, 0))
        sock.sendto(bytes(data, "utf-8"), multicast_address)

    def on_echo_reply(self, obs, data):
        """ update the results """

        # sanity checks:
        if data.get('type') != 'echo-reply':
            print(f"invalid echo reply {data.get('type')}")
            return

        request_id = data.get('request_id')
        if request_id != self.__id:
            print(f"invalid request id '{request_id} not matching {self.__id}")
            return

        with self.__lock:
            self.__results.append((data, obs))

        if not self.__goals:
            return

        stats = self.result_stats()
        release = True

        # invert counts for comparison :)
        goals = dict(self.__goals)

        stats['count'] *= -1
        if 'count' in goals:
            goals['count'] *= -1

        for cond, value in stats.items():
            if cond in goals:
                release = release and (value <= goals[cond])

        if release:
            with self.__condition:
                self.__condition.notify_all()
