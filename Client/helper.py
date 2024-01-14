from tkinter import messagebox
from configs import *

import logging
import random
import string


class ClientCommands:
    @staticmethod
    def register(client, user_type, user_data):
        return client.handle_server_messages(Commands.packet_commands['register'], user_type, user_data)

    @staticmethod
    def login(client, user_data):
        return client.handle_server_messages(Commands.packet_commands['login'], None, user_data)

    @staticmethod
    def handle_chat(client, message, command, user):
        print(f">: User {user} has sent message: {message} with command: {command}")
        client.send_chat_message(message, command, user)

    @staticmethod
    def request_doctor(client):
        logging.info(f"Requesting available doctors from server.")
        return client.handle_server_messages(command=Commands.packet_commands['request doctor'], client=None, data=None)

    @staticmethod
    def handle_failed_login():
        logging.info(">: Client has requested to login. Server has denied access.")
        messagebox.showwarning('Login Error', "Login credentials do not exist!")

    @staticmethod
    def handle_successful_login(user_type):
        logging.info(f">: {user_type} successfully logged in, switching to {user_type} Dashboard")
        messagebox.showinfo('Login', "Login was successful!")

    @staticmethod
    def generate_user_data(user_type):
        """
        Generate user data dynamically based on user type (Doctor or Patient).
        """
        title_options = ['Mr', 'Miss', 'Mrs', 'Ms']

        user_data = {
            'title': random.choice(title_options),
            'first_name': ''.join(random.choices(string.ascii_uppercase, k=5)),
            'last_name': ''.join(random.choices(string.ascii_uppercase, k=8)),
            'email': f'{"".join(random.choices(string.ascii_lowercase, k=8))}@example.com',
            'tel_no': ''.join(random.choices(string.digits, k=11)),
            'postcode': ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
            'password': ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        }

        if user_type == UserTypes.CLINICIAN:
            user_data['title'] = 'DR'

        return user_data

    @staticmethod
    def set_appointment(client, command, user_data):
        print(">: Preparing info to setup appointment on server.")
        client.handle_server_messages(command, client, user_data)


