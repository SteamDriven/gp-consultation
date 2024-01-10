from tkinter import *
from customtkinter import *

from PIL import Image
from Client.Widgets import InfoEntry

from os.path import *


class Login(CTkFrame):

    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        self.controller = controller

        # Set weights for grid columns to control resizing
        self.grid_columnconfigure(0, weight=4)  # Left frame
        self.grid_columnconfigure(1, weight=3)  # Right Frame
        self.grid_rowconfigure(0, weight=1)

        self.login_image_path = join(dirname(__file__), "../Images/Login_Image.png")
        self.logo_image_path = join(dirname(__file__), "../Images/Logo_Bluebg.png")

        self.helvetica_bold = CTkFont(family="Helvetica", size=45, weight="normal")
        self.helvetica_light = CTkFont(family="Arial Light", size=20)
        self.calibri_1 = CTkFont(family="Calibri Light", size=25, underline=True)
        self.calibri_2 = CTkFont(family="Calibri Light", size=20)
        self.calibri_3 = CTkFont(family="Calibri Light", size=20, underline=True)
        self.calibri_light = CTkFont(family="Calibri Light", size=25)

        self.left_frame = None
        self.right_frame = None
        self.login_image = None
        self.logo_image = None
        self.welcome_label = None
        self.signup_frame = None
        self.no_account_label = None
        self.sign_up_bt = None
        self.username_entry = None
        self.password_entry = None
        self.options_frame = None
        self.check_box = None
        self.forgot_password = None
        self.login_bt = None

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

        login_image_ck = CTkImage(original_login_image, size=(668, 606))
        logo_image_ck = CTkImage(original_logo_image, size=(152, 140))

        self.left_frame = CTkFrame(self, fg_color='white', corner_radius=0)

        self.right_frame = CTkFrame(self, fg_color='#4c70c0', corner_radius=0)

        self.login_image = CTkLabel(self.left_frame, image=login_image_ck, text='')

        self.logo_image = CTkLabel(self.right_frame, image=logo_image_ck, text='')

        self.welcome_label = CTkLabel(self.right_frame, text='Welcome Back!',
                                      font=self.helvetica_bold, text_color='white')

        self.signup_frame = CTkFrame(self.right_frame, fg_color='#4c70c0')  # Assuming the same background color

        self.no_account_label = CTkLabel(self.signup_frame, text="Don't have an account yet?",
                                         font=self.calibri_light, text_color='white')
        self.sign_up_bt = CTkButton(self.signup_frame, text='Sign up', font=self.calibri_1,
                                    hover=False, fg_color='#4c70c0', text_color='white')

        self.username_entry = InfoEntry(self.right_frame, placeholder='Username', show_bullet=False, min_width=500,
                                    fg_color='#4c70c0', font=(self.calibri_light, 30))
        self.password_entry = InfoEntry(self.right_frame, placeholder='Password', show_bullet=True, min_width=500,
                                    fg_color='#4c70c0', font=(self.calibri_light, 30))

        self.options_frame = CTkFrame(self.right_frame, fg_color='#4c70c0')
        self.check_box = CTkCheckBox(self.options_frame, text='Keep me logged in', text_color='white',
                                     font=self.calibri_2, border_width=10, corner_radius=5, fg_color='#4c70c0',
                                     border_color='white', checkbox_width=20, checkbox_height=20)
        self.forgot_password = CTkButton(self.options_frame, text='Forgot password?', text_color='white',
                                         font=self.calibri_3, fg_color='#4c70c0', hover=False)

        self.login_bt = CTkButton(self.right_frame, text='Login', text_color='white', font=('Helvetica bold', 20),
                                  fg_color='#7b96d4', width=500, height=70, hover_color='#3c5691',
                                  command=lambda: self.init_login())

    def place_widgets(self):
        self.left_frame.grid(row=0, column=0, sticky='nsew')
        self.right_frame.grid(row=0, column=1, sticky='nsew', ipadx=20)
        self.login_image.pack(pady=(300, 0))
        self.logo_image.pack(padx=(20, 0), pady=(20, 0))
        self.welcome_label.pack(pady=(10, 0), anchor='center')
        self.signup_frame.pack(pady=(10, 0), anchor='center')
        self.no_account_label.pack(side='left')
        self.sign_up_bt.pack(side='right')

        # ENTRIES
        self.username_entry.pack(pady=(150, 30), anchor='center')
        self.password_entry.pack(anchor='center')

        self.check_box.pack(side='left', padx=85)
        self.forgot_password.pack(side='right', padx=85)
        self.options_frame.pack(pady=30, anchor=CENTER)

        self.login_bt.pack(pady=40, anchor=CENTER)
