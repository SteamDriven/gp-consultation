import logging
import random
import re
import string
from tkinter import messagebox

import customtkinter as ctk

from libclient import Client
from pages import LOGIN, PATIENT_DASHBOARD, data

port = 50000


class Commands:
    REGISTER = 'REGISTER'
    LOGIN = 'LOGIN'
    REFERRAL = 'REFERRAL'
    VALIDATE_REGISTER = 'VALIDATE REGISTER'


class UserTypes:
    CLINICIAN = 'CLINICIAN'
    PATIENT = 'PATIENT'


class ServerCommands:
    @staticmethod
    def get_referral(client):
        return client.handle_server_messages(Commands.REFERRAL, None, None)

    @staticmethod
    def validate_register(user_type, data, client):
        return client.handle_server_messages(Commands.VALIDATE_REGISTER, user_type, data)


class ClientCommands:
    @staticmethod
    def register(client, user_type, user_data):
        return client.handle_server_messages(Commands.REGISTER, user_type, user_data)

    @staticmethod
    def login(client, user_data):
        return client.handle_server_messages(Commands.LOGIN, None, user_data)


class Validator:
    @staticmethod
    def validate_email(email):
        """
        Validate an email address using a regular expression.
        """
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_password(password, confirm):
        """
        Compare two passwords to ensure they match.
        """
        return password == confirm

    @staticmethod
    def validate_name(name):
        """
        Validate a name based on various criteria.
        """
        if not isinstance(name, str) or len(name) < 2 or name.isnumeric() or not re.match('^[A-Z0-9._]*$', name):
            return False
        return True

    @staticmethod
    def validate_tel_no(no):
        """
        Validate a telephone number based on its length.
        """
        return len(no) == 11

    @staticmethod
    def validate_postcode(code):
        """
        Validate a postcode based on its length.
        """
        pattern = r"^[A-Z]{1,2}([0-9]{1,2}[" "][0-9][A-Z]{2}$"
        return bool(re.match(pattern, code))

    @staticmethod
    def validate_referral(user_input, referral):
        """
        Compare the user's input with the server's generated referral code.
        """
        return user_input == referral


class APP(ctk.CTk):
    def __init__(self, title, size, client):
        ctk.CTk.__init__(self)

        # Configurations
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.attributes('-fullscreen', True)
        self.client = client

        self.validations = Validator()
        self.server_commands = ServerCommands()
        self.client_commands = ClientCommands()

        # self.create_random_doctor()
        # self.create_random_patient()

        # Widgets
        container = ctk.CTkFrame(self)
        container.pack(expand=True, fill='both')

        # Functions
        self.frames = {}
        pages = [LOGIN, PATIENT_DASHBOARD]
        for F in pages:
            frame = F(container, self)

            self.frames[F] = frame

    # Using the method mentioned later in the class to display a specific frame upon opening
        self.show_frame(PATIENT_DASHBOARD)
    #
    # Display current frame using page as a parameter

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.pack(side="left", fill="both", expand=True)

        # Initialise
        self.mainloop()

    def handle_successful_login(self, user_type, dashboard_frame):
        logging.info(f">: {user_type} successfully logged in, switching to {user_type} Dashboard")
        messagebox.showinfo('Login', "Login was successful!")

        dashboard = dashboard_frame
        dashboard.user_type = user_type
        self.show_frame(dashboard)

    @staticmethod
    def handle_failed_login():
        logging.info(">: Client has requested to login. Server has denied access.")
        messagebox.showwarning('Login Error', "Login credentials do not exist!")

    def validate_login(self, data):
        if '' in data:
            messagebox.showwarning('Error', 'You need to fill in all the boxes.')
            return print('>: Not all boxes have been filled.')

        logging.info(">: Client has requested to login. Sending login data to server.")
        accepted = self.client_commands.login(self.client, data)
        action = accepted[0]

        if action == 'CHANGE TO PATIENT DASH':
            self.handle_successful_login(UserTypes.PATIENT, PATIENT_DASHBOARD)

        elif action == 'CHANGE TO CLINICIAN DASH':
            self.handle_successful_login(UserTypes.CLINICIAN, None)

        elif action == 'SHOW LOGIN WARNING':
            self.handle_failed_login()

        data.patient = accepted[1]

    @staticmethod
    def generate_user_data(user_type, server_commands):
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

    def create_random_doctor(self):
        print('Generating fake data')
        doctor_data = self.generate_user_data(UserTypes.CLINICIAN, Commands.REGISTER)

        print("Doctor Data:", doctor_data)

        ClientCommands.register(self.client, UserTypes.CLINICIAN, doctor_data)

    def create_random_patient(self):
        print('Generating fake data')
        patient_data = self.generate_user_data(UserTypes.PATIENT, Commands.REGISTER)

        print("Patient Data:", patient_data)

        ClientCommands.register(self.client, UserTypes.PATIENT, patient_data)


app_client = Client('localhost', port)
my_app = APP('Test_App', (1920, 1080), app_client)
