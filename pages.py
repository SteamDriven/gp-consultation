import tkinter
from functools import partial
import tkinter as tk
from tkinter import *
import customtkinter as ctk
from PIL import Image
import calendar
from datetime import datetime


class DataManager:
    selected_time = None
    selected_day = None

    def update_times(self, time, day):
        self.selected_time = time
        self.selected_day = day

        print(f"TIME: {self.selected_time}, DAY: {self.selected_day}")


class Label(ctk.CTkFrame):
    DEFAULT_FONT = ('Arial Bold', 25)

    def __init__(self, master=None, color='white', bg='#4c6fbf', text='Loading', font=None, side=None, state='normal', **kwargs):
        super().__init__(master, **kwargs)

        self.text_col = color
        self.fg = bg
        self.text = text
        self.state = state

        if self.state == 'special':
            self.bind('<1>', self.change_type)

        if font:
            self.font = font
        else:
            self.font = self.DEFAULT_FONT

        if side:
            self.side = side
        else:
            self.side = 'right'

        self.configure(fg_color=self.fg, corner_radius=0)

        self.label = ctk.CTkLabel(self, text=self.text, fg_color=self.fg, text_color=self.text_col,
                                  font=self.font)

        self.label.pack(side=self.side, padx=10)

    def change_type(self, event):
        print('Changing to entry.')


class Entry(ctk.CTkFrame):
    DEFAULT_TEXT_COL = '#cecaca'
    DEFAULT_ENTRY_FONT = ('Arial Light', 30)
    DEFAULT_FONT = ('Arial Bold', 25)

    def __init__(self, master=None, placeholder='Enter response here', **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.configure(fg_color='#f2f2f2', corner_radius=0)

        self.setup_box()
        self.place_box()

    def create_entry(self):
        pass

    def setup_box(self):
        self.txt = Label(self, text='Enter response here...', bg='white', font=self.DEFAULT_ENTRY_FONT, side='left',
                         color=self.DEFAULT_TEXT_COL, state='special')
        self.send_button = ctk.CTkButton(self, text='Send', font=self.DEFAULT_FONT, text_color='white',
                                         corner_radius=5, fg_color='#7b96d4', width=250, anchor='w')

    def place_box(self):
        self.send_button.pack(side='right', ipady=5)
        self.txt.pack(fill='both', expand=True, anchor=CENTER, padx=5, pady=5)


class Chat(ctk.CTkFrame):
    DEFAULT_TEXT = 'white'
    DEFAULT_BG = '#4c6fbf'
    DEFAULT_CHAT_BG = '#f2f2f2'

    def __init__(self, master=None, title='AI Chat', state='AI', **kwargs):
        super().__init__(master, **kwargs)

        self.title = title
        self.state = state

        self.setup_chat()
        self.create_chat()

    def setup_chat(self):
        self.container = ctk.CTkFrame(self, fg_color=self.DEFAULT_CHAT_BG, corner_radius=0)
        self.label = Label(self.container, text=self.title)
        self.chat_frame = ctk.CTkScrollableFrame(self.container, fg_color=self.DEFAULT_CHAT_BG, corner_radius=0)
        self.chat_box = Entry(self.container)

    def create_chat(self):
        self.container.pack(fill='both', expand=True)
        self.label.pack(fill='x', ipady=5)
        self.chat_frame.pack(fill='both', expand=True)
        self.chat_box.pack(side='bottom', fill='x', pady=15, padx=15, ipady=5)


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


class BUTTON(ctk.CTkFrame):
    ENABLED_TEXT = 'white'
    DISABLED_TEXT = '#0f0e0c'
    ENABLED_BG = '#4c6fbf'
    DISABLED_BG = '#e7e5e5'

    def __init__(self, master=None, placeholder="placeholder", background=None, **kwargs):
        super().__init__(master, **kwargs)

        self.state = False
        self.placeholder = placeholder
        self.background = background
        self.col = 0

        self.configure(corner_radius=0, fg_color=self.DISABLED_BG)

        self.create_widgets()
        self.place_widgets()

    # def __repr__(self):
    #     return f"BUTTON: {self.placeholder}, {self.state}"

    def __str__(self):
        return f"BUTTON: {self.placeholder}, {self.state}"

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text=self.placeholder, fg_color=self.DISABLED_BG, text_color=self.DISABLED_TEXT,
                                  font=('Arial bold', 25), corner_radius=0)

    def place_widgets(self):
        self.label.pack(padx=10, pady=10, anchor=CENTER)

    def update_background(self, color):
        self.configure(fg_color=color)
        self.label.configure(fg_color=color)

    def update_text_color(self, color):
        self.label.configure(text_color=color)

    def change_state(self):
        if not self.state:
            self.state = True

            self.update_background(self.ENABLED_BG)
            self.update_text_color(self.ENABLED_TEXT)
        else:
            self.state = False

            self.update_background(self.DISABLED_BG)
            self.update_text_color(self.DISABLED_TEXT)

        return self.state


