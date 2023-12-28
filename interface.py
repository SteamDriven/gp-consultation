import tkinter
import customtkinter as ctk
import socket
import json
import re
from tkinter import messagebox
from tkinter import ttk
import phonenumbers
import string
import random
from libclient import Client

# CONFIGURATIONS
port = 50000

ctk.set_default_color_theme('blue')
ctk.set_appearance_mode('light')


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


class App(ctk.CTk):  # App class that will be the primary window for the Registration and Login process
    def __init__(self, title, size, client):
        ctk.CTk.__init__(self)

        # Settings configurations
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.attributes('-fullscreen', True)
        self.client = client

        self.validations = Validator()
        self.server_commands = ServerCommands()
        self.client_commands = ClientCommands()

        self.cur_user = []

        self.referral = self.server_commands.get_referral(self.client)
        print(self.referral)  # Generating a referral code for the client for testing purposes

        container = ctk.CTkFrame(self)
        container.pack(expand=True, fill='both')

        # Creating a grid layout for the container in order to place widgets strategically
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Generate and register doctor and patient data
        # self.register_doctor_and_patient()

        self.frames = {}
        pages = [Login, Doctor_Registration, Patient_Registration, Doctor_Dashboard, Patient_Dashboard]
        for F in pages:
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using the method mentioned later in the class to display a specific frame upon opening
        self.show_frame(Login)

    # Display current frame using page as a parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        # Initialise
        self.mainloop()

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

    def register_doctor_and_patient(self):
        print('Generating fake data')
        doctor_data = self.generate_user_data(UserTypes.CLINICIAN, Commands.REGISTER)
        patient_data = self.generate_user_data(UserTypes.PATIENT, Commands.REGISTER)

        print("Doctor Data:", doctor_data)
        print("Patient Data:", patient_data)

        ClientCommands.register(self.client, UserTypes.CLINICIAN, doctor_data)
        ClientCommands.register(self.client, UserTypes.PATIENT, patient_data)

    def handle_successful_login(self, user_type, dashboard_frame):
        print(f">: {user_type} successfully logged in, switching to {user_type} Dashboard")
        messagebox.showinfo('Login', "Login was successful!")
        self.show_frame(dashboard_frame)

    def handle_failed_login(self):
        print(">: Client has requested to login. Server has denied access.")
        messagebox.showwarning('Login Error', "Login credentials do not exist!")
        self.destroy()
        self.__init__('Olinic Management', (1920, 1080))

    def check_for_existing_credentials(self, data):
        if data[0] == 'DR':
            server_check = self.server_commands.validate_register(self.client, UserTypes.CLINICIAN, data)
        else:
            server_check = self.server_commands.validate_register(self.client, UserTypes.PATIENT, data)

        if server_check == 'DECLINE':
            messagebox.showwarning('Error', 'Email and/or Telephone number already exists.')
            return False

        elif server_check == 'ACCEPT':
            return True

    def validate_credentials(self, data):
        if not self.check_for_existing_credentials(data):
            return False
        errors = []

        if any(value == '' for value in data):
            messagebox.showwarning('Error', 'You need to fill in all the boxes.')
            return print('>: Not all boxes have been filled.')

        if not self.validations.validate_name(data[1]):
            errors.append('Invalid first name')
        if not self.validations.validate_name(data[2]):
            errors.append('Invalid last name')
        if not self.validations.validate_email(data[3]):
            errors.append('Invalid email address')
        if not self.validations.validate_tel_no(data[4]):
            errors.append('Invalid phone number')
        if not self.validations.validate_postcode(data[5]):
            errors.append('Invalid postcode')

        if data[0] == 'DR':
            if not self.validations.validate_referral(data[8], self.referral):
                errors.append('Invalid referral code.')

        if not self.validations.validate_password(data[6], data[7]):
            errors.append('Passwords do not match.')

        return errors

    def check_credentials(self, data):
        errors = self.validate_credentials(data)
        if not errors:
            self.show_frame(Login)

        if errors:
            messagebox.showwarning('Error', '\n'.join(errors))
            return

        if data[0] == 'DR':
            user_type = UserTypes.CLINICIAN
        else:
            user_type = UserTypes.PATIENT

        # Registration complete, notify the user
        messagebox.showinfo('Registration', 'Registration Complete!')

        # Send registration request to the server
        change = app_client.handle_server_messages(Commands.REGISTER, user_type, data)
        if change == 'CHANGE TO LOGIN':
            self.show_frame(Login)

    def validate_login(self, data):
        if '' in data:
            messagebox.showwarning('Error', 'You need to fill in all the boxes.')
            return print('>: Not all boxes have been filled.')

        print(">: Client has requested to login. Sending login data to server.")
        accepted = self.client_commands.login(data)
        action = accepted[0]

        if action == 'CHANGE TO PATIENT DASH':
            self.handle_successful_login(UserTypes.PATIENT, Patient_Dashboard)

        elif action == 'CHANGE TO CLINICIAN DASH':
            self.handle_successful_login(UserTypes.CLINICIAN, Doctor_Dashboard)

        elif action == 'SHOW LOGIN WARNING':
            self.handle_failed_login()

        self.cur_user = accepted[1]
        print(self.cur_user)


