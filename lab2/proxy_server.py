import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1" # this is localhost
PROXY_SERVER_PORT = 8080

# send some data(requests) to host:port
def send_requests(host, port, request):

    # Create a new socket in with block to ensure it's closed once we're done
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect the socket to host:port
        client_socket.connect((host, port))
        # Send the request through the connected socket.
        client_socket.send(request)
        # Shit the socket to further writes. Tells server we're done sending.
        client_socket.shutdown(socket.SHUT_WR)

        # Assemble response, be careful here, recall that recv(bytes) blocks until it recieves data!
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0: # read until connection terminates
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        # Return response
        return result
    
def handle_connection(conn, addr):
    with conn:
        print(f"Connectied by {addr}")

        request = b''
        while True: # while the client is keeping the socket open
            data = conn.recv(BYTES_TO_READ) # read data from the socket
            if not data: # if the socket has been closed, break
                break
            print(data) # print the data to screen
            request += data
            response = send_requests("www.google.com", 80, request) # send a request to google
            conn.sendall(response) # return the response from google to the client

# Start single-threaded proxy server
def start_server():
    # make server using 'with' to ensure it gets auto-closed
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # bind the server to host and port
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        # allow to reuse this socket address
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)
        # accept incoming connection
        conn, addr = server_socket.accept()
        handle_connection(conn, addr)

# Start muti-threaded proxy server
def start_threaded_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)

        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

#start_server()
start_threaded_server()