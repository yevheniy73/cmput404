import socket

BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\nHost: " + host.encode('utf-8') + b"\n\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialize a socket
    s.connect((host, port)) #connect to the host and port requested
    s.send(request) #request the page
    s.shutdown(socket.SHUT_WR) #done sending the request

    result = s.recv(BYTES_TO_READ) #constantly receiving the response
    while(len(result) > 0):
        print(result)
        result = s.recv(BYTES_TO_READ)
    
    s.close() #must close the socket

#get("www.google.com", 80)
get("localhost", 8080)