class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.frames = {}
        self.pages_list = []

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2), weight=1)

    def setup_pages(self, container):
        for F in self.pages_list:
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    # Display current frame using page as a parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Login(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        # Configurations
        self.remember_client = False

        #  Widgets
        self.container = ctk.CTkFrame(self, fg_color='white', height=550, width=450, corner_radius=5)
        self.o_label = ctk.CTkLabel(self.container, text='O', text_color='#1a99de', font=('Arial bold', 40))
        self.c_label = ctk.CTkLabel(self.container, text='-CLINIC', text_color='#343434',
                                    font=('Arial Bold Italic', 30))
        self.seperator = ttk.Separator(self.container, orient='horizontal')
        self.seperator2 = ttk.Separator(self.container, orient='horizontal')
        self.label = ctk.CTkLabel(self.container, text='Login', text_color='#444343', font=('Arial Bold', 35))

        self.username = ctk.CTkEntry(
            self.container,
            placeholder_text='Email address',
            font=('Arial Light', 15),
            width=320,
            height=40,
            text_color='black',
            corner_radius=1)

        self.password = ctk.CTkEntry(
            self.container,
            placeholder_text='Password',
            font=('Arial Light', 15),
            width=320,
            height=40,
            text_color='black',
            corner_radius=1,
            show='*')

        self.remember_check = ctk.CTkCheckBox(
            self.container,
            text='Remember me?',
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            font=('Arial light', 15)

        )

        self.submit = ctk.CTkButton(
            self.container,
            text='Log in',
            font=('Arial bold', 20),
            text_color='white',
            width=320,
            height=55,
            corner_radius=3,
            # command=lambda: controller.show_frame(Doctor_Dashboard)
            command=lambda: controller.validate_login(
                [self.username.get(), self.password.get()]
            )
        )

        self.label2 = ctk.CTkLabel(self.container, text="Don't have an account?", text_color='black',
                                   font=("Arial Light", 15))

        self.register_bt = ctk.CTkButton(self.container, text='Register now', fg_color='white', text_color='#1a99de',
                                         font=('Arial bold', 15), width=15, hover=False,
                                         command=lambda: controller.show_frame(Doctor_Registration))

        self.label3 = ctk.CTkLabel(self.container, text="Registering as new patient?", text_color='black',
                                   font=('Arial light', 15))

        self.reg_patient_bt = ctk.CTkButton(self.container, text='Register here', fg_color='white',
                                            text_color='#1a99de',
                                            font=("Arial bold", 15), width=15, hover=False,
                                            command=lambda: controller.show_frame(Patient_Registration))

        self.container.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.o_label.place(relx=0.38, rely=0.1, anchor=tkinter.CENTER)
        self.c_label.place(relx=0.54, rely=0.1, anchor=tkinter.CENTER)
        self.seperator.place(relx=0.2, rely=0.205, relwidth=0.28, relheight=0.003, anchor=tkinter.CENTER)
        self.seperator2.place(relx=0.8, rely=0.205, relwidth=0.28, relheight=0.003, anchor=tkinter.CENTER)
        self.label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
        self.username.place(relx=0.5, rely=0.36, anchor=tkinter.CENTER)
        self.password.place(relx=0.5, rely=0.46, anchor=tkinter.CENTER)
        self.remember_check.place(relx=0.3, rely=0.54, anchor=tkinter.CENTER)
        self.submit.place(relx=0.5, rely=0.66, anchor=tkinter.CENTER)
        self.label2.place(relx=0.37, rely=0.76, anchor=tkinter.CENTER)
        self.register_bt.place(relx=0.67, rely=0.76, anchor=tkinter.CENTER)
        self.label3.place(relx=0.35, rely=0.81, anchor=tkinter.CENTER)
        self.reg_patient_bt.place(relx=0.69, rely=0.81, anchor=tkinter.CENTER)


