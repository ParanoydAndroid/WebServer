# Import socket module
from socket import *


def send_by_byte(output: str, s: socket):
    for i in range(0, len(output)):
        s.send(output[i].encode())
    s.send('\r\n'.encode())

    return


# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 12000

serverSocket.bind(('', serverPort))
serverSocket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
    print('Ready to serve...')

    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    DATA_SIZE = 4096

    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except clause is executed
    try:
        # Receives the request message from the client
        message = connectionSocket.recv(DATA_SIZE).decode()

        # This is only necessary because for some reason I can't figure out, neither accept
        # Nor receive are blocking properly
        if message == '':
            break

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1]

        # Because the extracted path of the HTTP request includes
        # a character '/', we read the path from the second character
        f = open(filename[1:])

        # Store the entire content of the requested file in a temporary buffer
        outputdata = f.read()

        # Send the HTTP response header line to the connection socket

        OK_status = "HTTP/1.1 200 OK"
        OK_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(outputdata.encode()),
            'Connection': 'close'
        }

        OK_headers_joined = ''
        for k, v in OK_headers.items():
            new_header = ''.join("{}: {}\r\n".format(k, v))
            OK_headers_joined  += new_header

        print("Headers post join:", OK_headers_joined)

        send_by_byte(OK_status, connectionSocket)
        send_by_byte(OK_headers_joined, connectionSocket)

        # Send the content of the requested file to the connection socket
        send_by_byte(outputdata, connectionSocket)

        # Close the client connection socket
        connectionSocket.close()

    except IOError:

        error_status = "HTTP/1.1 404 Not Found"
        error_file = "404.html"

        with open(error_file, 'r') as error_file:
            outputdata = error_file.read()

        error_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(outputdata.encode(encoding="utf-8")),
            'Connection': 'close'
        }

        error_headers_joined = ''.join("%s: %s\r\n".format((k, v) for k, v in error_headers))

        # Send HTTP response message for file not found
        send_by_byte(error_status, connectionSocket)
        send_by_byte(error_headers_joined, connectionSocket)
        send_by_byte(outputdata, connectionSocket)

        # Close the client connection socket
        connectionSocket.close()

print("Stopping service ...\n")
serverSocket.close()
print("Service stopped!")
