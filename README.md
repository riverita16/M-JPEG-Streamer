# Client-Server M-JPEG Streamer

Cient-server protocol/program, where the client needs to have a JPEG decoder and is able to successfully display a decompressed image.

Socket/TCP connection between the client and server where the client will fetch the first compressed file and decompress it. The decompressed file is to displayed for x-ms (x milliseconds) with the use of the OS-equivalent sleep command.