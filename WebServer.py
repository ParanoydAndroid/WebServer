# Import socket module
from socket import *

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
    DATA_SIZE = 1024

    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except clause is executed
    try:
        # Receives the request message from the client
        message = connectionSocket.recv(DATA_SIZE).decode()

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1]

        # Because the extracted path of the HTTP request includes
        # a character '/', we read the path from the second character
        f = open(filename[1:])

        # Store the entire content of the requested file in a temporary buffer
        outputdata =  "test" # Fill in start    #Fill in end

        # Send the HTTP response header line to the connection socket
        # Fill in start
        # Fill in end

        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # Close the client connection socket
        connectionSocket.close()

    except IOError:
        break
        # Send HTTP response message for file not found
        # Fill in start    #Fill in end
        # Close the client connection socket
        # Fill in start    #Fill in end

serverSocket.close()
