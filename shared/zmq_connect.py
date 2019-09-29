import zmq
import json


#   Request-reply service in Python
#   Connects REP socket to tcp://localhost:5560
#   Expects "Devices" from client, replies with valid devices
#
def zmq_worker():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5559")
    devices = json.loads(socket.recv())
    return devices


#   Connects REQ socket to tcp://localhost:5559
#   Sends "Devices" to server, expects a device inventory
#   of non-excluded devices to proceed with
#
def zmq_client(devices):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")
    devices = (json.dumps(devices)).encode("ascii")
    socket.send(devices)
