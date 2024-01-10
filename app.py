import logging
import random
import re
import string
from tkinter import messagebox

import customtkinter as ctk

from libclient import Client
from pages import LOGIN, PATIENT_DASHBOARD, DOCTOR_DASHBOARD
from methods import ServerCommands, ClientCommands, Validator, appointmentData
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
        self.frames = {}

        self.validations = Validator()
        self.server_commands = ServerCommands()
        self.client_commands = ClientCommands()
        self.user_data = appointmentData()

        self.pages_list = {
            "login": LOGIN,
            # "doctor": DOCTOR_DASHBOARD,
        }

        # self.create_random_doctor()
        # self.create_random_patient()

        # Widgets
        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True, fill='both')

        self.create_pages()

        # Functions
    def create_pages(self):
        for key, value in self.pages_list.items():
            self.frames[key] = value(self.container, self)

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

    def validate_login(self, data):
        if '' in data:
            messagebox.showwarning('Error', 'You need to fill in all the boxes.')
            return print('>: Not all boxes have been filled.')

        logging.info(">: Client has requested to login. Sending login data to server.")
        accepted = self.client_commands.login(self.client, data)
        command = accepted[0]
        info = accepted[1]

        if command == 'CHANGE TO PATIENT DASH':
            ClientCommands.handle_successful_login(UserTypes.PATIENT)
            logging.info(f"Received login data: {info}")
            self.user_data.user = f"PATIENT: {' '.join(info[1])}"

            try:
                for f in self.frames.values():
                    f.pack_forget()

                frame = PATIENT_DASHBOARD(self.container, self, self.user_data, self.client)
                frame.pack(side="top", fill="both", expand=True)
                frame.tkraise()

            except Exception as e:
                print(f"Error in show_frame: {e}")

        # elif accepted[0] == 'CHANGE TO CLINICIAN DASH':
        #     ClientCommands.handle_successful_login(UserTypes.CLINICIAN)
        #     self.user_data.user = accepted[1]
        #     self.show_frame('doctor')

        elif command == 'SHOW LOGIN WARNING':
            ClientCommands.handle_failed_login()

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

    def create_random_doctor(self):
        print('Generating fake data')
        doctor_data = self.generate_user_data(UserTypes.CLINICIAN)

        print("Doctor Data:", doctor_data)

        ClientCommands.register(self.client, UserTypes.CLINICIAN, doctor_data)

    def create_random_patient(self):
        print('Generating fake data')
        patient_data = self.generate_user_data(UserTypes.PATIENT)

        print("Patient Data:", patient_data)

        ClientCommands.register(self.client, UserTypes.PATIENT, patient_data)


app_client = Client('localhost', port)
my_app = APP('Test_App', (1920, 1080), app_client)
