import time
import sys
import socket
import threading
import random

from bot import verbs

"""
This program lets you chat with different bots. You can chose between alexa, siri, cortana, watson.
Run them all in parallel for the full experience.
"""

ENCODING = 'utf-8'
connection_list = []


if sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print("Put in the following arguments to start the server:\n"
          "py [application] [port to connect to]\n"
          "e.g py server.py 12345")
    sys.exit()

elif len(sys.argv) != 2:
    print("Put in the following arguments to start the server:\n"
          "py [application] [port to connect to]\n"
          "e.g py server.py 12345")
else:
    HOST = 'localhost'
    PORT = sys.argv[1]

    try:
        PORT = int(PORT)
    except ValueError:
        print("Invalid port number, try for example 12345")

    if PORT == "":
        print("Type a valid port number to connect, for example 12345")

    else:
        # create socket - IPv4 address family and TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # REUSEADDR set to 1 as socket option
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # server informs OS that it will use given host and port
        server_socket.bind((HOST, PORT))
        # server listens for connections
        server_socket.listen()

        print("Server is running!", "Address:", HOST, "Port:", PORT)
        print("\n-------------Welcome to BadBots!------------\n"
              "Wait for connected clients...")


class Communication(threading.Thread):
    # constructor
    def __init__(self, thread_number, client_socket, client_address):
        self.thread = threading.Thread.__init__(self)
        self.thread_number = thread_number
        self.client_socket = client_socket
        self.client_address = client_address
        self.connected = True

    def run(self):
        print(f"\nConnection nr {self.thread_number}: Connected to {self.client_address}")

        while self.connected:
            message = ""

            try:
                message = self.client_socket.recv(1024).decode(ENCODING)
            except:
                # removing disconnected client
                print(f"\nConnection {self.thread_number} disconnected.")
                self.connected = False
                self.remove_self()

            if message != "":
                print(message)
                message = message
                broadcast(self, message)
            else:
                self.connected = False

    def suggestion_new(self, text):
        if self.connected:
            self.client_socket.send(text.encode(ENCODING))
        else:
            print(f"Connection {self.thread_number} disconnected")
            self.remove_self()

    def remove_self(self):
        remove_from_list(self)


def broadcast(connect, msg):
    for c in connection_list:
        if c != connect:
            c.client_socket.send(msg.encode(ENCODING))


class Connection(threading.Thread):
    # constructor
    def __init__(self, conn_list):
        self.thread = threading.Thread.__init__(self)
        self.connection_list = conn_list

    def run(self):
        while True:
            # accept new connection -> new socket
            client_socket, address = server_socket.accept()
            new_connection = Communication(len(connection_list), client_socket, HOST)

            # append new connection
            connection_list.append(new_connection)
            connection_list[len(connection_list) - 1].start()

    def remove_disconnected(self, disconnected_client):
        self.connection_list.remove(disconnected_client)
        # remove disconnected client
        print(f"Connection nr {disconnected_client.thread_number} removed from list of connections")


connection = Connection(connection_list)
connection.daemon = True
connection.start()


def remove_from_list(disconnected):
    # remove disconnected client
    connection.remove_disconnected(disconnected)


action = ""
time.sleep(12)
# asks the host if they want to choose an action or not.
choice = input("Do you want to make a suggestion yourself? y/n:")

# the host choose an action from a list of verbs that the chatbots understand.
# If they don't, something random gets chosen.
if choice == "y":
    for counter in range(10):
        time.sleep(6)
        print("\nVerbs: eat, study, play, code, work, think, sleep, read, fly, talk, laugh, climb")
        suggestion_input = input("Suggest a verb to do: ")
        if suggestion_input == "bye":
            sys.exit()
        elif suggestion_input not in verbs:
            suggestion_input = random.choice(verbs)
        suggestion = "\nHost: Do you guys want to {}".format(suggestion_input)
        time.sleep(5)
        print(suggestion)
        for conn in connection_list:
            conn.suggestion_new(suggestion)

# random action gets suggested
if choice == "n" or choice == "":
    for counter in range(10):
        action = random.choice(
            ["eat", "study", "play", "work", "sleep", "read", "fly", "talk", "laugh", "climb"])
        suggestion = "\nHost: Why don't we {} today?".format(action)
        time.sleep(11)
        print(suggestion)
        for conn in connection_list:
            conn.suggestion_new(suggestion)

if choice == "bye":
    sys.exit()

# delay to avoid closing before response from client
time.sleep(12)
print("Closing...")
sys.exit()
