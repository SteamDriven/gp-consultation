from configs import *

import socket
import json
import logging


class Client:
    COMMAND_REFERRAL = 'REFERRAL'
    COMMAND_END = 'END'
    COMMAND_COMPLETED = 'COMPLETED'
    COMMAND_PASSED = 'PASSED'
    COMMAND_FAILED = 'FAILED'
    COMMAND_ACCEPT = 'ACCEPT'
    COMMAND_DENY = 'DENY'

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect_to_socket()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.handle_close()

    def handle_close(self):
        if self.client_socket:
            self.client_socket.close()
            logging.info(f">: Connection to socket on HOST {self.host} has been closed!")

    def send_chat_message(self, message, command, user):
        if command == Commands.chat_commands['broadcast']:
            self.handle_server_messages(Commands.chat_commands['broadcast'], user, message, False)

        elif command == Commands.chat_commands['announcement']:
            self.handle_server_messages(Commands.chat_commands['announcement'], None, message, False)

    def send_message(self, command, client, data):
        try:
            message = {"COMMAND": command, "CLIENT": client, "DATA": data}
            self.client_socket.send(json.dumps(message).encode())

        except (socket.error, ConnectionError) as e:
            logging.error(f"Failed to send message {e}")

    def receive_message(self):
        try:
            received_data = self.client_socket.recv(1024).decode()

            if not received_data:
                return None
            return json.loads(received_data)

        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON: {e}")
            return None

    def handle_server_messages(self, command, client, data, receive=True):
        self.send_message(command, client, data)

        if receive:
            received = self.receive_message()

            if received["COMMAND"] == self.COMMAND_REFERRAL:
                return received["DATA"]

            if received['COMMAND'] == Commands.chat_commands['receive']:
                logging.info(f"Message: {received['DATA']} received from USER: {received['CLIENT']}")

            if received["COMMAND"] == self.COMMAND_END:
                self.handle_close()

            if received["COMMAND"] == self.COMMAND_COMPLETED:
                return 'CHANGE TO LOGIN'

            if received['COMMAND'] == self.COMMAND_PASSED:
                return 'ACCEPT'

            if received['COMMAND'] == self.COMMAND_FAILED:
                return 'DECLINE'

            if received['COMMAND'] == self.COMMAND_ACCEPT:
                logging.info('>: Login was accepted.')

                if received['CLIENT']:
                    if received['DATA'][0] == UserTypes.PATIENT:
                        logging.info('Changing to patient dash.')
                        return ['CHANGE TO PATIENT DASH', received['DATA']]

                    elif received['DATA'][0] == UserTypes.PATIENT:
                        logging.info('Changing to clinician dash.')
                        return ['CHANGE TO CLINICIAN DASH', received['DATA']]

            if received['COMMAND'] == self.COMMAND_DENY:
                logging.info('Login request was denied by server.')
                return ['SHOW LOGIN WARNING', False]

    def connect_to_socket(self):

        try:
            self.client_socket.connect((self.host, self.port))
            logging.info(f">: Client has connected successfully on PORT: {self.port}")

        except socket.error as err:
            logging.error(f">: Failed to connect to socket on HOST: {self.host}")
            logging.error(err)
