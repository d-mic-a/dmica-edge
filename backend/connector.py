from observant_swarm import Swarm, SwarmWatcher, SwarmTerminal

swarm_status = None
observant_list = []
observant_power = None
    
    
swarm = Swarm(("127.0.0.1","1000"))
swarm.start_discovery()


lst = swarm.observants() 

print(lst)