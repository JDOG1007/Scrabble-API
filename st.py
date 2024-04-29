import socket
import threading
import json
from time import sleep


HEADER = 1024
PORT = 6000
HOST = '192.168.0.10'
clients = {}
FORMAT = 'utf-8'


def send(msg, conn):
    json_msg = json.dumps(msg)
    message = json_msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def receive(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    print(f"MSG LENGTH: {msg_length}")
    if msg_length:
        print("w1")
        msg_length = int(msg_length)
        print('w2')
        msg = conn.recv(msg_length).decode(FORMAT)
        return json.loads(msg)


def game(conn_1, conn_2):
    while True:
        msg = receive(conn_1)
        sleep(0.10)
        send(['p1msg', msg], conn_2)
        sleep(0.10)
        print("w1")
        msg2 = receive(conn_2)
        print('w2')
        sleep(0.10)
        print(f'MSG: {msg2}')
        msg2 = str(msg2)
        send(['p2msg', msg2], conn_1)
        sleep(0.10)


def handle_client(client_socket, client_address):
    init = False
    while True:
        try:
            message = receive(client_socket)
            if message[0] == "INIT" and not init:
                clients[message[1]] = ([client_socket, client_address])
                print(clients)
            if message[0] == "SEND":
                send(message[1], client_socket)
            if message[0] == "START":
                send(list(clients.keys()), client_socket)
                player = receive(client_socket)
                send("summmoned", clients[player][0])
                game(client_socket, clients[player][0])
        except Exception as E:
            print(f"Error: {E}")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Listening on {HOST}:{PORT}")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection {client_socket}:{client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    main()
