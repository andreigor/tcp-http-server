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
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind the server object to the adress and port
        server.bind(self.address)

        # start listening for connections

        server.listen(5)
        print("[LISTENING] Server listening at ", server.getsockname())

        while True:
            # accept any new connection
            conn, addr = server.accept()
            print("Connected by ", addr)

            data = conn.recv(1024)
            print(data)

            response = self.handle_request(data)
            # send back the data to client
            conn.sendall(response)
            # close the connection
            conn.close()

    def handle_request(self, data):
        """Handles incoming data and returns a response.
        Override this in subclass.
        """
        return data


class HTTPServer(TCPServer):
    headers = {
        "Connection: keep-alive"
        'Server': 'CrudeServer',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: 'OK',
        301: 'Moved Permanently',
        400: 'Bad Request',
        404: 'Not Found',
        505: 'HTTP Version Not Supported'

    }

    def handle_request(self, data):
        state_line = self.state_line(status_code=200)
        headers = self.response_headers

        # add a blank line to separate header from body
        blank_line = b'\r\n'

        response_body = b"""<html>
        <body>
        <h1>
        Request Received!
        </h1>
        </html>
        
        """

        return b"".join([state_line, headers, blank_line, response_body])

    def state_line(self, status_code):
        """Returns response line"""
        reason = self.status_codes[status_code]
        line = "HTTP/1.1 %s %s\r\n" % (status_code, reason)

        return line.encode()  # call encode to convert str to bytes

    def response_headers(self, extra_headers=None):
        """Returns headers
        The `extra_headers` can be a dict for sending 
        extra headers for the current response
        """
        headers_copy = self.headers.copy()  # make a local copy of headers

        if extra_headers:
            headers_copy.update(extra_headers)

        headers = ""

        for h in headers_copy:
            headers += "%s: %s\r\n" % (h, headers_copy[h])

        return headers.encode()  # call encode to convert str to bytes


if __name__ == "__main__":
    server = HTTPServer()
    server.start()
