import sys
import socket
import threading

from variables import Variables
from aes_implementation import cipher

HEADER = 64
PORT = 1234
SERVER = socket.gethostname()
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
client_list = []


def update_client(msg):
    global client_list
    for clients in client_list:
        clients.send(msg)


def handle_client(conn, addr):
    global client_list, DISCONNECT_MESSAGE

    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)

            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length)
                decrypt_msg = cipher.decrypt(msg)
                # decrypt_msg = str(decrypt_msg)
                if decrypt_msg.find(DISCONNECT_MESSAGE) != -1:
                    print('handle client break')
                    connected = False
                else:
                    # print(f"[{addr}] {msg}")
                    update_client(msg)
        except ConnectionResetError:
            break
    client_list.remove(conn)
    conn.close()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    print(f"[CLOSED] {addr} is disconnected")
    # sys.exit()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        if Variables.threadFlag:
            print('start while broken')
            break
        conn, addr = server.accept()
        client_list.append(conn)
        local_client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        local_client_thread.daemon = True
        local_client_thread.start()

    print(f"[REMOVE LISTENER] Server listener is removed on {SERVER}")


print("[STARTING] server is starting...")
start()
