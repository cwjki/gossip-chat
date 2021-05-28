import sys
import threading
import zmq


class ClientDisplay(object):

    def __init__(self, node_port):
        self.context = zmq.Context()
        self.display_sock = None
        self.node_port = node_port

    def handleConnect(self):
        self.display_sock = self.context.socket(zmq.SUB)
        self.display_sock.setsockopt_string(zmq.SUBSCRIBE, '')
        self.display_sock.connect("tcp://localhost:" + self.node_port)

    def run(self):
        self.handleConnect()
        while True:
            data = self.display_sock.recv_json()
            username, message = data['username'], data['message']
            print('{}: {}'.format(username, message))


if len(sys.argv) != 2:
    print("expected: script, node_port")
    exit()

node_port = str(sys.argv[1])
client = ClientDisplay(node_port)
client.run()
