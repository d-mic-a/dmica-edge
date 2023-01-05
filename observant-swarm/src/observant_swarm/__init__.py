# Observant Swarm Library
# @author: Florian Delizy
# @license: M.I.T.

def package_information():
    """ get a tuple (name, version) from the changelog """
    if package_information.name is None:
        import os #pylint: disable=import-outside-toplevel
        import re #pylint: disable=import-outside-toplevel
        with open(os.path.join(os.path.dirname(__file__), "changelog.txt")) as changelog:
            matches = re.compile(r"([^ ]+) \(([^\)]+)\) .*").match(changelog.readline()) # pylint: disable=invalid-name
            package_information.name = str(matches[1].replace("-", "_"))
            package_information.version = str(matches[2])

    return (package_information.name, package_information.version)

package_information.name = None
package_information.version = None


def __getattr__(name: str) -> any:
    if name == "__version__":
        return package_information()[1]
    raise AttributeError("module does not contain %s" % (repr(name)))


__author__ = "Florian Delizy <fdelizy.ee11@nycu.edu.tw>"


from .observant import Observant
from .swarm import Swarm, SwarmWatcher
from .swarm_terminal import SwarmTerminal
from .observant_terminal import ObservantTerminal

# vim: set sw=4 expandtab ts=4 ai cindent:
