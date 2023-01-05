from backend.observant_swarm import *
#from yolov7PoseEstimation import poseEstimate

class ConsoleWatcher(SwarmWatcher): #pylint: disable=too-few-public-methods
    """ simple watcher example """

    def on_observant_connected(self, swarm, observant): #pylint: disable=redefined-outer-name
        print(f"Observant {observant} joins the swarm {swarm}")

def detections():
    detection_data = []
    
    detection_data.append(poseEstimate.run())
    
    print(detection_data)


def observants_api():
    swarm_status = None
    observant_list = []
    observant_power = None
    
    swarm = Swarm(("127.0.0.1","1234"))
    swarm.register_watcher(ConsoleWatcher())
    # cmd = SwarmTerminal(swarm)
    while True:
        swarm.start_discovery()
        print(swarm.is_discovering())
    
        lst = swarm.observants()
    
    print(lst)


if __name__ == "__main__":
    observants_api()
    