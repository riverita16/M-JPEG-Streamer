import socket
from time import sleep, time
from PIL import Image
from io import BytesIO
import struct
import psutil
import os

def close_image_viewer():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'mspmsn' in proc.info['name'].lower() or 'preview' in proc.info['name'].lower():
            proc.terminate()

def start_client(ip, port, ms):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((ip, port))
    print(f"Connected to server at {ip}:{port}")

    try:
        # Send initial message to the server
        message = "Hello, server!"
        client_socket.sendall(message.encode())

        # Receive the server's response
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")

        for i in range(12):
            command = "next"
            print(f"\nRequesting image {i + 1}")
            client_socket.sendall(command.encode())

            # Receive the image size (4 bytes)
            size_data = client_socket.recv(4)
            if len(size_data) < 4:
                print("Failed to receive image size.")
                break
            img_size = struct.unpack('!I', size_data)[0]

            # Receive the image data
            image_data = BytesIO()
            received = 0

            start = time()
            while received < img_size:
                chunk = client_socket.recv(min(1024, img_size - received))
                if not chunk:
                    break
                image_data.write(chunk)
                received += len(chunk)
            
            end = time()

            if received < img_size:
                print(f"Incomplete image received: {received}/{img_size} bytes")
                break

            image_data.seek(0)

            print(f'Decompression took {(end-start) * 1000} ms')

            # Open the image using Pillow
            image = Image.open(image_data)
            print(f"Displaying image {i + 1}")
            image.show()

            # Display the image for the specified duration
            sleep(ms / 1000)
            
        close_image_viewer()

    finally:
        client_socket.close()

if __name__ == "__main__":
    ip = input("Enter server IP to connect to: ")
    port = int(input("Enter port to connect to: "))
    ms = int(input('Enter the value for {x}-ms display duration: '))
    start_client(ip, port, ms)
