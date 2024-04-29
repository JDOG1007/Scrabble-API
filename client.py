import socket

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.10"
ADDR = (SERVER, PORT)
INIT_MESSAGE = "!INIT"
ENTER_NAME = "EN"
START_MATCH = "!START"
CHALLENGE_REQ = "You have been challenged type Y to continue"
COMMAND_LIST = [INIT_MESSAGE, DISCONNECT_MESSAGE, "!HELP", START_MATCH]
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
START_MESSAGE = "U HAVE BEEN STARTED WITH"
msgs = []


def send(msg2):
    message = msg2.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)

    client.send(message)


def receive():
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg1 = client.recv(msg_length).decode(FORMAT)
        if msg1 == CHALLENGE_REQ:
            if input(f"{CHALLENGE_REQ}: ") == "Y":
                play_game(2)
            else:
                print("Match declined")
        return msg1


hasINIT = False
send("connect")
connect = True


def play_game(pn):
    if pn == 1:
        send(input("Enter Text to send to Opponent"))
    else:
        print(f"Enemy player says: {receive()}")


while connect:
    print("")
    msg = input("Please enter a command. Type !HELP for a list of possible commands: ")
    print("")
    if msg not in COMMAND_LIST:
        print("Thats not a command idiot. Maybe try !HELP")
        continue
    if msg == DISCONNECT_MESSAGE:
        send(DISCONNECT_MESSAGE)
        print("Succesfully disconnected")
        break
    if msg == "!HELP":
        for command in COMMAND_LIST:
            print(command)
        continue
    if msg == INIT_MESSAGE:
        if not hasINIT:
            send(INIT_MESSAGE)
            name = input("Please enter a username: ")
            print("")
            print(f"Logged in as {name}")
            send(name)
            hasINIT = True
            continue
        else:
            print("You have already been initialized")
    if msg == START_MATCH:
        send(START_MATCH)
        if hasINIT:
            names = receive()
            print(f"Please enter the name of your opponent. Opponents online: {names}")
            print("")
            name = input()
            print("")
            print(f"Game started with {name}")
            send(name)
            play_game(1)
        else:
            print("You must log in with !INIT before starting a match")



