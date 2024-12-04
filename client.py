# The client needs to have two buffers, one for the display and other for receiving the next file.

# receive one image -> display -> load next image -> display

import socket

# Client program
def start_client(ip, port):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((ip, port))
    print(f"Connected to server at {ip}:{port}")

    try:
        # Send some data to the server
        message = "Hello, server!"
        client_socket.sendall(message.encode())

        # Receive a response from the server
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")
    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    ip = input("Enter server IP to connect to: ")
    port = int(input("Enter port to connect to: "))
    start_client(ip, port)
