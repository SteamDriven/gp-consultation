import tkinter
import tkinter as tk
from tkinter import *
import customtkinter as ctk
from PIL import Image


class ENTRY(ctk.CTkFrame):

    def __init__(self, master=None, placeholder="", show_bullet=False, font=None, min_width=None, **kwargs):
        super().__init__(master, **kwargs)

        # CONFIGURATIONS
        self.placeholder = placeholder
        self.show_bullet = ""

        if show_bullet:
            self.show_bullet = '*'

        self.label = ctk.CTkLabel(self, text=self.placeholder, fg_color='#4c70c0', text_color='white',
                                  font=('Calibri Light', 25))
        self.label.grid(row=0, column=0, pady=5, padx=5, sticky='w')

        self.entry = ctk.CTkEntry(self, show=self.show_bullet, width=min_width, font=font, border_width=0,
                                  corner_radius=10)
        self.entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, ipady=20)

    def get_entry(self):
        current_val = self.entry.get()
        return current_val if current_val != self.placeholder else False

    def clear_entry(self):
        self.entry.delete(0, END)


class IMAGE_BUTTON(ctk.CTkFrame):
    def __init__(self, master=None, description="", path=None, size=None, fg=None, font=None, command=None, **kwargs):
        super().__init__(master, **kwargs)

        # CONFIGURATIONS
        if size is None:
            size = (1, 1)

        if fg is None:
            fg = "#3c5691"

        if font is None:
            font = ('Arial Bold', 30)

        self.text = description
        self.img_path = path
        self.size = size
        self.background_color = fg
        self.font = font
        self.name = self.text
        self.command=command

        self.configure(fg_color=self.background_color, corner_radius=0)

        self.setup_widgets()
        self.place_widgets()

    def setup_widgets(self):
        image = Image.open(self.img_path)
        image_ck = ctk.CTkImage(image, size=self.size)

        self.logo = ctk.CTkLabel(self, image=image_ck, text='')
        self.btn = ctk.CTkButton(self, text=self.text, text_color='white', font=self.font,
                                 fg_color=self.background_color, hover_color='#202f50', corner_radius=0,
                                 anchor='w', command=self.command)

    def place_widgets(self):
        self.logo.grid(row=0, column=0, sticky='ew')
        self.btn.grid(row=0, column=1, columnspan=2, sticky='ew')


