from tkinter import *
from customtkinter import *

from PIL import Image as PILImage
from Client.Pages.Dashboard.Chat import ChatRoom
from Client.Pages.Dashboard.ChatBoard import *
from Client.Pages.Dashboard.Appointments import *
from Client.Pages.Dashboard.Symptoms import Symptoms
from Client.Pages.Dashboard.AppointmentDetails import *
from Client.Pages.Dashboard.AcceptAppointment import *
from Client.Pages.Dashboard.Notifications import *
from Client.Pages.Dashboard.SelectTime import *
from Client.Widgets import ImageButton

from os.path import *

from Client.libclient import Client


class Dashboard(CTkFrame):

    def __init__(self, parent, controller, user_data, client):
        CTkFrame.__init__(self, parent)

        print(f"{self.__class__.__name__} successfully initialised.")

        # CONFIGURATIONS
        self.user_data = user_data
        self.controller = controller
        self.client = client

        self.username = ' '.join(self.user_data.user[1][1:]).title()

        self.logo_image_path = join(dirname(__file__), "../../Images/Logo_Bluebg.png")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2), weight=1)

        self.helvetica_bold = CTkFont(family="Helvetica", size=45, weight="normal")
        self.helvetica_light = CTkFont(family="Arial Light", size=20)
        self.calibri_1 = CTkFont(family="Calibri Light", size=25, underline=True)
        self.calibri_2 = CTkFont(family="Calibri Light", size=20)
        self.calibri_3 = CTkFont(family="Calibri Light", size=20, underline=True)
        self.calibri_light = CTkFont(family="Calibri Light", size=25)

        self.title_bar = None
        self.logo_image = None
        self.user_lbl = None
        self.menu_bar = None
        self.dash_frame = None
        self.dash_btn = None
        self.buttons_frame = None
        self.main_frame = None

        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        print('oof')
        original_logo_image = PILImage.open(self.logo_image_path)
        print('oof2')
        logo_image_ck = CTkImage(original_logo_image, size=(96, 90))
        print('oof3')

        self.title_bar = CTkFrame(self, fg_color='#4c6fbf', corner_radius=0, height=90)
        self.logo_image = CTkLabel(self.title_bar, image=logo_image_ck, text='')
        self.user_lbl = CTkLabel(self.title_bar, text=self.username, text_color='white',
                                 font=self.helvetica_bold)
        self.menu_bar = CTkFrame(self, fg_color='#3c5691', corner_radius=0, width=300)
        self.dash_frame = CTkFrame(self.menu_bar, fg_color='#2a3e6a', corner_radius=0, height=75)
        self.dash_btn = CTkButton(self.dash_frame, fg_color='#2a3e6a', corner_radius=0, text='My Dashboard',
                                  font=('Arial Bold', 35), hover=False)
        self.buttons_frame = CTkFrame(self.menu_bar, fg_color='#3c5691', corner_radius=0)
        self.main_frame = CTkFrame(self, fg_color='white', corner_radius=0)

    def place_widgets(self):
        self.title_bar.grid(row=0, column=0, columnspan=4, sticky='ew')
        self.logo_image.pack(side=LEFT, anchor=CENTER)
        self.user_lbl.pack(side=RIGHT, anchor=CENTER, padx=30)
        self.menu_bar.grid(row=1, column=0, rowspan=4, sticky='ns')
        self.dash_frame.pack(side=TOP, anchor=CENTER)
        self.dash_btn.pack(padx=12, pady=12, anchor=CENTER, ipadx=20)
        self.buttons_frame.pack(pady=80, anchor=CENTER)
        self.main_frame.grid(row=1, column=1, rowspan=2, sticky='nsew')


