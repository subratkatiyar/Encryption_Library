import sys
import socket
import threading

HEADER = 64
PORT = 1234
SERVER = socket.gethostbyname(socket.gethostname())
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
    global client_list
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                print(f"[{addr}] {msg}")
                # conn.send("Msg received".encode(FORMAT))
                # print("-->",msg)
                update_client(msg)
        except ConnectionResetError:
            break
    client_list.remove(conn)
    conn.close()
    sys.exit()


def start():
    # global client_list
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        # temp = [conn, addr]
        client_list.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