class Doctor_Registration(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        # Create all the necessary widgets for this page
        self.container = ctk.CTkFrame(self, fg_color='white', height=800, width=600, corner_radius=5)
        self.seperator = ttk.Separator(self.container, orient='horizontal')
        self.seperator2 = ttk.Separator(self.container, orient='horizontal')
        self.label = ctk.CTkLabel(self.container, text='Doctor Registration', text_color='#444343',
                                  font=('Arial bold', 20))

        self.first_name = ctk.CTkEntry(
            self.container,
            placeholder_text='First name',
            font=('Arial Bold', 15),
            corner_radius=1
        )

        self.last_name = ctk.CTkEntry(
            self.container,
            placeholder_text='Surname',
            font=('Arial Bold', 15),
            corner_radius=1
        )

        self.email = ctk.CTkEntry(
            self.container,
            placeholder_text='Email address',
            font=('Arial Bold', 15),
            corner_radius=1
        )

        self.tel_no = ctk.CTkEntry(
            self.container,
            placeholder_text='Telephone number',
            font=('Arial Bold', 15),
            corner_radius=1
        )

        self.password = ctk.CTkEntry(
            self.container,
            placeholder_text='New password',
            font=('Arial Bold', 15),
            corner_radius=1,
            show='*'
        )

        self.c_password = ctk.CTkEntry(
            self.container,
            placeholder_text='Confirm password',
            font=('Arial Bold', 15),
            corner_radius=1,
            show='*'
        )

        self.referral = ctk.CTkEntry(
            self.container,
            placeholder_text='Referral Code',
            font=('Arial Bold', 15),
            corner_radius=1
        )

        self.postcode = ctk.CTkEntry(
            self.container,
            placeholder_text='Postcode',
            font=('Arial Bold', 15),
            corner_radius=1
        )

        self.submit = ctk.CTkButton(
            self.container,
            text='Register now',
            font=('Arial Bold', 20),
            text_color='white',
            corner_radius=3,
            command=lambda: controller.check_credentials(
                [
                    "DR",
                    self.first_name.get().upper(),
                    self.last_name.get().upper(),
                    self.email.get(),
                    self.tel_no.get(),
                    self.postcode.get(),
                    self.password.get(),
                    self.c_password.get(),
                    self.referral.get(),
                ]
            )
        )

        self.label2 = ctk.CTkLabel(self.container, text="Already have an account?", text_color='black',
                                   font=("Arial Light", 15))

        self.login_bt = ctk.CTkButton(self.container, text='Login here', fg_color='white', text_color='#1a99de',
                                      font=('Arial bold', 15), width=15, hover=False,
                                      command=lambda: controller.show_frame(Login))

        # Creating a simple grid layout for widgets
        self.container.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.container.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.container.grid_columnconfigure((0, 1), weight=1, pad=25)

        self.label.place(relx=0.5, rely=0.13, anchor=tkinter.CENTER)
        self.seperator.place(relx=0.2, rely=0.13, relwidth=0.25, relheight=0.003, anchor=tkinter.CENTER)
        self.seperator2.place(relx=0.8, rely=0.13, relwidth=0.25, relheight=0.003, anchor=tkinter.CENTER)
        self.first_name.grid(row=0, column=0, sticky='ew', padx=(70, 5), pady=(110, 10), ipady=6)
        self.last_name.grid(row=0, column=1, sticky='ew', padx=(5, 70), pady=(110, 10), ipady=6)
        self.email.grid(row=1, column=0, columnspan=2, sticky='ew', padx=70, pady=10, ipady=6)
        self.tel_no.grid(row=2, column=0, columnspan=2, sticky='ew', padx=70, pady=10, ipady=6)
        self.password.grid(row=3, column=0, columnspan=2, sticky='ew', padx=70, pady=10, ipady=6)
        self.c_password.grid(row=4, column=0, columnspan=2, sticky='ew', padx=70, pady=10, ipady=6)
        self.referral.grid(row=5, column=0, sticky='ew', padx=(70, 5), pady=10, ipady=6)
        self.postcode.grid(row=5, column=1, sticky='ew', padx=(5, 70), pady=10, ipady=6)
        self.submit.grid(row=6, column=0, columnspan=2, sticky='nsew', padx=70, pady=(10, 60), ipady=8)
        self.label2.place(relx=0.38, rely=0.93, anchor=tkinter.CENTER)
        self.login_bt.place(relx=0.66, rely=0.93, anchor=tkinter.CENTER)


class Patient_Registration(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        # Create all the necessary widgets for this page
        self.container = ctk.CTkFrame(self, fg_color='white', height=800, width=600, corner_radius=5)
        self.label = ctk.CTkLabel(self.container, text='Patient Registration', text_color='#444343',
                                  font=('Arial bold', 20))

        self.title = ctk.CTkOptionMenu(
            self.container,
            values=['Mr', 'Miss', 'Mrs', 'Ms'],
            corner_radius=3,
            font=('Arial Bold', 15),
            text_color='white',
        )

        self.first_name = ctk.CTkEntry(
            self.container,
            placeholder_text='First name',
            font=('Arial Bold', 15),
            corner_radius=1
        )

        self.last_name = ctk.CTkEntry(
            self.container,
            placeholder_text='Surname',
            font=('Arial Bold', 15),
            corner_radius=1
        )

        self.email = ctk.CTkEntry(
            self.container,
            placeholder_text='Email address',
            font=('Arial Bold', 15),
            corner_radius=1
        )

        self.tel_no = ctk.CTkEntry(
            self.container,
            placeholder_text='Telephone number',
            font=('Arial Bold', 15),
            corner_radius=1
        )

        self.password = ctk.CTkEntry(
            self.container,
            placeholder_text='New password',
            font=('Arial Bold', 15),
            corner_radius=1,
            show='•'
        )

        self.c_password = ctk.CTkEntry(
            self.container,
            placeholder_text='Confirm password',
            font=('Arial Bold', 15),
            corner_radius=1,
            show='•'
        )

        self.postcode = ctk.CTkEntry(
            self.container,
            placeholder_text='Postcode',
            font=('Arial Bold', 15),
            corner_radius=1
        )

        self.submit = ctk.CTkButton(
            self.container,
            text='Register now',
            font=('Arial Bold', 18),
            text_color='white',
            corner_radius=2,
            command=lambda: controller.check_credentials(
                [
                    self.title.get().upper(),
                    self.first_name.get().upper(),
                    self.last_name.get().upper(),
                    self.email.get(),
                    self.tel_no.get(),
                    self.postcode.get(),
                    self.password.get(),
                    self.c_password.get()
                ]
            )
        )

        self.label2 = ctk.CTkLabel(self.container, text="Already have an account?", text_color='black',
                                   font=("Arial Light", 15))

        self.login_bt = ctk.CTkButton(self.container, text='Login here', fg_color='white', text_color='#1a99de',
                                      font=('Arial bold', 15), width=15, hover=False,
                                      command=lambda: controller.show_frame(Login))

        # Creating a simple grid layout for widgets
        self.container.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.container.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.container.grid_columnconfigure((0, 1), weight=1, pad=25)

        self.label.place(relx=0.5, rely=0.13, anchor=tkinter.CENTER)
        self.title.grid(row=0, column=0, sticky='nsew', padx=(70, 5), pady=(120, 10), ipady=1)
        self.first_name.grid(row=1, column=0, sticky='ew', padx=(70, 5), pady=10, ipady=6)
        self.last_name.grid(row=1, column=1, sticky='ew', padx=(5, 70), pady=10, ipady=6)
        self.email.grid(row=2, column=0, columnspan=2, sticky='ew', padx=70, pady=10, ipady=6)
        self.tel_no.grid(row=3, column=0, columnspan=2, sticky='ew', padx=70, pady=10, ipady=6)
        self.password.grid(row=4, column=0, sticky='ew', padx=(70, 5), pady=10, ipady=6)
        self.c_password.grid(row=4, column=1, sticky='ew', padx=(5, 70), pady=10, ipady=6)
        self.postcode.grid(row=5, column=0, sticky='ew', padx=(70, 5), pady=(10, 80), ipady=6)
        self.submit.grid(row=5, column=1, sticky='nsew', padx=(5, 70), pady=(10, 80), ipady=6)
        self.label2.place(relx=0.38, rely=0.91, anchor=tkinter.CENTER)
        self.login_bt.place(relx=0.66, rely=0.91, anchor=tkinter.CENTER)


class Doctor_Dashboard(Dashboard):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Add all the subpages per button into a list
        self.pages_list = [Doctor_Overview, Patients_Tab, Billings_Tab, Bookings_Tab, Settings_Tab]

        # Create all the widgets using the format of 'Dashboard' parent class
        self.title_bar = ctk.CTkFrame(self, fg_color='#3ea1fb', height=75, corner_radius=1)
        self.title_bar.grid(row=0, column=0, columnspan=4, sticky='nsew')

        self.menu_bar = ctk.CTkFrame(self, fg_color='#394356', width=280, corner_radius=1)
        self.menu_bar.grid(row=1, column=0, rowspan=4, sticky='nsew')
        self.menu_bar.rowconfigure((0, 1, 2, 3), weight=0)
        self.menu_bar.columnconfigure((1, 2, 3), weight=1)

        self.menu_container = ctk.CTkFrame(self, fg_color='white', corner_radius=1)
        self.menu_container.grid(row=1, rowspan=2, column=1, sticky='nsew')

        self.menu_title = ctk.CTkLabel(self.menu_bar, fg_color='#394356', corner_radius=1,
                                       text='Menu', anchor='w', text_color='white', width=250, font=('Arial Bold', 23))
        self.menu_title.grid(row=0, column=0, sticky='we', padx=25, pady=40)

        self.patients_bt = ctk.CTkButton(self.menu_bar, fg_color='#394356', corner_radius=1,
                                         text='Patients', anchor='w', text_color='white', font=('Arial Bold', 23),
                                         hover_color='#2c333c', command=lambda: self.show_frame(Patients_Tab))
        self.patients_bt.grid(row=1, column=0, sticky='we', padx=25, pady=(20, 10), ipady=5)

        self.bookings_bt = ctk.CTkButton(self.menu_bar, fg_color='#394356', corner_radius=1,
                                         text='Appointments', anchor='w', text_color='white', font=('Arial Bold', 23),
                                         hover_color='#2c333c', command=lambda: self.show_frame(Bookings_Tab))
        self.bookings_bt.grid(row=2, column=0, sticky='we', padx=25, pady=20, ipady=5)

        self.reports_bt = ctk.CTkButton(self.menu_bar, fg_color='#394356', corner_radius=1,
                                        text='Reports', anchor='w', text_color='white', font=('Arial Bold', 23),
                                        hover_color='#2c333c', command=lambda: self.show_frame(Billings_Tab))
        self.reports_bt.grid(row=3, column=0, sticky='we', padx=25, pady=20, ipady=5)

        self.settings = ctk.CTkButton(self.menu_bar, fg_color='#394356', corner_radius=1,
                                      text='Settings', anchor='w', text_color='white', font=('Arial Bold', 23),
                                      hover_color='#2c333c', command=lambda: self.show_frame(Settings_Tab))
        self.settings.grid(row=4, column=0, sticky='we', padx=25, pady=20, ipady=5)

        self.setup_pages(self.menu_container)
        self.show_frame(Doctor_Overview)


# All the subpages for the Doctor's dashboard
class Doctor_Overview(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        container = ctk.CTkFrame(self, fg_color='blue')
        container.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


class Patients_Tab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.add_patient = ctk.CTkButton(
            self,
            text_color='white',
            text='Add new patient',
            font=('Arial Bold', 17),
            width=200,
            height=50,
            corner_radius=4
        )
        self.add_patient.grid(row=0, column=0, padx=30, pady=(30, 10), sticky='nsew')


class Bookings_Tab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        container = ctk.CTkFrame(self, fg_color='green')
        container.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


class Billings_Tab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        container = ctk.CTkFrame(self, fg_color='purple')
        container.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


class Settings_Tab(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        container = ctk.CTkFrame(self, fg_color='grey')
        container.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


class Patient_Dashboard(Dashboard):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        pass


app_client = Client('localhost', port)
App('Olinic Management', (1920, 1080), app_client)
