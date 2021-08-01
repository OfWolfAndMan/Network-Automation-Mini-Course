from shared.zmq_connect import zmq_worker, zmq_client
from multiprocessing import Process




devices = {"device": "A"}
Process(target=zmq_worker).start()
