import socket
import threading
import json
from time import sleep


HEADER = 1024
PORT = 6000
HOST = '192.168.0.10'
FORMAT = 'utf-8'
messages = []
NAME = input("Enter username: ")
print("")


def send(msg, conn):
    json_msg = json.dumps(msg)
    message = json_msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    print(f"Sending: {message}: {send_length}")
    conn.send(send_length)
    conn.send(message)


def receive_messages(client_socket):
    while True:
        try:
            msg_length = client_socket.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client_socket.recv(msg_length).decode(FORMAT)
                messages.append(json.loads(msg))
        except Exception as E:
            print(f"Error: {E}")


def game_p2(client_socket):
    while True:
        if messages[-1][0] == "p1msg":
            print(f'MSG: {messages[-1][1]}')
            messages.append([0, 0])
            to_send = input("MSG: ")
            send(to_send, client_socket)
            sleep(0.10)


def game_p1(client_socket):
    send(input("MSG: "), client_socket)
    sleep(0.10)
    while True:
        if messages[-1][0] == "p2msg":
            print(f'MSG: {messages[-1][1]}')
            messages.append([0, 0])
            send(input("MSG: "), client_socket)
            sleep(0.10)


def main():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    send((['INIT', NAME]), client_socket)
    while True:
        msg = [input("Enter a command: ")]
        if messages and messages[-1] == "summmoned":
            print("Jokes on you game has started")
            game_p2(client_socket)
        if msg[0] == "SEND":
            msg.append(input("enter msg"))
            send(msg, client_socket)
            sleep(0.10)
            continue
        if msg[0] == "START":
            send(msg, client_socket)
            sleep(0.10)
            print(messages[-1])
            opponent = input("choose an opponent: ")
            messages.append("START")
            send(opponent, client_socket)
            game_p1(client_socket)
            continue


if __name__ == "__main__":
    main()
