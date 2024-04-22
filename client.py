import socket

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.10"
ADDR = (SERVER, PORT)
INIT_MESSAGE = "!INIT"
ENTER_NAME = "EN"
COMMAND_LIST = [INIT_MESSAGE, DISCONNECT_MESSAGE, "!HELP"]
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        return msg
hasINIT = False
send("connect")
connect = True
while connect == True:
    msg = input("Please enter a command. Type !HELP for a list of possible commands: ")
    print("")
    send(msg)
    if msg not in COMMAND_LIST:
        print("Thats not a command idiot. Maybe try !HELP")
        continue
    if msg == DISCONNECT_MESSAGE:
        print("Succesfully disconnected")
        break
    if msg == "!HELP":
        for command in COMMAND_LIST:
            print(command)
        continue
    msg = receive()
    if msg == ENTER_NAME and hasINIT == False:
        name = input("Please enter a username: ")
        send(name)
        hasINIT = True
    else:
        print("You have already been initialized")
        continue



