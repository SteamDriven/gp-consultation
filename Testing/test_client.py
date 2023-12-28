import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

client_socket.send('>: I am the CLIENT'.encode())
data = client_socket.recv(4096).decode()

print(f">: From SERVER: {data}")
client_socket.close()


