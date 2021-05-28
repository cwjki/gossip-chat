import zmq
import random
from threading import Thread
import time
import sys
import uuid


class GossipNode(object):
    infected_nodes = []

    def __init__(self, chat_port, display_port, connected_nodes):
        self.context = zmq.Context()
        self.chat_sock = None
        self.display_sock = None
        self.chat_port = chat_port
        self.messages = []
        self.display_port = display_port
        self.susceptible_nodes = connected_nodes

    def connect(self, node_port):
        node_sock = self.context.socket(zmq.REQ)
        node_sock.connect("tcp://localhost:" + node_port)
        return node_sock

    def handleReceive(self):
        data = self.chat_sock.recv_json()
        print(data)
        username = data['username']
        message = data['message']
        messageId = data['messageId']
        return [username, message, messageId]

    def handleSendToNode(self, username, message, messageId):

        susceptible_nodes = self.susceptible_nodes.copy()

        while susceptible_nodes:
            selected_port = random.choice(susceptible_nodes)

            print("\n")
            print("Susceptible nodes: ", susceptible_nodes)
            print("Infected nodes: ", GossipNode.infected_nodes)
            print("Selected node: [{0}]".format(selected_port))

            node_sock = self.connect(selected_port)

            data = {
                'messageId': messageId,
                'username': username,
                'message': message,
            }
            node_sock.send_json(data)
            node_sock.close()

            susceptible_nodes.remove(selected_port)
            GossipNode.infected_nodes.append(selected_port)

            print("Message: '{0}' ".format(message))
            print("Susceptible nodes: ", self.susceptible_nodes)
            print("Infected nodes: ", GossipNode.infected_nodes)
            print("\n")

    def handleSend(self, username, message):
        data={
            'username': username,
            'message': message,
        }
        self.chat_sock.send(b'\x00')
        self.display_sock.send_json(data)

    def run(self):
        self.chat_sock=self.context.socket(zmq.REP)
        self.chat_sock.bind("tcp://*:" + self.chat_port)

        self.display_sock=self.context.socket(zmq.PUB)
        self.display_sock.bind("tcp://*:" + self.display_port)

        print("Server listening")
        while True:
            username, message, messageId=self.handleReceive()

            filteredMessages=list(
                filter(lambda obj: obj[0] == messageId, self.messages))

            if len(filteredMessages) == 0:
                data={
                    'id': messageId,
                    'username': username,
                    'message': message,
                }

                self.messages.append((messageId, data))
                self.handleSendToNode(username, message, messageId)
                self.handleSend(username, message)


if len(sys.argv) != 3:
    print("expected: script, chat_port, display_port")
    exit()

chat_port=str(sys.argv[1])
display_port=str(sys.argv[2])

connecteds=[item for item in input(
    "Enter the list node ports : ").split()]

GossipNode=GossipNode(chat_port, display_port, connecteds)
GossipNode.run()
