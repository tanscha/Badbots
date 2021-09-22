import socket
import sys
import time

from bot import *

ENCODING = 'utf-8'

if sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print("Put in the following arguments to connect:\n"
          "py [application] [address to connect to] [port to connect to] [chatbot to connect to]\n"
          "e.g py client.py localhost 12345 watson")
    sys.exit()

if len(sys.argv) != 4:
    print("Put in the following arguments to connect:\n"
          "py [application] [address to connect to] [port to connect to] [chatbot to connect to]\n"
          "e.g py client.py localhost 12345 watson")

else:

    HOST = str(sys.argv[1])
    PORT = sys.argv[2]
    bot = str(sys.argv[3]).lower()

    try:
        PORT = int(PORT)
    except ValueError:
        print("Invalid port. Try for example 12345")

    # a list of available chatbots
    chatbot_list = ["alexa", "siri", "cortana", "watson", "all"]

    if PORT is None or HOST == "":
        print("Invalid address or port")

    # the client will only connect if the input is correct
    elif bot not in chatbot_list:
        print("Invalid chatbot. Try with one of the following chatbots:")
        for i in chatbot_list:
            print(i)

    else:
        # create a socket with IPc4 address family and TCP socket.
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server timeout after seconds
        client_socket.settimeout(60)
        # connect to given host and port
        client_socket.connect((HOST, PORT))

        print("Client is running!", "Address:", HOST, "Port:", PORT, "Chatbot:", bot)
        print("\n-------------Welcome to BadBots!------------\n")

    message = ""
    alternative_action = ""

    # in a loop as long as server is running
    while True:
        message = None
        try:
            message = client_socket.recv(1024)
        except:
            print("Connection ended from server")
            sys.exit()

        if message is not None:
            # if message not empty -> extract the verb from message
            message = message.decode(ENCODING)
            print(message)
            action = extract_verb(message)

            if action is not None:
                response = ""
                if "Host:" in message:
                    alternative_action = action
                    response = chatbot_response(bot, action)
                if message != "" and alternative_action != "":
                    if action != alternative_action:
                        response = chatbot_response(bot, alternative_action, action)
                        alternative_action = ""

                        # random delay on response
                time.sleep(random.randint(2, 5))

                try:
                    if response != "":
                        client_socket.send(response.encode(ENCODING))
                except:
                    # closing
                    print("Connection ended from server.")
                    sys.exit()

