from database import *
from configs import UserTypes, Commands
from helper import *
from methods import *

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

                    if message['COMMAND'] == Commands.packet_commands['appointments']['create apt']:
                        logging.info(f">: Received {message['CLIENT']}'s booking data. Registering to database.")

                        user_data = PatientData().from_dict(message['DATA'])

                        doctor_to_assign = message['DATA']['assigned_doctor']
                        patient_to_assign = message['DATA']['user']
                        date_of_appt = message['DATA']['selected_day']
                        time_of_appt = message['DATA']['selected_time']
                        symptoms = message['DATA']['symptoms']
                        images = message['DATA']['images']

                        doctor_id = doctor_to_assign[1][0]
                        patient_id = patient_to_assign[1][0]

                        data_packet = {
                            'doctor': doctor_id,
                            'patient': patient_id,
                            'date': date_of_appt,
                            'time': time_of_appt,
                            'd_not': 0,  # To indicate by default that both the doctor and client are not connected.
                            'c_not': 0
                        }

                        booking = self.database.create_booking(data_packet)
                        logging.info("Data packet for booking has been sent for registration.")

                        if booking:
                            logging.info(f"Sending notification request to Doctor: {data_packet['doctor']}\n"
                                         f"Sending notification alert to Patient: {data_packet['patient']}\n"
                                         f"Switching USER: {data_packet['patient']}'s screen\n"
                                         f"to current appointments")

                            doctor_message = (f"You have been requested for an appointment by Patient: "
                                              f"{patient_to_assign}\n"
                                              f"The time of the appointment is: {time_of_appt} and the date\n"
                                              f"is: {date_of_appt}.")

                            patient_message = (f"You have scheduled a request for an appointment with DR"
                                               f"{doctor_to_assign}\n"
                                               f"The appointment is set for {date_of_appt} at {time_of_appt}.\n"
                                               f"You will receive a confirmation upon acceptance of your appointment.")

                            # Now attempt to send a notification separately to both the doctor and client.
                            # If either party is not currently connected, don't adjust database.
                            for identifier, user in self.connected_users.items():
                                if int(doctor_id) == identifier:
                                    self.message['COMMAND'] = Commands.packet_commands['notifications']['send doctor']
                                    self.message['CLIENT'] = doctor_id
                                    self.message['DATA'] = [UserTypes.CLINICIAN, patient_id, doctor_message]

                                    self.database.sql = '''UPDATE BOOKINGS SET D_NOT = 1 WHERE Booking_ID = ?'''
                                    self.database.query(self.database.sql, (booking,))
                                    logging.info(f"Bookings has been updated, as DR {doctor_to_assign} is online to "
                                                 "receive notification.")

                                    user.send(json.dumps(self.message).encode())
                                    logging.info(f"Notification has been sent to DR: {doctor_to_assign}.")
                                else:
                                    logging.info(f"DR {doctor_to_assign} is not online, notification will be sent"
                                                 f"at their next available convenience.")

                                if patient_id == identifier:
                                    self.message['COMMAND'] = Commands.packet_commands['notifications']['send patient']
                                    self.message['CLIENT'] = patient_id
                                    self.message['DATA'] = [UserTypes.PATIENT, patient_message]

                                    self.database.sql = '''UPDATE BOOKINGS SET C_NOT = 1 WHERE Booking_ID = ?'''
                                    self.database.query(self.database.sql, (booking,))
                                    logging.info(f"Bookings has been updated, as PATIENT {patient_to_assign} is online "
                                                 "to receive notification.")

                                    user.send(json.dumps(self.message).encode())
                                    logging.info(f"Notification has been sent to PATIENT: {patient_to_assign}.")
                                else:
                                    logging.info(f"PATIENT {patient_to_assign} is not online, notification will be sent"
                                                 f"at their next available convenience.")

                    if message['COMMAND'] == Commands.packet_commands['request doctor']:
                        logging.info(">: Server received request to find available doctors.")
                        print('>: Server received request to find available doctors.')
                        doctors = self.database.request_doctors()

                        if doctors:
                            self.message['COMMAND'] = Commands.packet_commands['return doctor']
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

                    if message['COMMAND'] == Commands.packet_commands['register']:
                        logging.info(">: Client requested to be registered to the database.")

                        if ServerCommands.register_user(message["DATA"], message['CLIENT'], db=self.database):
                            self.message["COMMAND"] = Commands.packet_commands['complete']

                            client.send(json.dumps(self.message).encode())

                    if message['COMMAND'] == Commands.packet_commands['referral']:
                        logging.info(">: Client requested a referral code from server.")
                        code = ServerCommands.generate_code(6)

                        self.message["COMMAND"] = Commands.packet_commands['referral']
                        self.message["CLIENT"] = UserTypes.CLINICIAN
                        self.message["DATA"].append(code)

                        client.send(json.dumps(self.message).encode())

                    if message['COMMAND'] == Commands.packet_commands['validate register']:
                        found_results = self.database.check_records(message)
                        logging.debug(found_results)

                        if found_results:
                            self.message['COMMAND'] = Commands.packet_commands['fail']
                            logging.debug(self.message)
                            client.send(json.dumps(self.message).encode())

                        elif not found_results:
                            self.message['COMMAND'] = Commands.packet_commands['pass']
                            logging.debug(self.message)

                            client.send(json.dumps(self.message).encode())

                    if message['COMMAND'] == Commands.packet_commands['login']:
                        logging.info(">: Server received request to validate login credentials.")
                        accept_login = ServerCommands.compare_login(message, self.database)

                        user_type = users[accept_login[0]]
                        user_id = accept_login[1][0]
                        logging.debug(f"User: {accept_login}")

                        if user_type is not None:
                            logging.info(f">: {accept_login[1]} is a {user_type}")

                            self.message['COMMAND'] = Commands.packet_commands['accept']
                            self.message['CLIENT'] = user_id  # Set the client key to the user_id
                            self.message['DATA'] = [user_type, accept_login[1]]

                            self.connected_users[user_id] = client  # Add user that logged in, to the connected users.
                            logging.info(f"User: {self.connected_users[user_id]} has connected successfully.")

                            logging.debug(self.message)
                            client.send(json.dumps(self.message).encode())

                        else:
                            self.message['COMMAND'] = Commands.packet_commands['deny']
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
