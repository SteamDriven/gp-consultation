from database import Database, tables
from configs import UserTypes, Commands
from helper import *

import socket
import json
import threading
import string
import random
import logging


class Server:
    """
        Server class that holds all the necessary attributes for socket connection.
    """

    def __init__(self, host, port):
        """
            Initialize the Server object.

            Args:
                host (str): The host address.
                port (int): The port number.
        """
        self.host = host
        self.port = port
        self.end = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connected = None
        self.message = {'COMMAND': "", 'CLIENT': [], 'DATA': []}
        self.client_address = None
        self.message = {"COMMAND": "", "CLIENT": "", "DATA": ""}
        self.connected_users = {}
        self.appointments = {}
        self.query = ""
        self.query_data = []

        self.database = Database('Olinic Management.db')
        self.database.create_tables(tables)
        self.setup_server()

    def stop_server(self):
        if self.server_socket:
            self.server_socket.close()
            print(f">: [SERVER]: Binding to socket on HOST: {self.host} has been severed!")

    def handle_messages_from_client(self, client):
        """
            Handle client requests and return information back.

            Args: client (socket.socket): Client socket object.
        """

        users = {-1: None, 1: UserTypes.PATIENT, 2: UserTypes.CLINICIAN}

        while True:
            try:
                data = client.recv(2048)

                if not data:
                    break

                else:
                    message = json.loads(data.decode())

                    if message['COMMAND'] == Commands.chat_commands['announcement']:
                        logging.info(f">: {message['DATA']} has joined the chat.")

                    if message['COMMAND'] == Commands.COMMAND_REQUEST_DOCTOR:
                        logging.info(">: Server received request to find available doctors.")
                        print('>: Server received request to find available doctors.')
                        doctors = self.database.request_doctors()

                        if doctors:
                            self.message['COMMAND'] = Commands.RETURN_DOCTORS
                            self.message['CLIENT'] = ServerCommands.find_user(self.connected_users, client)
                            self.message['DATA'] = doctors

                            logging.info(f">: Sending list of available doctors to User: {self.message['CLIENT']}")

                            client.send(json.dumps(self.message).encode())
                            self.message = {'COMMAND': "", 'CLIENT': [], 'DATA': []}

                    if message['COMMAND'] == Commands.chat_commands['broadcast']:
                        logging.info(f">: User {message['CLIENT']} has said: {message['DATA']}")

                        for key, user_socket in self.connected_users.items():
                            if user_socket == self.connected_users[message['CLIENT']]:
                                logging.debug(f"Skipping USER {key} cause it's matches Sender id.")
                                continue

                            logging.debug(f"Sending a message to USER: {key}")
                            name = self.database.check_records(message)
                            self.message['COMMAND'] = Commands.chat_commands['receive']
                            self.message['CLIENT'] = [message['CLIENT'], name]
                            self.message['DATA'] = message['DATA']

                            user_socket.send(json.dumps(self.message).encode())

                            self.message = {'COMMAND': "", 'CLIENT': [], 'DATA': []}

                    if message['COMMAND'] == Commands.REGISTER:
                        logging.info(">: Client requested to be registered to the database.")

                        if ServerCommands.register_user(message["DATA"], message['CLIENT'], self.database):
                            self.message["COMMAND"] = Commands.COMMAND_COMPLETED

                            client.send(json.dumps(self.message).encode())

                    if message['COMMAND'] == Commands.REFERRAL:
                        logging.info(">: Client requested a referral code from server.")
                        code = ServerCommands.generate_code(6)

                        self.message["COMMAND"] = Commands.REFERRAL
                        self.message["CLIENT"] = UserTypes.CLINICIAN
                        self.message["DATA"].append(code)

                        client.send(json.dumps(self.message).encode())

                    if message['COMMAND'] == Commands.VALIDATE_REGISTER:
                        found_results = self.database.check_records(message)
                        logging.debug(found_results)

                        if found_results:
                            self.message['COMMAND'] = Commands.COMMAND_FAILED
                            logging.debug(self.message)
                            client.send(json.dumps(self.message).encode())

                        elif not found_results:
                            self.message['COMMAND'] = Commands.COMMAND_PASSED
                            logging.debug(self.message)

                            client.send(json.dumps(self.message).encode())

                    if message['COMMAND'] == Commands.LOGIN:
                        logging.info(">: Server received request to validate login credentials.")
                        accept_login = ServerCommands.compare_login(message, self.database)

                        user_type = users[accept_login[0]]
                        user_id = accept_login[1][0]
                        logging.debug(f"User: {accept_login}")

                        if user_type is not None:
                            logging.info(f">: {accept_login[1]} is a {user_type}")

                            self.message['COMMAND'] = Commands.COMMAND_ACCEPT
                            self.message['CLIENT'] = user_id  # Set the client key to the user_id
                            self.message['DATA'] = [user_type, accept_login[1]]

                            self.connected_users[user_id] = client  # Add user that logged in, to the connected users.
                            logging.info(f"User: {self.connected_users[user_id]} has connected successfully.")

                            logging.debug(self.message)
                            client.send(json.dumps(self.message).encode())

                        else:
                            self.message['COMMAND'] = Commands.COMMAND_DENY
                            self.message['CLIENT'] = None
                            self.message['DATA'] = []

                            logging.debug(self.message)
                            client.send(json.dumps(self.message).encode())

            except socket.error as e:
                logging.error(f"Error while receiving data from client: {e}")
                break

    def setup_server(self):
        """
        Set up the server by binding to the socket.
        """

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()

            logging.info(f">: Server is successfully set up and listening on port: {self.port}")

        except socket.error as err:
            logging.error(f">: [SERVER]: Failed to set up server on HOST: {self.host}, PORT: {self.port}")
            logging.error(err)

            raise

    def start_listening(self):
        """
        Start listening for incoming client connections.
        """
        while True:
            try:
                self.client_connected, self.client_address = self.server_socket.accept()
                logging.info(f">: Accepted connection by Address: {self.client_address}")

                threading.Thread(target=self.handle_messages_from_client, args=(self.client_connected,)).start()
            except socket.error as err:
                logging.error(">: [SERVER]: Error accepting connection.")
                logging.error(err)


# INIT
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    app_server = Server('localhost', 50000)
    app_server.start_listening()