class LOGIN(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.controller = controller

        # Set weights for grid columns to control resizing
        self.grid_columnconfigure(0, weight=4)  # Left frame
        self.grid_columnconfigure(1, weight=3)  # Right Frame
        self.grid_rowconfigure(0, weight=1)

        self.login_image_path = "Images/Login_Image.png"
        self.logo_image_path = "Images/Logo_Bluebg.png"

        self.helvetica_bold = ctk.CTkFont(family="Helvetica", size=45, weight="normal")
        self.helvetica_light = ctk.CTkFont(family="Arial Light", size=20)
        self.calibri_1 = ctk.CTkFont(family="Calibri Light", size=25, underline=True)
        self.calibri_2 = ctk.CTkFont(family="Calibri Light", size=20)
        self.calibri_3 = ctk.CTkFont(family="Calibri Light", size=20, underline=True)
        self.calibri_light = ctk.CTkFont(family="Calibri Light", size=25)

        self.create_widgets()
        self.place_widgets()

    def init_login(self):
        login_info = self.get_login_information()
        self.username_entry.clear_entry()
        self.password_entry.clear_entry()

        self.controller.validate_login(login_info)

    def get_login_information(self):
        return [self.username_entry.get_entry(), self.password_entry.get_entry()]

    def create_widgets(self):
        original_login_image = Image.open(self.login_image_path)
        original_logo_image = Image.open(self.logo_image_path)

        login_image_ck = ctk.CTkImage(original_login_image, size=(668, 606))
        logo_image_ck = ctk.CTkImage(original_logo_image, size=(152, 140))

        self.left_frame = ctk.CTkFrame(self, fg_color='white', corner_radius=0)

        self.right_frame = ctk.CTkFrame(self, fg_color='#4c70c0', corner_radius=0)

        self.login_image = ctk.CTkLabel(self.left_frame, image=login_image_ck, text='')

        self.logo_image = ctk.CTkLabel(self.right_frame, image=logo_image_ck, text='')

        self.welcome_label = ctk.CTkLabel(self.right_frame, text='Welcome Back!',
                                          font=self.helvetica_bold, text_color='white')

        self.signup_frame = tk.Frame(self.right_frame, bg='#4c70c0')  # Assuming the same background color

        self.no_account_label = ctk.CTkLabel(self.signup_frame, text="Don't have an account yet?",
                                             font=self.calibri_light, text_color='white')
        self.sign_up_bt = ctk.CTkButton(self.signup_frame, text='Sign up', font=self.calibri_1,
                                        hover=False, fg_color='#4c70c0', text_color='white')

        self.username_entry = ENTRY(self.right_frame, placeholder='Username', show_bullet=False, min_width=500,
                                    fg_color='#4c70c0', font=(self.calibri_light, 30))
        self.password_entry = ENTRY(self.right_frame, placeholder='Password', show_bullet=True, min_width=500,
                                    fg_color='#4c70c0', font=(self.calibri_light, 30))

        self.options_frame = ctk.CTkFrame(self.right_frame, fg_color='#4c70c0')
        self.check_box = ctk.CTkCheckBox(self.options_frame, text='Keep me logged in', text_color='white',
                                         font=self.calibri_2, border_width=10, corner_radius=5, fg_color='#4c70c0',
                                         border_color='white', checkbox_width=20, checkbox_height=20)
        self.forgot_password = ctk.CTkButton(self.options_frame, text='Forgot password?', text_color='white',
                                             font=self.calibri_3, fg_color='#4c70c0', hover=False)

        self.login_bt = ctk.CTkButton(self.right_frame, text='Login', text_color='white', font=('Helvetica bold', 20),
                                      fg_color='#7b96d4', width=500, height=70, hover_color='#3c5691',
                                      command=lambda: self.init_login())

    def place_widgets(self):
        self.left_frame.grid(row=0, column=0, sticky='nsew')
        self.right_frame.grid(row=0, column=1, sticky='nsew', ipadx=20)
        self.login_image.pack(pady=(300, 0))
        self.logo_image.pack(padx=(20, 0), pady=(20, 0))
        self.welcome_label.pack(pady=(10, 0), anchor='center')
        self.signup_frame.pack(pady=(10, 0), anchor='center')
        self.no_account_label.pack(side=tk.LEFT)
        self.sign_up_bt.pack(side=tk.RIGHT)

        # ENTRIES
        self.username_entry.pack(pady=(150, 30), anchor='center')
        self.password_entry.pack(anchor='center')

        self.check_box.pack(side=tk.LEFT, padx=85)
        self.forgot_password.pack(side=tk.RIGHT, padx=85)
        self.options_frame.pack(pady=30, anchor=tkinter.CENTER)

        self.login_bt.pack(pady=40, anchor=tkinter.CENTER)


class DASHBOARD(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        # CONFIGURATIONS
        self.user_type = "Loading"
        self.controller = controller
        self.frames = {}
        self.pages_list = [APPOINTMENTS]

        self.logo_image_path = "Images/Logo_Bluebg.png"

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2), weight=1)

        self.helvetica_bold = ctk.CTkFont(family="Helvetica", size=45, weight="normal")
        self.helvetica_light = ctk.CTkFont(family="Arial Light", size=20)
        self.calibri_1 = ctk.CTkFont(family="Calibri Light", size=25, underline=True)
        self.calibri_2 = ctk.CTkFont(family="Calibri Light", size=20)
        self.calibri_3 = ctk.CTkFont(family="Calibri Light", size=20, underline=True)
        self.calibri_light = ctk.CTkFont(family="Calibri Light", size=25)

    def create_widgets(self):
        original_logo_image = Image.open(self.logo_image_path)
        logo_image_ck = ctk.CTkImage(original_logo_image, size=(96, 90))

        self.title_bar = ctk.CTkFrame(self, fg_color='#4c6fbf', corner_radius=0, height=90)
        self.logo_image = ctk.CTkLabel(self.title_bar, image=logo_image_ck, text='')
        self.user_lbl = ctk.CTkLabel(self.title_bar, text=self.user_type, text_color='white',
                                     font=self.helvetica_bold)
        self.menu_bar = ctk.CTkFrame(self, fg_color='#3c5691', corner_radius=0, width=300)
        self.dash_frame = ctk.CTkFrame(self.menu_bar, fg_color='#2a3e6a', corner_radius=0, height=75)
        self.dash_btn = ctk.CTkButton(self.dash_frame, fg_color='#2a3e6a', corner_radius=0, text='My Dashboard',
                                      font=('Arial Bold', 35), hover=False)
        self.buttons_frame = ctk.CTkFrame(self.menu_bar, fg_color='#3c5691', corner_radius=0)
        self.main_frame = ctk.CTkFrame(self, fg_color='white', corner_radius=0)

    def place_widgets(self):
        self.title_bar.grid(row=0, column=0, columnspan=4, sticky='ew')
        self.logo_image.pack(side=LEFT, anchor=CENTER)
        self.user_lbl.pack(side=RIGHT, anchor=CENTER, padx=30)
        self.menu_bar.grid(row=1, column=0, rowspan=4, sticky='ns')
        self.dash_frame.pack(side=TOP, anchor=CENTER)
        self.dash_btn.pack(padx=12, pady=12, anchor=CENTER, ipadx=20)
        self.buttons_frame.pack(pady=80, anchor=CENTER)
        self.main_frame.grid(row=1, column=1, rowspan=2, sticky='nsew')

        for F in self.pages_list:
            frame = F(self.main_frame, self)

            self.frames[F] = frame

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.pack(side="left", fill="both", expand=True)


class PATIENT_DASHBOARD(DASHBOARD):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.user_type = "Patient"
        self.buttons = {
            'Appointments': {
                "path": 'Images/Appointments.PNG',
                "size": (56, 60),
                "command": lambda: self.show_frame(APPOINTMENTS)
            },
            'Profile': {
                "path": 'Images/Profile.PNG',
                "size": (55, 57),
                "command": None
            },
            'Prescriptions': {
                "path": 'Images/Prescriptions.PNG',
                "size": (60, 58),
                "command": None
            },
            'Notifications': {
                "path": 'Images/Notifications.PNG',
                "size": (58, 58),
                "command": None
            },
            'Chat': {
                "path": 'Images/Chat.PNG',
                "size": (67, 52),
                "command": None
            },
        }

        self.create_widgets()
        self.configure_menu()
        self.place_widgets()

    def configure_menu(self):
        self.buttons_frame.grid_columnconfigure(0, weight=0)
        self.buttons_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)

        for label, info in self.buttons.items():
            print("\nButton Type:", label)

            button = IMAGE_BUTTON(self.buttons_frame,
                                  label,
                                  info['path'],
                                  info['size'],
                                  command=info['command'])

            button.pack(pady=30, anchor=W)


class APPOINTMENTS(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        self.configure(fg_color='red', corner_radius=0)


class DOCTOR_DASHBOARD(DASHBOARD):
    pass
