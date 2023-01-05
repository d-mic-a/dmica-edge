#! /usr/bin/env python3
""" Simple test server used as example of the Swarm usage """

from observant_swarm import Swarm, SwarmWatcher, SwarmTerminal


class ConsoleWatcher(SwarmWatcher): #pylint: disable=too-few-public-methods
    """ simple watcher example """

    def on_observant_connected(self, swarm, observant): #pylint: disable=redefined-outer-name
        print(f"Observant {observant} joins the swarm {swarm}")



if __name__ == "__main__":

    swarm = Swarm(("127.0.0.1", "1234"))
    swarm.register_watcher(ConsoleWatcher())

    cmd = SwarmTerminal(swarm)

    swarm.start_discovery()
    cmd.cmdloop()
