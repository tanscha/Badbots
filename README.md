# BadBots
BadBots is a socket chatroom program that lets you chat with different hardcoded chatbots.
## To start the program
Run the server first:
```
py server.py
```
Then run clients:
```
py client.py [host] [port] [chatbot]
py client.py localhost 12345 watson
```
## The chatbots
There are four available chatbots: alexa, siri, watson and cortana. 
They have their own answers to different suggested actions.
Their answers are sent to the host/server and all other clients except themselves.
The bots have som memory and will respond different if an action is already suggested.
The chatbots are supposed to be negative, sassy and talkative.

The chatbot "all" is only supposed to be a quick way to talk several bots while only 
connecting from one client. The best experience is when you connect 
alexa, siri, watson and cortana in parallel from different terminals.


## TCP Server
The server acts as a chat room and initiates rounds of dialogue. 
The host will first be asked if they want to suggest an action or let it be random.
y for own suggestion, n (or just press enter) for random.
The suggestion is sent to all connected clients.
Each client has its separate thread, and gets a thread number when connecting. 
One round of dialogue counts 10 suggested actions from the host, and then closes.
Alternatively, the server closes if the host writes "bye" when asked if they want
to suggest their own action. The server also closes when the input is "bye"
when asked to suggest a verb.

To view explanation on command line parameters:
```
py server.py --help 
```


## TCP client
The client program takes in 3 command line parameters: HOST/IP address, PORT and bot. 
Each client can connect from its own terminal and run a bot each. 
If the message is from the host, the suggested action will be extracted from the sentence.
Please run Watson, Alexa, Siri and Cortana in parallel to get the full experience.