class DATE_FRAME(ctk.CTkFrame):
    DISABLED_TEXT = '#0f0e0c'
    ENABLED_TEXT = '#ffffff'
    ENABLED_BG = '#4c6fbf'

    def __init__(self, master=None, day=None, date=None, colour='green', **kwargs):
        super().__init__(master, **kwargs)

        self.day = day
        self.date = date
        self.colour = colour
        self.state = 'DISABLED'

        self.configure(fg_color=self.colour)

    def __str__(self):
        return f"BUTTON: {self.day.upper()}, {self.date}, {self.state}"

    def create_labels(self):
        self.day_label = ctk.CTkLabel(self, text_color=self.DISABLED_TEXT, text=self.day, fg_color=self.colour,
                                      font=('Arial Bold', 35))
        self.date_label = ctk.CTkLabel(self, text_color=self.DISABLED_TEXT, text=self.date, fg_color=self.colour,
                                       font=('Arial light', 35))

    def place_widgets(self):
        self.day_label.grid(row=0, column=0, sticky='ns', padx=15, pady=5, ipadx=20, ipady=20)
        self.date_label.grid(row=1, column=0, sticky='ns', pady=5)

    def update_day(self, new_day):
        self.day = new_day
        self.day_label.configure(text=self.day)

        return print(f"Day has now been set to {self.day}")

    def update_date(self, new_date):
        self.date = new_date
        self.date_label.configure(text=self.date)

        return print(f"Date has now been set to {self.date}")

    def change_color(self, back, color):
        self.configure(fg_color=back)
        self.day_label.configure(text_color=color, fg_color=back)
        self.date_label.configure(text_color=color, fg_color=back)

    def change_state(self):
        if self.state == 'DISABLED':
            self.state = 'ENABLED'

            self.change_color(self.ENABLED_BG, self.ENABLED_TEXT)
        else:
            self.state = "DISABLED"
            self.change_color(self.colour, self.DISABLED_TEXT)

        print(f"Button state has been changed to {self.state}")


