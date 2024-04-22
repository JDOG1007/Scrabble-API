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
ENTER_NAME = "EN"
VIEW_PLAYER = "!PLAYER LIST"


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


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = receive(conn)
        if msg:
            if msg == DISCONNNECT_MESSAGE:
                connected = False
            if msg == INIT_MESSAGE:
                send(ENTER_NAME, conn)
                name = receive(conn)
                playerlist[name] = addr
                print(playerlist)

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
