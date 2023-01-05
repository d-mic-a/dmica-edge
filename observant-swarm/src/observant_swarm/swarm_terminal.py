"""
Observant Swarm Interactive Terminal

Thi
"""

import json
from cmd import Cmd
from .observant_terminal import ObservantTerminal

class SwarmTerminal(Cmd):
    """
    Interactive terminal to control the swarm (for debug mostly)

    to use, run SwarmTerminal(swarm).cmdloop()
    """

    def __init__(self, swarm):
        self.__swarm = swarm

        super().__init__()

        self.intro = "Welcome to the Observant Swarm Terminal, " \
                   + "please run 'help' for uall available commands"

        self.prompt = "swarm$ "


    def do_status(self, _):
        """ show the swarm status """
        swarm = self.__swarm

        disc = "yes" if swarm.is_discovering() else "no"
        addr, port = swarm.address()
        bcast, dport = swarm.broadcast_address()

        print(
             "discovery daemon:\n"\
             f"\t- running: {disc}\n"\
             f"\t- address: {bcast}\n"\
             f"\t- port: {dport}\n"\
             f"\t- streaming ports: {swarm.streaming_range()!r}\n"
        )

        print(
            "command server:\n"\
            f"\t- address: {addr}\n"\
            f"\t- port: {port}\n"\
        )

        lst = swarm.streamers()
        print(f"{len(lst)} streamers:")
        for obs in lst:
            print(f"\tport {obs.streaming_port()}: observant {obs.hwid()}")

    def do_start_discovery(self, _):
        """ start the observant swarm discovery thread """
        if self.__swarm.is_discovering():
            print("discovery already started")
            return

        self.__swarm.start_discovery()


    def do_stop_discovery(self, _):
        """ stop the discovery thread """
        if not self.__swarm.is_discovering():
            print("discovery not started")
            return

        self.__swarm.stop_discovery()
        self.__swarm.join()

    def do_list(self, _):
        """ list all observants currently registered in the swarm """
        data = []
        for obs in self.__swarm.observants():
            pos = obs.position()
            desc = {
                'id': obs.hwid(),
                'addr': obs.address(),
                'port': str(obs.port()),
                'position': repr(pos),
                'streaming': f"yes:({obs.streaming_port()})" if obs.is_streaming() else "no",
            }
            data.append(desc)

        if not data:
            print("No observant connected")
            return

        first = data[0]

        sizes = {key: max([len(item) for item in [desc[key] for desc in data]]) for key in first}

        # title line:
        for key, size in sizes.items():
            print(f"{key:<{size}} ", end="")

        print()

        for desc in data:
            for key, size in sizes.items():
                print(f"{desc[key]:<{size}} ", end="")
            print()


    def do_connect(self, line):
        """ connect to an observant """
        hwid = line.strip()
        obs = None

        try:
            obs = self.__swarm.observant(hwid)
        except KeyError:
            print(f"observant not found '{hwid}'")
            return

        cmd = ObservantTerminal(obs)
        cmd.cmdloop()

    def complete_connect(self, text, line, start_index, end_index): #pylint: disable=unused-argument
        """ autocomplete in the list of connects """
        words = [w for w in line.split(" ") if w]
        if len(words) > 1:
            return []

        lst = [obs.hwid() for obs in self.__swarm.observants()]
        return [hwid for hwid in lst if hwid.startswith(text)]


    def do_EOF(self, line): #pylint: disable=invalid-name
        """ quit on EOF """
        print("") # clear the console line
        return self.do_exit(line)

    def do_exit(self, line): #pylint: disable=unused-argument,no-self-use
        """ exit the terminal, and the program """
        return True

    request_goal_types = {
        'timeout': float,
        'count': int,
        'distance': float,
        'xy-distance': float,
        'elevation': float,
    }

    def complete_request(self, text, line, start_index, end_index): #pylint: disable=unused-argument
        """ autocomplete in the list for request"""
        words = [w for w in line.split(" ") if w.strip()]
        if len(words) <= 3:
            return []

        if '=' in text:
            return []

        lst = list(self.request_goal_types.keys())
        for desc in words[3:]:
            if '=' not in desc:
                continue
            key, _ = desc.strip().split('=')
            if key in lst:
                lst.remove(key)

        if text in lst:
            return [f"{text}="]

        if not text:
            return lst
        return [f'{goal}=' for goal in lst if goal.startswith(text)]


    def do_request(self, line):
        """start an echo-request on a position. Parameters are:

         x y z : position

         optional arguments (all floats or integer):

            timeout=X: the timeout to wait for
            count=N: the minumum number of participants
            distance=D: the max distance goal
            xy-distance=D: the max xy-distance
            elevation=D: the max elevation goal
        """

        args = [x.strip() for x in line.split(' ') if x.strip()]

        if len(args) < 3:
            print("must provide the location x y z at least, please refer to help request")
            return

        position = list((float(x) for x in args[0:3]))

        goals = {}
        for goal in args[3:]:
            try:
                key, value = goal.split('=')
            except ValueError:
                print(f"invalid goal spec {goal}, please check help")
                return

            if key not in self.request_goal_types:
                print(f"unknown goal {key}")
                return
            goals[key] = self.request_goal_types[key](value)

        timeout = goals.pop('timeout', None)

        print(
            "starting request on swarm:\n"
            f"- position: {position!r}\n"
            f"- goals: {goals!r}\n"
            f"- timeout: {timeout!r}\n"
        )

        request = self.__swarm.echo_request(position, goals, timeout)

        stats = json.dumps(request.result_stats(), default=str, indent=4)
        results = json.dumps(request.results(), default=str, indent=4)

        print(
            "request returned:\n"
            f"results: {results}\n"
            f"stats: {stats}\n"
        )
