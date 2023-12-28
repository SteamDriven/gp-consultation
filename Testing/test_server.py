import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    try:
        server_socket.bind(('localhost', 8080))
        server_socket.listen()
        print(f">: Server is successfully setup and listening from port: {8080}")

        conn, addr = server_socket.accept()
        print(f">: Accepted connection by Address: {addr}")

        while True:
            data = conn.recv(4096).decode()
            if not data:
                break
            print(f">: From CLIENT: {str(data)}")
            conn.send('>: This is SERVER'.encode())

        conn.close()

    except socket.error as err:
        print(err)
        print(f">: [SERVER]: Failed to connect to socket on HOST: {'localhost'}")


