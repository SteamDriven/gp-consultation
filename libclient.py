import socket
import json
from time import sleep
import logging


class Client:
    COMMAND_REFERRAL = 'REFERRAL'
    COMMAND_END = 'END'
    COMMAND_COMPLETED = 'COMPLETED'
    COMMAND_PASSED = 'PASSED'
    COMMAND_FAILED = 'FAILED'
    COMMAND_ACCEPT = 'ACCEPT'
    COMMAND_DENY = 'DENY'

    USER_ROLE_CLINICIAN = 'CLINICIAN'
    USER_ROLE_PATIENT = 'PATIENT'

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

    def send_message(self, command, client, data):
        message = {"COMMAND": command, "CLIENT": client, "DATA": data}
        logging.debug(message)
        self.client_socket.send(json.dumps(message).encode())

    def receive_message(self):
        try:
            received_data = self.client_socket.recv(1024).decode()

            if not received_data:
                return None
            return json.loads(received_data)

        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON: {e}")
            return None

    def handle_server_messages(self, command, client, data):
        self.send_message(command, client, data)
        received = self.receive_message()

        if received["COMMAND"] == self.COMMAND_REFERRAL:
            return received["DATA"]

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

            if received['CLIENT'] == self.USER_ROLE_PATIENT:
                logging.info('Changing to patient dash.')
                return ['CHANGE TO PATIENT DASH', received['DATA']]

            if received['CLIENT'] == self.USER_ROLE_CLINICIAN:
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
