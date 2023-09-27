import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1" # this is localhost
PORT = 8080

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            # wait for a request and when you get it, you receive it
            data = conn.recv(BYTES_TO_READ)
            #if receive an empty byte string b''
            if not data:
                break
            print(data)
            # send back to the client (echo it)
            conn.sendall(data)

# Start single threaded echo server
def start_server():
    # initialize socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # socket init
        s.bind((HOST, PORT)) #bind ip and port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # set reuseaddr to 1
        s.listen() # listen for incoming connections
        conn, addr = s.accept() # socket referring to client, addr is client IP and Port
        handle_connection(conn, addr) # send a response


# Start multithreaded echo server
def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # socket init
        s.bind((HOST, PORT)) #bind ip and port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # set reuseaddr to 1
        s.listen(2) # allow backlog of up to 2 connections ==> queue [waiting conn1, waiting conn2]
        while True:
            conn, addr = s.accept() # socket referring to client, addr is client IP and Port
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

#start_server()
start_threaded_server()
