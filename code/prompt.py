import sys
import threading
import zmq
import uuid


class ClientPrompt(object):

    def __init__(self, username, prompt_port):
        self.username = username
        self.context = zmq.Context()
        self.chat_sock = None

    def handleConnect(self):
        self.chat_sock = self.context.socket(zmq.REQ)
        self.chat_sock.connect("tcp://localhost:" + prompt_port)

    def handleReconnect(self):
        self.chat_sock.setsockopt(zmq.LINGER, 0)
        self.chat_sock.close()
        self.handleConnect()

    def handleSend(self, message):
        messageId = uuid.uuid4()

        data = {
            'messageId': str(messageId),
            'username': username,
            'message': message,
        }
        self.chat_sock.send_json(data)

    def run(self):
        self.handleConnect()

        while True:
            message = input("%s> " % username)
            self.handleSend(message)
            self.chat_sock.recv()


if len(sys.argv) != 3:
    print("expected: script, username, prompt_port")
    exit()

username = str(sys.argv[1])
prompt_port = str(sys.argv[2])
client = ClientPrompt(username, prompt_port)
client.run()
