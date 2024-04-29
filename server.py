import threading
import socket


HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (SERVER, PORT)
server.bind(ADDR)
FORMAT = 'utf-8'
DISCONNNECT_MESSAGE = "!DISCONNECT"
INIT_MESSAGE = "!INIT"
START_MESSAGE = "U HAVE BEEN STARTED WITH"
ENTER_NAME = "EN"
COMMAND_LIST = f"{DISCONNNECT_MESSAGE}"
START_MATCH = "!START"
CHALLENGE_REQ = "You have been challenged type Y to continue"
playerlist = {}


def send(msg, conn):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def receive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg


def game(p1, p2):
    send(CHALLENGE_REQ, p2)
    tts = receive(p1)
    print(tts)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = receive(conn)
        if msg:
            if msg == DISCONNNECT_MESSAGE:
                connected = False
            if msg == INIT_MESSAGE:
                name = receive(conn)
                playerlist[name] = [conn]
                print(playerlist)
            if msg == START_MATCH:
                names = ""
                for name in playerlist.keys():
                    names += name + " "
                send(names, conn)
                name = receive(conn)
                print(name)
                game(conn, playerlist[name][0])
    conn.close()


def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("Server starting")
start()
