import socket

SERVER = '127.0.0.1'
PORT = 5050


class TCPServer:

    def __init__(self, server=SERVER, port=PORT):
        self.server = server
        self.port = port
        self.address = (self.server, self.port)

    def start(self):
        # create a socket object
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind the server object to the adress and port
        server.bind(self.address)

        # start listening for connections

        server.listen(5)
        try:
            print("[LISTENING] Server listening at ", server.getsockname())

            while True:
                # accept any new connection
                conn, addr = server.accept()
                print("Connected by ", addr)

                data = conn.recv(1024)
                print(data)
                # send back the data to client
                conn.sendall(data)

                # close the connection
                conn.close()

        finally:
            server.shutdown(socket.SHUT_RDWR)
            server.close()


if __name__ == "__main__":
    server = TCPServer()
    server.start()
