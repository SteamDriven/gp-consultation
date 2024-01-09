import logging
import random
import re
import string
from tkinter import messagebox

import customtkinter as ctk

from libclient import Client
from pages import LOGIN, PATIENT_DASHBOARD
from methods import ServerCommands, ClientCommands, Validator, appt_data
from configs import UserTypes, Commands

port = 50000


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

        self.pages_list = {
            "login": LOGIN,
            "patient_dash": PATIENT_DASHBOARD,
        }

        # self.create_random_doctor()
        # self.create_random_patient()

        # Widgets
        container = ctk.CTkFrame(self)
        container.pack(expand=True, fill='both')

        # Functions
        self.frames = {}
        for key, value in self.pages_list.items():
            self.frames[key] = value(container, self)

        # Using the method mentioned later in the class to display a specific frame upon opening
        self.show_frame('login')

    #
    # Display current frame using page as a parameter

    def show_frame(self, cont: str):
        frame = self.frames[cont]
        print('Displaying frame:', cont)

        try:
            for f in self.frames.values():
                f.pack_forget()

            frame.pack(side="top", fill="both", expand=True)
            frame.tkraise()

        except Exception as e:
            print(f"Error in show_frame: {e}")

        # Initialise
        self.mainloop()

    def handle_successful_login(self, user_type, dashboard_frame, user):
        logging.info(f">: {user_type} successfully logged in, switching to {user_type} Dashboard")
        messagebox.showinfo('Login', "Login was successful!")

        self.frames[dashboard_frame].create_widgets()
        self.frames[dashboard_frame].configure_menu()
        self.frames[dashboard_frame].place_widgets()
        self.frames[dashboard_frame].create_pages()
        self.frames[dashboard_frame].user_lbl.configure(text=user)
        self.frames[dashboard_frame].show_frame('request_app')
        self.show_frame(dashboard_frame)

        appt_data.user = user

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
            print(accepted)
            self.handle_successful_login(UserTypes.PATIENT, 'patient_dash', accepted[1])

        elif action == 'CHANGE TO CLINICIAN DASH':
            self.handle_successful_login(UserTypes.CLINICIAN, None)

        elif action == 'SHOW LOGIN WARNING':
            self.handle_failed_login()

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
