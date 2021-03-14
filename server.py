import socket
import os
import mimetypes

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
        501: 'Not Implemented',
        505: 'HTTP Version Not Supported'

    }

    def handle_request(self, data):
        # Create an instance of HTTPRequest
        request = HTTPRequest(data)

        # Now, we call the appropriate function(handler) according to the given request
        try:
            handler = getattr(self, 'handle_%s' % request.method)

        except(AttributeError):
            handler = self.HTTP_501_handler

        # Process the appropriate response, given the input request

        response = handler(request)

        return response

    def handle_GET(self, request):
        """
        Handles the response for the get method
        """
        filename = request.url.strip('/')

        if os.path.exists(filename):
            state_line = self.state_line(status_code=200)
            content_type = mimetypes.guess_type(filename)[0] or 'text/html'
            extra_headers = {'Content-Type': content_type}
            response_headers = self.response_headers(
                extra_headers=extra_headers)
            with open(filename, 'rb') as f:
                response_body = f.read()

        else:
            state_line = self.state_line(status_code=404)
            response_headers = self.response_headers()
            response_body = b'<h1>404: Not Found</h1>'

        blank_line = b'\r\n'
        return b''.join([state_line, response_headers, blank_line, response_body])

    def HTTP_501_handler(self, request):
        state_line = self.state_line(status_code=501)
        response_headers = self.response_headers()
        blank_line = b'\r\n'

        response_body = b'<h1>501 Not Implemented</h1>'
        return b"".join([state_line, response_headers, blank_line, response_body])

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


class HTTPRequest:
    def __init__(self, data):
        self.method = None
        self.url = None
        self.http_version = "1.1"  # Default version
        self.parse(data)

    def parse(self, data):
        # get all the lines of the request
        lines = data.split(b"\r\n")

        # first line of a HTTP request is the request line, containing the method, the url and the http version
        request_line = lines[0]

        request_fields = request_line.split(b" ")

        self.method = request_fields[0].decode()  # decode from bytes to string

        if len(request_fields) > 1:
            self.url = request_fields[1].decode()

        if len(request_fields) > 2:
            self.http_version = request_fields[2].decode()


if __name__ == "__main__":
    server = HTTPServer()
    server.start()
