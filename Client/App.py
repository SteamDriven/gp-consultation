import logging
import random
import string
from tkinter import messagebox

import customtkinter as ctk

from Client.Pages.Dashboard.Dashboard import PatientDashboard, DoctorDashboard
from Client.Pages.Login import Login
from Client.Pages.Chat.Overview import ChatOverview
from libclient import Client
from methods import *
from helper import ClientCommands
from configs import *

client_port = 50000


class App(ctk.CTk):
    def __init__(self, title, size, client):
        ctk.CTk.__init__(self)

        # Configurations
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.attributes('-fullscreen', True)
        self.client = client
        self.frames = {}

        self.validations = Validator()
        self.client_commands = ClientCommands()
        self.user_data = None

        self.pages_list = {

            "login": Login,
            "chat": ChatOverview,
        }

        # self.create_random_doctor(1)
        # self.create_random_patient(1)

        # Widgets
        self.container = ctk.CTkFrame(self)
        self.container.pack(expand=True, fill='both')

        self.create_pages()

        # Functions

    def create_pages(self):
        for key, value in self.pages_list.items():
            self.frames[key] = value(self.container, self)

        ClientCommands.show_frame('login', self.frames)

    # def show_frame(self, cont: str, frame):
    #
    #     if cont not in self.frames and frame:
    #         self.frames[cont] = frame(self.container)
    #
    #     selected_page = self.frames[cont]
    #     for p in self.frames.values():
    #         if p:
    #             p.pack_forget()
    #
    #         selected_page.pack(side="top", fill="both", expand=True)
    #         selected_page.tkraise()

        # Initialise

        self.mainloop()

    def validate_login(self, data):
        if '' in data:
            messagebox.showwarning('Error', 'You need to fill in all the boxes.')
            return print('>: Not all boxes have been filled.')

        logging.info(">: Client has requested to login. Sending login data to server.")
        accepted = self.client_commands.login(self.client, data)
        print(f"{accepted} is the received login data.")
        command = accepted[0]
        info = accepted[1]

        if command == Commands.packet_commands['page commands']['change p']:
            ClientCommands.handle_successful_login(UserTypes.PATIENT)
            logging.info(f"Received login data: {info}")

            self.user_data = PatientData()
            self.user_data.user = info

            ClientCommands.add_page(PatientDashboard, (self.container, self, self.user_data, self.client), self.frames,
                                    'patient dashboard')
            ClientCommands.show_frame('patient dashboard', self.frames)

            # try:
            #     for f in self.frames.values():
            #         f.pack_forget()
            #
            #     frame = PatientDashboard(self.container, self, self.user_data, self.client)
            #     frame.pack(side="top", fill="both", expand=True)
            #     frame.tkraise()
            #
            # except Exception as e:
            #     print(f"Error in show_frame: {e}")

        elif command == Commands.packet_commands['page commands']['change d']:
            ClientCommands.handle_successful_login(UserTypes.CLINICIAN)
            logging.info(f"Received login data: {info}")

            self.user_data = DoctorData()
            self.user_data.user = info

            ClientCommands.add_page(DoctorDashboard, (self.container, self, self.user_data, self.client),
                                    self.frames, 'doctor dashboard')
            ClientCommands.show_frame('doctor dashboard', self.frames)

            # try:
            #     for f in self.frames.values():
            #         f.pack_forget()
            #
            #     frame = DoctorDashboard(self.container, self, self.user_data, self.client, self)
            #     frame.pack(side="top", fill="both", expand=True)
            #     frame.tkraise()
            #
            # except Exception as e:
            #     print(f"Error in show_frame: {e}")

        elif command == Commands.packet_commands['page commands']['warning']:
            ClientCommands.handle_failed_login()

    def create_random_doctor(self, amt):
        print('Generating fake data')

        for i in range(amt):
            doctor_data = ClientCommands.generate_user_data(UserTypes.CLINICIAN)

            print("Doctor Data:", doctor_data)

            ClientCommands.register(self.client, UserTypes.CLINICIAN, doctor_data)

    def create_random_patient(self, amt):
        print('Generating fake data')

        for i in range(amt):
            patient_data = ClientCommands.generate_user_data(UserTypes.PATIENT)

            print("Patient Data:", patient_data)

            ClientCommands.register(self.client, UserTypes.PATIENT, patient_data)

    def get_pages(self):
        return self.pages_list


app_client = Client('localhost', client_port)
my_app = App('Test_App', (1920, 1080), app_client)
