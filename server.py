import socket
import os
import struct

IMAGE_DIR = './jpegs'

def get_server_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
    return ip

def start_server(port):
    server_ip = get_server_ip()

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind to a port
    server_socket.bind((server_ip, port))
    print(f"Server started at {server_ip} on port {port}")
    
    # Listen for incoming connections
    server_socket.listen(1)
    
    # Load all JPEGs into memory
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg") or f.endswith(".jpeg")]
    image_files = sorted(image_files)  # Take the first 10 JPEGs

    while True:
        print("\nWaiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            data = client_socket.recv(1024)
            if data:
                print(f"Received: {data.decode()}")
                client_socket.sendall(b'Hello, client!')

                for i, image_file in enumerate(image_files):
                    command = client_socket.recv(1024).decode()
                    if command.lower() == "next":
                        print(f"Client requested image {i + 1}: {image_file}")

                        # Send the image
                        image_path = os.path.join(IMAGE_DIR, image_file)
                        with open(image_path, 'rb') as img:
                            img_data = img.read()
                            img_size = len(img_data)

                            # Send the size of the image (4 bytes)
                            client_socket.sendall(struct.pack('!I', img_size))

                            # Send the image data
                            client_socket.sendall(img_data)

                        print(f"Sent image {i + 1} to client")
                    else:
                        print(f"Unexpected command from client: {command}")
                        break
            else:
                print("No data received")
        finally:
            client_socket.close()

if __name__ == "__main__":
    port = int(input("Enter port to start the server on: "))
    start_server(port)
