import socket

def get_server_ip():
    # dummy socket to get the server's IP address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
    return ip


def start_server(port):
    server_ip = get_server_ip()

    # create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # bind to a port
    server_socket.bind((server_ip, port))
    print(f"Server started at {server_ip} on port {port}")
    
    # listen for incoming connections
    server_socket.listen(1)
    
    while True:
        print("Waiting for a connection...")

        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            # send compressed jpegs
            data = client_socket.recv(1024)
            if data:
                print(f"Received: {data.decode()}")
                # Send a response back to the client
                client_socket.sendall(b'Hello, client!')
            else:
                print("No data received")
        finally:
            # Close the connection
            client_socket.close()

if __name__ == "__main__":
    port = int(input("Enter port to start the server on: "))
    start_server(port)