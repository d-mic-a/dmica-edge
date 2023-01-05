"""

Observant Remote Interactive Terminal

Thi
"""

from cmd import Cmd
import json

class ObservantTerminal(Cmd):
    """
    Interactive terminal to control the swarm (for debug mostly)

    to use, run SwarmTerminal(swarm).cmdloop()
    """

    def __init__(self, obs):

        self.__observant = obs
        super().__init__()

        self.intro = f"Welcome to Observant {obs} Remote Terminal, " \
                   + "please run 'help' for all available commands"

        self.prompt = f"{obs}$ "

    def update_protocol(self, _):
        """ force the protocol update (debug) """
        self.__observant.protocol(True)

    def do_protocol(self, _):
        """ list the protocol commands doc (debug) """
        for name, desc in self.__observant.protocol().items():
            print(f"* {name}: {desc['doc']}")

    def do_dump_protocol(self, _):
        """ dump the protocol struct of the observant (debug) """
        print(json.dumps(self.__observant.protocol(), default=str, indent=4, sort_keys=True))

    def do_EOF(self, line): #pylint: disable=invalid-name
        """ quit on EOF """
        print("") # clear the console line
        return self.do_exit(line)

    def do_exit(self, line): #pylint: disable=unused-argument,no-self-use
        """ exit the terminal, and the program """
        return True

    def do_position(self, _):
        """ print the observant current status """
        print(json.dumps(self.__observant.position(), default=str, indent=4))


    def do_status(self, _):
        """ print the current observant full status """
        obs = self.__observant
        streaming = f"yes:{obs.streaming_port()}" if obs.is_streaming() else "no"
        lit = "on" if obs.is_lit() else "off"

        print(
            f"- hwid: {obs.hwid()}\n"
            f"- addr: {obs.address()}\n"
            f"- port: {obs.port()}\n"
            f"- streaming: {streaming}\n"
            f"- position: {obs.position()!r}\n"
            f"- light: {lit}\n"
        )

    def do_lite_on(self, _):
        """ switch on the lite """
        self.__observant.switch_light(True)

    def do_lite_off(self, _):
        """ switch off the lite """
        self.__observant.switch_light(False)

    def do_start_streaming(self, _):
        """ request the observant to start streaming """
        self.__observant.start_streaming()

    def do_stop_streaming(self, _):
        """ request the observant to stop streaming """
        self.__observant.stop_streaming()

    # magically populates all observant supported commands:

    def get_names(self):
        """
        This method used to pull in base class attributes
        at a time dir() didn't do it yet.

        (overriden from cmd to add the virtual commands here)
        """

        lst = dir(self.__class__)
        for name in self.__observant.protocol():
            name = name.replace('-', '_')
            lst.append(f"do__{name}") # double '_'
            lst.append(f"help__{name}") # double '_'
        # add all the do_* functions here
        return lst

    # https://github.com/python/cpython/blob/3.11/Lib/cmd.py#L213
    def __getattr__(self, attribute):
        """
        supports the virtual names
        """
        attrs = dir(self.__class__)

        # give priority to directly defined attributes
        if attribute in attrs:
            return attrs[attribute]

        # Must add the do_* functions here
        # each function must have a doc too __doc__

        protocol = self.__observant.protocol()

        if attribute.startswith('do__'):
            name = attribute[4:].replace('_', '-')
            if name in protocol:
                ret = lambda line:  self.send_protocol_command(name, line)
                ret.__doc__ = f"send the protocol command {name}:\n{protocol[name]['doc']}"
                return ret

        # else AttributeError
        raise AttributeError(f"{attribute} not found!")

    def send_protocol_command(self, cmd, line):
        """ send the command to observer, display result on the line """
        args = {}
        spec = self.__observant.get_command_spec(cmd)
        split = [x for x in line.split(' ') if x]

        for idx, item in enumerate(spec['args_spec'].items()):
            name, cls = item

            if idx >= len(split):
                print(f"missing argument {name} (position {idx})")
                return

            try:
                args[name] = cls(split[idx])
            except ValueError:
                print(f"invalid value {split[idx]} for arg {name} expected type {cls.__name__}")
                return

        ret = self.__observant.send_command(cmd, **args)
        print(json.dumps(ret, default=str, indent=4))
