import socket
SERVER = '127.0.0.1'
PORT = 5050
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((SERVER, PORT))
sentence = input('Input lowercase sentence: ')
byte_sentence = str.encode(sentence)
clientSocket.send(byte_sentence)
modifiedSentence = clientSocket.recv(1024)
print('From server: ', modifiedSentence)

clientSocket.close()
