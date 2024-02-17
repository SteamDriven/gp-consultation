import json
import textwrap
from datetime import datetime
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
    def handle_chat(client, message, command):
        client.send_chat_message(message, command)

    @staticmethod
    def update_notes(command, client):
        return client.handle_server_messages(command, None, None)

    @staticmethod
    def request_doctor(client):
        logging.info(f"Requesting available doctors from server.")
        return client.handle_server_messages(command=Commands.packet_commands['request doctor'], client=None, data=None)

    @staticmethod
    def update_booking(client, packet):
        logging.info("Request to update bookings table.")
        return client.handle_server_messages(command=Commands.packet_commands['update b'], client=None, data=packet,
                                             receive=False)

    @staticmethod
    def send_patient_notification(client, packet):
        client.handle_server_messages(command=Commands.packet_commands['notifications']['send patient'], client=None,
                                      data=packet, receive=False)

    @staticmethod
    def send_notification(client, packet, command):
        client.handle_server_messages(command=Commands.packet_commands['notifications'][command], client=None,
                                      data=packet, receive=False)

    @staticmethod
    def generate_id():
        """
           Generate a unique user ID.

           Returns:
               int: Unique user ID.
        """
        return random.randint(10000, 99999)

    @staticmethod
    def format_time():
        now = datetime.now()
        formatted_time = now.strftime('%d %b %Y at %I:%M %p')
        return formatted_time

    @staticmethod
    def format_paragraph(input_string, width):
        if len(input_string) < width:
            return input_string
        else:
            return textwrap.fill(input_string, width=width)

    @staticmethod
    def convert_to_minutes(time_str):
        # Convert a time string (e.g., '1:30') to minutes
        time_str = time_str.replace(' AM', '').replace(' PM', '')
        hours, minutes = map(int, time_str.split(':'))

        if 'PM' in time_str:
            hours += 12

        return hours * 60 + minutes

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
    def set_appointment(client, role, command, user_data):
        print(">: Preparing info to setup appointment on server.")
        client.handle_server_messages(command, role, user_data, False)

    @staticmethod
    def show_frame(cont: str, my_dict, callback=None):
        if not my_dict[cont]:
            logging.warning(f"Frame '{cont}' not found in the dictionary.")
            return

        selected_page = my_dict[cont]
        try:
            for p in my_dict.values():
                print(p)
                if p and p.winfo_exists():
                    p.pack_forget()

            if cont == 'notifications':
                selected_page.update_notifications()

            selected_page.pack(side="top", fill="both", expand=True)
            selected_page.tkraise()

        except Exception as e:
            logging.warning(f"Error displaying {cont}: {e}")
            raise

    @staticmethod
    def add_page(frame, values, my_dict, cont: str):
        my_dict[cont] = frame(*values)