class CALENDAR(ctk.CTkFrame):
    LEFT_ARROW_PATH = "Images/Left_arrow.PNG"
    RIGHT_ARROW_PATH = "Images/Right_arrow.PNG"

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.year = None
        self.month = None
        self.current_week = None
        self.buttons = []
        self.selected_button = None

        self.configure(fg_color='#f2f2f2')
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.create_widgets()

    def get_current_week(self):
        cal = calendar.monthcalendar(self.year, self.month)

        for i, week in enumerate(cal):
            if datetime.now().day in week:
                return i
            return 0

    def get_selected_button(self):
        return self.selected_button

    def select_date(self, index):
        if len(self.buttons) > 0:
            selected = self.buttons[index]
            selected.change_state()
            self.selected_button = selected

        print(f'{self.selected_button} has been selected randomly.')

    def display_buttons(self):
        if len(self.buttons) > 0:
            for button in self.buttons:
                print(button)

    def set_current_date(self):
        self.year = datetime.now().year
        self.month = datetime.now().month

        if self.year and self.month:
            self.current_week = self.get_current_week()

    @staticmethod
    def get_day(date):
        if date:
            day = date.strftime('%a')
        else:
            day = ""

        return day

    def create_widgets(self):
        self.set_current_date()
        self.day_frame = ctk.CTkFrame(self, fg_color='#f2f2f2')
        self.day_frame.grid(row=0, column=1, pady=40)

        left_image = Image.open(self.LEFT_ARROW_PATH)
        right_image = Image.open(self.RIGHT_ARROW_PATH)
        left_image_ck = ctk.CTkImage(left_image, size=(61, 73))
        right_image_ck = ctk.CTkImage(right_image, size=(69, 76))

        next_week = partial(self.change_week, True)
        prev_week = partial(self.change_week, False)

        self.left_arrow = ctk.CTkButton(self, image=left_image_ck, text='', fg_color='#f2f2f2', hover=False,
                                        command=prev_week)
        self.right_arrow = ctk.CTkButton(self, image=right_image_ck, text='', fg_color='#f2f2f2', hover=False,
                                         command=next_week)

        self.left_arrow.grid(row=0, column=0, padx=5)
        self.right_arrow.grid(row=0, column=2, padx=5)

        self.display_week()
        self.select_date(0)
        self.display_buttons()

    def clear_frame(self):
        for child in self.day_frame.winfo_children():
            child.destroy()

        self.buttons = []

    def display_week(self):
        cal = calendar.monthcalendar(self.year, self.month)
        week = cal[self.current_week]

        for row, day in enumerate(week):
            frame = DATE_FRAME(self.day_frame, colour='#f2f2f2')

            if day == 0:
                state = False
            else:
                state = True
            # text = "" if date == 0 else date
            # state = "NORMAL" if date > 0 else "DISABLED"

            if state:
                weekday = self.get_day(datetime(self.year, self.month, day))
                frame.date = day
                frame.day = weekday

                frame.create_labels()
                frame.place_widgets()
                frame.grid(row=0, column=row, sticky='nsew', padx=15)

                frame.bind("<1>", lambda event, button=frame: self.select_button(event, button))
                self.buttons.append(frame)

    def update_calendar(self):
        if self.current_week >= len(calendar.monthcalendar(self.year, self.month)):
            self.current_week = 0
            self.month += 1

            if self.month > 12:
                self.month = 1
                self.year += 1

        if self.current_week < 0:
            self.month -= 1

            if self.month < 1:
                self.month = 12
                self.year -= 1

            self.current_week = len(calendar.monthcalendar(self.year, self.month)) - 1

    def change_week(self, direction):

        if direction:
            self.current_week += 1
        else:
            self.current_week -= 1

        self.update_calendar()

        self.clear_frame()
        self.display_week()
        self.select_date(0)

    def select_button(self, event, button):
        print(f"{button} has been selected. Current selected date is {self.selected_button}")

        if self.selected_button:
            self.selected_button.change_state()

            button.change_state()
            self.selected_button = button

        print(f"Selected date has been changed to: {self.selected_button}")

    # def create_widgets(self):
    #     self.day_frame = ctk.CTkFrame(self, fg_color='red')
    #     self.day_frame.pack(side='top', fill='x')
    #
    #     self.redraw(self.year, self.month)
    #
    # def redraw(self, year, month):
    #     for d in self.day_frame.winfo_children():
    #         d.destroy()
    #
    #     for col, day in enumerate(("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")):
    #         frame = FRAME(master=self.day_frame, day=day)


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
        self.command = command

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

        print(f"{self.__class__.__name__} successfully initialised.")

        # CONFIGURATIONS
        self.user_type = "Loading"
        self.controller = controller
        self.current_frame = None
        self.frames = {}
        self.pages_list = []

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

    def show_frame(self, cont):
        frame = self.frames[cont]
        if frame:
            print('Displaying frame:', cont)

            frame.pack(side="left", fill="both", expand=True)
            frame.tkraise()