class PatientDashboard(Dashboard):
    def __init__(self, parent, controller, user_data, client):
        super().__init__(parent, controller, user_data, client)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.client = client
        self.user_data = user_data
        self.frames = {}
        self.pages_list = {

            "request app": RequestAppointments,
            "symptoms": Symptoms,
            "chat room": ChatRoom,
            'appointments': Appointments,
            'notifications': Notifications,
        }

        self.buttons = {
            'Appointments': {
                "path": f'{join(dirname(__file__), "../../Images/Appointments.PNG")}',
                "size": (56, 60),
                "command": lambda: self.show_frame("request app")
            },
            'Profile': {
                "path": f'{join(dirname(__file__), "../../Images/Profile.PNG")}',
                "size": (55, 57),
                "command": None
            },
            'Prescriptions': {
                "path": f'{join(dirname(__file__), "../../Images/Prescriptions.PNG")}',
                "size": (60, 58),
                "command": None
            },
            'Notifications': {
                "path": f'{join(dirname(__file__), "../../Images/Notifications.PNG")}',
                "size": (58, 58),
                "command": lambda: self.show_frame("notifications")
            },
            'Chat': {
                "path": f'{join(dirname(__file__), "../../Images/Chat.PNG")}',
                "size": (67, 52),
                "command": lambda: self.show_frame('chat room')
            },
        }

        self.dash_btn.configure(command=lambda: self.show_frame('dashboard'))

        self.configure_menu()
        for key, value in self.pages_list.items():
            self.frames[key] = value(self.main_frame, self, self.user_data)

        self.show_frame('appointments')

    def show_frame(self, cont: str):
        frame = self.frames[cont]
        print('Displaying frame:', cont)

        try:
            for f in self.frames.values():
                print(f)
                f.pack_forget()

            if cont == 'chat room':
                frame.create()
                frame.place()

            if cont == 'notifications':
                frame.update_notifications()

            frame.pack(side="top", fill="both", expand=True)
            frame.tkraise()

        except Exception as e:
            print(f"Error in show_frame: {e}")
            raise

    def configure_menu(self):
        self.buttons_frame.grid_columnconfigure(0, weight=0)
        self.buttons_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
        print('configuring menu for loading buttons')

        for label, info in self.buttons.items():
            print("\nButton Type:", label)

            button = ImageButton(self.buttons_frame,
                                 label,
                                 info['path'],
                                 info['size'],
                                 command=info['command'])

            button.pack(pady=30, anchor=W)
            print('packing button')


class DoctorDashboard(Dashboard):
    def __init__(self, parent, controller, user_data, client):
        super().__init__(parent, controller, user_data, client)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.client = client
        self.user_data = user_data
        self.controller = controller
        self.frames = {}
        self.pages_list = {

            # "chat room": ChatBoard,
            'appointments': Appointments,
            'notifications': Notifications,
            # 'confirm apt': SelectTime,
        }

        self.buttons = {
            'Appointments': {
                "path": f'{join(dirname(__file__), "../../Images/Appointments.PNG")}',
                "size": (56, 60),
                "command": None
            },
            'Profile': {
                "path": f'{join(dirname(__file__), "../../Images/Profile.PNG")}',
                "size": (55, 57),
                "command": None
            },
            'Patients': {
                "path": f'{join(dirname(__file__), "../../Images/Patient.PNG")}',
                "size": (59, 56),
                "command": None
            },
            'Notifications': {
                "path": f'{join(dirname(__file__), "../../Images/Notifications.PNG")}',
                "size": (58, 58),
                "command": lambda: self.show_frame("notifications")
            },
            'Chat': {
                "path": f'{join(dirname(__file__), "../../Images/Chat.PNG")}',
                "size": (67, 52),
                "command": lambda: self.show_frame('chat room')
            },
        }

        # self.dash_btn.configure(command=lambda: self.show_frame('dashboard'))

        self.configure_menu()
        for key, value in self.pages_list.items():
            self.frames[key] = value(self.main_frame, self, self.user_data)

        # self.add_page('apt details', AppointmentDetails, (self.main_frame, self))
        self.show_frame('appointments')

    def show_frame(self, cont: str):
        frame = self.frames[cont]
        print('Displaying frame:', cont)

        try:
            if frame is not None:
                for f in self.frames.values():
                    f.pack_forget()

                # if cont == 'chat room':
                #     for f in self.controller.frames.values():
                #         f.pack_forget()
                #
                #         frame = ChatBoard(self.controller.container, self, self.user_data, self.client)
                #     # frame.create()
                #     # frame.place()

                if cont == 'notifications':
                    frame.update_notifications()

                frame.pack(side="top", fill="both", expand=True)
                frame.tkraise()

            else:
                raise ValueError(f"Frame '{cont}' does not exist.")

        except Exception as e:
            print(f"Error in show_frame: {e}")
            raise e

    def configure_menu(self):
        self.buttons_frame.grid_columnconfigure(0, weight=0)
        self.buttons_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
        print('configuring menu for loading buttons')

        for label, info in self.buttons.items():
            print("\nButton Type:", label)

            button = ImageButton(self.buttons_frame,
                                 label,
                                 info['path'],
                                 info['size'],
                                 command=info['command'])

            button.pack(pady=30, anchor=W)
