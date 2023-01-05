# Observant Swam library

## Introduction

This repository contains the python server library used to control the Observant Swarm.


## Building

```
        make dist
```

## Testing:

```
        ./tests/local_server.py
```

The test runs a terminal, use help for more information. (you need to have an observant running in the network).

example of session:

```
 ./tests/local_server.py 
Welcome to the Observant Swarm Terminal, please run 'help' for uall available commands
swarm$ help

Documented commands (type help <topic>):
========================================
EOF  connect  exit  help  list  start_discovery  status  stop_discovery

Observant observant-6be21385ad3b [192.168.45.8] joins the swarm SWARM[127.0.0.1:1234]
swarm$ connect 6be21385ad3b
Welcome to Observant observant-6be21385ad3b [192.168.45.8] Remote Terminal, please run 'help' for all available commands
observant-6be21385ad3b [192.168.45.8]$ help

Documented commands (type help <topic>):
========================================
EOF             _randomize_id    _start_beacon  _stop_server   help    
_daemon_status  _server_address  _start_server  _verbosity     position
_list_commands  _set_id          _status        dump_protocol  protocol
_quit           _set_position    _stop_beacon   exit         

observant-6be21385ad3b [192.168.45.8]$ position
[
    1.0,
    2.0,
    3.0
]
observant-6be21385ad3b [192.168.45.8]$ help position
 print the observant current status 
observant-6be21385ad3b [192.168.45.8]$ help _status
send the protocol command status:
 Get information about the observant
format:
{
    "cmd": "status"
}

```


## Usage

```python
        import observant_swarm

        swarm = Swarm("127.0.0.1", "1234")
        swarm.start_discovery()

        // do your thing

        lst = swarm.observants() // get the list of Observant objects
 
```


please check the code for more info
