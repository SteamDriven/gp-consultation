import schedule

from database import *
from configs import UserTypes, Commands
from helper import *
from methods import *
from datetime import *

import socket
import json
import threading
import string
import random
import logging
import time


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
        self.client_address = None
        self.message = {"COMMAND": "", "CLIENT": None, "DATA": None}
        self.connected_users = {}
        self.query = ""
        self.query_data = []
        self.sent_notifications = set()

        self.active_sessions = self.load_active_sessions()

        self.database = Database('Olinic Management.db')
        self.setup_server()

        # schedule.every(10).seconds.do(self.check_upcoming_bookings)

    def save_active_sessions(self):
        with open('active_sessions.json', 'w') as file:
            json.dump(self.active_sessions, file)

    @staticmethod
    def load_active_sessions():
        try:
            with open('active_sessions.json', 'r') as file:
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def check_upcoming_bookings(self):
        print('checking upcoming bookings')
        upcoming_bookings = self.database.find_booking()

        for booking in upcoming_bookings:
            print(booking)
            booking_reference = booking[0]

            if booking_reference not in self.sent_notifications:
                patient_id = booking[1]
                clinician_id = booking[2]

                patient_details = self.database.find_patient(patient_id)
                clinician_details = self.database.find_doctor(clinician_id)

                patient_name = ' '.join(patient_details[1:]).title()
                clinician_name = ' '.join(clinician_details[1:]).title()

                booked_time = json.loads(booking[4])

                patient_msg = ServerCommands.format_paragraph(
                    f"Your appointment with Dr {clinician_name} is scheduled for {booked_time[0]}. "
                    f'The clinician will invite you to this via chat, so be sure to look out for an invite '
                    f'in your notifications tab shortly.', 120)

                clinician_msg = ServerCommands.format_paragraph(
                    f"You have an appointment with your patient {patient_name}, scheduled for {booked_time[0]}. "
                    f'You will receive a prompt to invite them for a chat via your notifications shortly.', 120)

                patient_notification = {
                    'identifier': self.database.generate_code(5),
                    'user': patient_id,
                    'message': ['Upcoming Appointment', patient_msg],
                    'time': ServerCommands.format_time(),
                    'status': 'Accepted',
                    'service': 'reminder',
                }
                self.database.store_notification(patient_notification)

                clinician_notification = {
                    'identifier': self.database.generate_code(5),
                    'user': clinician_id,
                    'message': ['Upcoming Appointment', clinician_msg, clinician_name, patient_details],
                    'time': ServerCommands.format_time(),
                    'status': 'Accepted',
                    'service': 'reminder',
                }
                self.database.store_notification(clinician_notification)

                self.sent_notifications.add(booking_reference)
                logging.info(f'Sent notification: {booking_reference}')

                self.active_sessions[booking_reference] = {
                    'clinician': [clinician_id, clinician_name],
                    'patient': [patient_id, patient_name],
                }

                self.save_active_sessions()
                logging.info(f"Successfully saved active booking into dict: {self.active_sessions}")

                clinician_notification = {
                    'identifier': self.database.generate_code(5),
                    'user': clinician_id,
                    'message': ['Start your chat session', clinician_msg, clinician_name, patient_details],
                    'time': ServerCommands.format_time(),
                    'status': 'Accepted',
                    'service': 'booking',
                }

                self.database.store_notification(clinician_notification)

    def stop_server(self):
        if self.server_socket:
            self.server_socket.close()
            print(f">: [SERVER]: Binding to socket on HOST: {self.host} has been severed!")

    def choose_random_doctor(self):
        doctors = self.database.request_doctors()
        available = []

        if doctors:
            for doctor in doctors:
                available.append(doctor)

        return random.choice(available)

    def get_connected_user(self, client):
        for key, user in self.connected_users.items():
            if user == client:
                return key

    def handle_messages_from_client(self, client):
        """
            Handle client requests and return information back.

            Args: client (socket.socket): Client socket object.
        """

        users = {-1: None, 1: UserTypes.PATIENT, 2: UserTypes.CLINICIAN}

        while True:
            try:
                data = client.recv(8192)

                if not data:
                    break

                else:
                    try:
                        message = json.loads(data.decode())

                        if message['COMMAND'] == Commands.packet_commands['notifications']['invite']:
                            patient_id = message['DATA'][1]
                            clinician = message['DATA'][0]

                            additional_info = ServerCommands.format_paragraph(('To accept this invitation and join the '
                                                                               'chat, please select the option'
                                                                               'below and you will be redirected.'),
                                                                              120)

                            notification = {
                                'identifier': self.database.generate_code(5),
                                'user': patient_id,
                                'message': [f'Dr {clinician} has invited you to a consultation.', additional_info],
                                'time': ServerCommands.format_time(),
                                'status': 'Accepted',
                                'service': 'consultation',
                            }

                            self.database.store_notification(notification)

                        if message['COMMAND'] == Commands.packet_commands['notifications']['send patient']:
                            doctor_id = self.get_connected_user(client)
                            doctor_data = self.database.find_doctor(doctor_id)

                            print(doctor_data)
                            doctor_name = ' '.join(doctor_data[1:]).title()
                            packet = message['DATA']

                            notification = {
                                'identifier': self.database.generate_code(5),
                                'user': packet[0],
                                'message': [f'Booking Accepted: Dr {doctor_name}', packet[1]],
                                'time': packet[2],
                                'status': packet[3],
                                'service': packet[4],
                            }

                            self.database.store_notification(notification)

                        if message['COMMAND'] == Commands.packet_commands['update b']:
                            col, new_val, patient, status = (message['DATA'][0], json.dumps(message['DATA'][1]), message['DATA'][2],
                                                             message['DATA'][3])
                            self.database.update_booking(col, new_val, patient, status)

                        if message['COMMAND'] == Commands.packet_commands['find b']:
                            booking_info = self.database.find_booking(message['DATA'])

                            self.message['COMMAND'] = Commands.packet_commands['find b']
                            self.message['CLIENT'] = None
                            self.message['DATA'] = booking_info

                            if booking_info:
                                client.send(json.dumps(self.message).encode())

                        if message['COMMAND'] == Commands.packet_commands['find p']:
                            patient_info = self.database.find_patient(message['DATA'])

                            self.message['COMMAND'] = Commands.packet_commands['find p']
                            self.message['CLIENT'] = None

                            if patient_info:
                                self.message['DATA'] = patient_info

                                client.send(json.dumps(self.message).encode())
                                logging.info(f"Server sent PATIENT: {self.message['DATA']} info to client.")

                            else:
                                logging.info(f"Server cannot find PATIENT: {message['DATA']}")
                                self.message['DATA'] = []
                                client.send(json.dumps(self.message).encode())

                        if message['COMMAND'] == Commands.packet_commands['notifications']['search']:
                            print('Received request for searching.')
                            user_id = ServerCommands.find_user(self.connected_users, client)
                            logging.info(f"Received USER: {user_id}'s request for new notifications. Searching...")

                            notifications = self.database.return_notifications(user_id)
                            print(f'found {notifications}')

                            self.message['COMMAND'] = Commands.packet_commands['notifications']['send']
                            self.message['CLIENT'] = user_id

                            if notifications is not None:
                                logging.info(f"Received USER: {user_id}'s notifications. They have {len(notifications)}"
                                             f" new notifications.")

                                self.message['DATA'] = notifications

                                encoded_message = json.dumps(self.message)

                                print("Encoded Message:", encoded_message)
                                print("Encoded Message Length:", len(encoded_message))

                                client.send(encoded_message.encode())
                                logging.debug("Sending client their notifications...")

                            else:
                                self.message['DATA'] = []

                                client.send(json.dumps(self.message).encode())
                                logging.debug("Client has no notifications.")

                        if message['COMMAND'] == Commands.packet_commands['appointments']['create apt']:
                            logging.info(f">: Received {message['CLIENT']}'s booking data. Registering to database.")

                            user_data = PatientData().from_dict(message['DATA'])

                            patient_to_assign = message['DATA']['user']
                            doctor_to_assign = message['DATA']['assigned_doctor']

                            if doctor_to_assign is None:
                                doctor_to_assign = self.choose_random_doctor()
                                logging.info(f'Assigned random available doctor: {doctor_to_assign} to user:'
                                             f'{patient_to_assign}')

                            date_of_appt = message['DATA']['selected_day']
                            time_of_appt = message['DATA']['selected_time']
                            symptoms = message['DATA']['symptoms']
                            images = message['DATA']['images']

                            doctor_id = doctor_to_assign[1][0]
                            doctor_name = ' '.join(doctor_to_assign[1][1:]).title()
                            patient_id = patient_to_assign[1][0]
                            patient_name = ' '.join(patient_to_assign[1][1:]).title()

                            print(doctor_name, patient_name)

                            data_packet = {
                                'doctor': doctor_id,
                                'patient': patient_id,
                                'date': date_of_appt,
                                'time': time_of_appt,
                            }

                            booking = self.database.create_booking(data_packet)
                            logging.info("Data packet for booking has been sent for registration.")

                            if booking:
                                logging.info(f"Sending notification request to Doctor: {data_packet['doctor']}\n"
                                             f"Sending notification alert to Patient: {data_packet['patient']}\n"
                                             f"Switching USER: {data_packet['patient']}'s screen\n"
                                             f"to current appointments")

                                doctor_message = (f"You have been requested for an appointment by Patient: "
                                                  f"{patient_name} {patient_id}"
                                                  f"The time of the appointment is: {time_of_appt}\n and the date "
                                                  f"is: {date_of_appt}.")

                                patient_message = (f"You have scheduled a request for an appointment with Dr "
                                                   f"{doctor_name} {doctor_id}. "
                                                   f"The appointment is set for {date_of_appt} at {time_of_appt}.\n"
                                                   f"You will receive a confirmation upon acceptance of your "
                                                   f"appointment.")

                                status = 'Pending'
                                current_timestamp = ServerCommands.format_time()

                                doctor_message = ServerCommands.format_paragraph(doctor_message, 120)
                                patient_message = ServerCommands.format_paragraph(patient_message, 120)

                                doctor_notification = {
                                    'identifier': self.database.generate_code(5),
                                    'user': doctor_id,
                                    'message': [f'New Booking: Dr {doctor_name}', doctor_message, patient_id,
                                                symptoms, images],
                                    'time': current_timestamp,
                                    'status': status,
                                    'service': 'patient',
                                }

                                patient_notification = {
                                    'identifier': self.database.generate_code(5),
                                    'user': patient_id,
                                    'message': [f'New Booking: {patient_name}', patient_message],
                                    'time': current_timestamp,
                                    'status': status,
                                    'service': 'system',
                                }

                                self.database.store_notification(doctor_notification)
                                self.database.store_notification(patient_notification)

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
                            current_user = self.get_connected_user(client)
                            print(current_user)
                            message_data = message['DATA']

                            logging.info(f"Received message: {message_data} from user: {current_user}")
                            print(self.active_sessions)

                            for booking_ref, roles in self.active_sessions.items():
                                clinician_id, clinician_name = roles.get('clinician', [None, None])
                                patient_id, patient_name = roles.get('patient', [None, None])

                                print(clinician_id, clinician_name, patient_id, patient_name)

                                if current_user in [clinician_id, patient_id]:
                                    logging.info(f'Checking what role user: {current_user} is.')

                                    if current_user == clinician_id:
                                        role = 'Doctor'
                                        name = clinician_name
                                        recipient = [patient_id, patient_name]
                                        logging.info(f'Clinician: {current_user} is sending to patient: {recipient}')

                                    else:
                                        role = 'Patient'
                                        name = patient_name
                                        recipient = [clinician_id, clinician_name]
                                        logging.info(f'Patient: {current_user} is sending to clinician: {recipient}')

                                    self.message['COMMAND'] = Commands.chat_commands['receive']
                                    self.message['CLIENT'] = recipient[0]
                                    self.message['DATA'] = [role, name, message_data]

                                    self.connected_users[recipient[0]].send(json.dumps(self.message).encode())
                                    current_user = None

                                else:
                                    logging.info(f"User {current_user} was not found in any active session")

                        if message['COMMAND'] == Commands.packet_commands['register']:
                            logging.info(">: Client requested to be registered to the database.")

                            if ServerCommands.register_user(message["DATA"], message['CLIENT'], db=self.database):
                                self.message["COMMAND"] = Commands.packet_commands['complete']

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

                            print(accept_login)

                            user_type = users[accept_login[0]]
                            # user_id = users[accept_login[1][0]]
                            logging.debug(f"User: {accept_login}")

                            if user_type is not None:
                                logging.info(f">: {accept_login[1]} is a {user_type}")
                                user_id = accept_login[1][0]

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

                    except json.JSONDecodeError as err:
                        logging.warning(f'Error decoding JSON: {e}')
                        logging.warning(f'Received data: {data.decode()}')
                        raise

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

    def execute(self):
        # schedule_thread = threading.Thread(target=self.start_schedule)
        # schedule_thread.start()

        self.start_listening()

    def start_schedule(self):
        while not self.end:
            schedule.run_pending()
            time.sleep(1)

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
    app_server.execute()
