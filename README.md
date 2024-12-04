# Client-Server M-JPEG Streamer

### PA3_Team_ID 5

Cient-server protocol/program, where the client needs to have a JPEG decoder and is able to successfully display a decompressed image.

Socket/TCP connection between the client and server where the client will fetch the first compressed file and decompress it. The decompressed file is to displayed for x-ms (x milliseconds) with the use of the OS-equivalent sleep command.

### Steps to run

**Server**
```console
foo@bar:~$ python3 server.py
Enter port to start the server on: <port>
```

**Client**
```console
foo@bar:~$ python3 client.py
Enter server IP to connect to: <ip>
Enter port to connect to: <port>
Enter the value for {x}-ms display duration: <x-ms/fps>
```