class PATIENT_DASHBOARD(DASHBOARD):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.user_type = "Patient"
        self.appointment_data = DataManager()
        self.pages_list = {
            "request_app": REQUEST_APPOINTMENTS,
            "symptoms": SYMPTOMS,
        }

        self.buttons = {
            'Appointments': {
                "path": 'Images/Appointments.PNG',
                "size": (56, 60),
                "command": lambda: self.show_frame("request_app")
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

        self.frames = {}
        for key, value in self.pages_list.items():
            self.frames[key] = value(self.main_frame, self)
            # self.frames[key].grid(row=0, column=0, sticky='nsew')
            # self.frames[key].pack(side="top", fill="both", expand=True)

        self.show_frame(REQUEST_APPOINTMENTS)

    def show_frame(self, cont):
        frame = self.frames[cont]
        print('Displaying frame:', cont)

        try:
            for f in self.frames.values():
                f.pack_forget()

            frame.pack(side="top", fill="both", expand=True)
            frame.tkraise()

        except Exception as e:
            print(f"Error in show_frame: {e}")

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


class REQUEST_APPOINTMENTS(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.configure(fg_color='white')
        self.available_times = ['Morning', 'Early Afternoon', 'Late Afternoon', 'Evening']
        self.selected_time = None
        self.buttons = []
        self.control = controller

        self.create()
        self.place()
        self.update_selected(0)

    def create_buttons(self):
        for index, time in enumerate(self.available_times):
            print(index, time)

            button = BUTTON(self.time_frame, time)
            button.col = index

            button.bind("<1>", lambda event, widget=button: self.select_button(event, widget))
            self.buttons.append(button)

        return self.buttons

    def select_button(self, event, widget):
        if self.selected_time:
            self.selected_time.change_state()

            widget.change_state()
            self.selected_time = widget

        print(f"Selected time has been changed to: {self.selected_time}")

    def update_selected(self, index):
        if len(self.buttons) > 0:
            self.selected_time = self.buttons[index]
            self.selected_time.change_state()

        return print(f"Selected time has been updated to: {self.selected_time}")

    def update_time(self):
        self.control.appointment_data.update_times(self.selected_time, self.date_entry.selected_button)
        self.control.show_frame(SYMPTOMS)

    def create(self):
        self.title = ctk.CTkLabel(self, text='Request new appointment', text_color='Black',
                                  font=('Arial Bold', 35))
        self.date_entry = CALENDAR(self)
        self.time_frame = ctk.CTkFrame(self, fg_color='white', corner_radius=0)
        self.confirm = ctk.CTkButton(self, fg_color='#b1c9eb', corner_radius=2, text='Confirm Booking',
                                     font=('Arial Bold', 25), text_color='white', hover_color='#7c99c4',
                                     command=lambda: self.update_time())

    def place(self):
        self.title.pack(pady=(80, 5), padx=30, anchor=W)
        self.date_entry.pack(pady=10, padx=30, anchor=W, ipadx=200)
        self.time_frame.pack(pady=15, padx=30, anchor=CENTER)

        buttons = self.create_buttons()
        for button in buttons:
            button.grid(row=0, column=button.col, padx=25, pady=10, sticky='nsew', ipadx=80)

        self.confirm.pack(side='bottom', pady=80, anchor=CENTER, ipadx=20, ipady=5)


class SYMPTOMS(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.controller = controller
        self.configure(fg_color='white')

        self.create()
        self.place()

    def create(self):
        self.title = ctk.CTkLabel(self, text='Discuss your symptoms', text_color='Black',
                                  font=('Arial Bold', 30))
        self.ai_chat = Chat(self)
        self.cancel_button = ctk.CTkButton(self, text='Cancel Request', text_color='white', font=('Arial Bold', 20),
                                           fg_color='#b1c9eb', corner_radius=5)

    def place(self):
        self.title.pack(pady=(80, 5), padx=30, anchor=W)
        self.ai_chat.pack(fill='both', expand=True, padx=30, pady=(20, 0))
        self.cancel_button.pack(side='right', padx=30, pady=(20, 120), ipadx=30, ipady=5)


class DOCTOR_DASHBOARD(DASHBOARD):
    pass
