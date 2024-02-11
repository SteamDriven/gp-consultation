import random
from tkinter import *
from customtkinter import *
from os.path import *
from functools import partial
from PIL import Image
from datetime import datetime
from configs import Commands
from helper import ClientCommands
from textwrap import *

import logging
import threading
import calendar

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
cmds = Commands.packet_commands
appt_cdms = cmds['appointments']


class Label(CTkFrame):
    DEFAULT_FONT = ('Arial Bold', 25)

    def __init__(self, master=None, color='white', bg='#4c6fbf', text='Loading', font=None, side=None, state='normal',
                 **kwargs):
        super().__init__(master, **kwargs)

        self.text_col = color
        self.fg = bg
        self.text = text
        self.state = state
        self.textbox = None
        self.client_message = None

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

        self.configure(fg_color=self.fg, border_color='light grey')

        self.label = CTkLabel(self, text=self.text, fg_color=self.fg, text_color=self.text_col,
                              font=self.font)

        self.label.pack(side=self.side, padx=10)

    def get_message(self):
        self.client_message = self.textbox.get("0.0", "end")

        if not self.client_message.strip():
            self.textbox.delete("0.0", "end")
            return False

        self.textbox.delete("0.0", "end")
        return self.client_message

    def create_textbox(self):
        self.textbox = CTkTextbox(self, fg_color=self.fg, text_color=self.text_col, font=self.font, corner_radius=0,
                                  border_width=0, height=10)
        self.textbox.focus_set()
        self.textbox.bind("<Return>", self.change_type)

    def change_type(self, event):
        if self.textbox:
            self.textbox.pack_forget()
            self.textbox = None

            self.label = CTkLabel(self, text=self.text, fg_color=self.fg, text_color=self.text_col,
                                  font=self.font)
            self.label.pack(side=self.side, padx=10)

        else:
            print('Changing to entry.')
            self.create_textbox()
            self.label.pack_forget()
            self.textbox.pack(side=self.side, fill='x', expand=True, padx=10)


class ChatEntry(CTkFrame):
    DEFAULT_TEXT_COL = 'grey'
    DEFAULT_ENTRY_FONT = ('Arial Light', 15)
    DEFAULT_FONT = ('Arial Bold', 25)

    def __init__(self, master=None, placeholder='Type a message', command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.command = command
        self.configure(fg_color='white', corner_radius=3, border_color='#e7e5e5', border_width=3)

        self.setup_box()
        self.place_box()

    def setup_box(self):
        image = Image.open("Images/Send.PNG")
        image_ck = CTkImage(image, size=(28, 28))

        self.txt = Label(self, text=self.placeholder, bg='white', font=self.DEFAULT_ENTRY_FONT, side='left',
                         color=self.DEFAULT_TEXT_COL, state='special')
        self.send_button = CTkButton(self.txt, text='', fg_color='white', command=self.command, hover=False,
                                     image=image_ck, width=5)

    def place_box(self):
        self.send_button.pack(side='right', padx=5)
        self.txt.pack(fill='both', expand=True, anchor=CENTER, padx=5, pady=5)


class UploadFrame(CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.header = None
        self.container = None
        self.browse = None
        self.cancel = None
        self.upload_image = None
        self.description = None
        self.photo = None
        self.images = []

        self.configure(fg_color='white', corner_radius=0, height=500, width=600)
        self.pack_propagate(False)

        self.create_frame()
        self.setup_frame()

    def create_frame(self):
        path = 'Images/Upload.PNG'
        image = Image.open(path)
        image_ck = CTkImage(image, size=(88, 49))

        self.header = CTkFrame(self, fg_color='#e7e5e5', corner_radius=0)
        self.upload_image = CTkLabel(self.header, image=image_ck, fg_color='#e7e5e5', text='')
        self.description = CTkLabel(self.header, fg_color='#e7e5e5', text='Upload your images here',
                                    text_color='#737373', font=('Arial light', 20))
        self.container = CTkScrollableFrame(self, fg_color='white', corner_radius=0, orientation='horizontal')
        self.browse = CTkButton(self, fg_color='#7b96d4', corner_radius=0, text='Browse files',
                                text_color='white', font=('Arial Bold', 25), command=self.upload)
        self.cancel = CTkButton(self, fg_color='white', text='No thanks', text_color='grey',
                                font=('Arial light', 15, 'underline'), hover=False)

    def setup_frame(self):
        self.header.pack(side='top', fill='x', anchor=CENTER)
        self.upload_image.pack(side='top', pady=10, anchor=CENTER)
        self.description.pack(anchor=CENTER, pady=5)
        self.container.pack(anchor=CENTER, pady=10, fill='both')
        self.browse.pack(pady=(40, 10), ipadx=25, ipady=10)
        self.cancel.pack(pady=5)

    def get_children(self):
        children = self.container.winfo_children()
        if children:
            return children
        else:
            return False

    def upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        print('done')

        if file_path:
            image = Image.open(file_path)
            image_ck = CTkImage(image, size=(200, 200))

            self.photo = CTkLabel(self.container, image=image_ck, text='', fg_color='white')
            self.photo.pack(side='left', padx=5, pady=10)
            self.images.append(image)


class MessageBox(CTkFrame):
    def __init__(self, master=None, fg='#e8ebfa', message=None, name=None, **kwargs):
        super().__init__(master, **kwargs)

        self.fg = fg
        self.message = message
        self.name = name
        self.message_text = None
        self.data_frame = None
        self.cur_time = None
        self.cur_date = None
        self.name_lbl = None
        self.profile = None

        self.image = None
        self.preview = None

        self.profiles = {
            1: join(dirname(__file__), 'Images/Profiles/1.png'),
            2: join(dirname(__file__), 'Images/Profiles/2.png'),
            3: join(dirname(__file__), 'Images/Profiles/3.png'),
            4: join(dirname(__file__), 'Images/Profiles/4.png'),
            5: join(dirname(__file__), 'Images/Profiles/5.png'),
            6: join(dirname(__file__), 'Images/Profiles/Server.png')
        }

        self.configure(fg_color='white', corner_radius=3)
        self.create_widget()
        self.place_widgets()

    def create_widget(self):
        if self.name[1] == 'Service':
            self.image = Image.open(self.profiles[6])
            self.preview = CTkImage(self.image, size=(100, 95))

        elif self.name[1] == 'Doctor':
            self.image = Image.open(self.profiles[5])
            self.preview = CTkImage(self.image, size=(100, 95))

        else:
            self.image = Image.open(self.profiles[random.randint(1, 4)])
            self.preview = CTkImage(self.image, size=(100, 95))

        self.data_frame = CTkFrame(self, fg_color='white')
        self.profile = CTkLabel(self.data_frame, image=self.preview, text='', fg_color='white')
        self.name_lbl = CTkLabel(self.data_frame, text=self.name[0], text_color='#737373', font=('Arial light', 14))
        self.cur_time = CTkLabel(self.data_frame, text=f"{datetime.now().strftime('%H:%M')}", text_color='#737373',
                                 font=('Arial light', 13))
        self.cur_date = CTkLabel(self.data_frame, text=f"{datetime.now().strftime('%m/%d/%y')}",
                                 text_color='#737373', font=('Arial light', 13))
        self.message_text = CTkLabel(self, fg_color=self.fg, text=self.message, text_color='#525254',
                                     font=('Arial Light', 20), justify='left', corner_radius=5)

    def place_widgets(self):
        self.data_frame.pack(anchor=W)
        self.profile.pack(side='left', padx=5)
        self.name_lbl.pack(side='left', padx=(5, 10),)
        self.cur_time.pack(side='left', padx=5)
        self.cur_date.pack(side='right', padx=5)
        self.message_text.pack(padx=5, ipadx=10, ipady=10)


class Treeview(CTkFrame):
    def __init__(self, master=None, client=None, headers=None, **kwargs):
        super().__init__(master, **kwargs)

        if headers is None:
            headers = [None]
        self.configure(fg_color='#e7e5e5', corner_radius=5)
        self.client = client
        self.header_list = headers
        self.selected_doctor = None
        self.header_frame = None
        self.header = None

        self.create_header()
        self.create_labels()
        self.select_random_doctor()

    @staticmethod
    def change_state(widget, bool):
        if bool:
            widget.configure(fg_color='#7b96d4')

            for child in widget.winfo_children():
                child.configure(fg_color='#7b96d4', text_color='white')

        elif not bool:
            widget.configure(fg_color='#cecaca')

            for child in widget.winfo_children():
                child.configure(fg_color='#cecaca', text_color='black')

    def select_random_doctor(self):
        doctors = []
        for child in self.winfo_children():
            if child == self.header_frame:
                continue
            doctors.append(child)

        self.selected_doctor = random.choice(doctors)
        self.change_state(self.selected_doctor, True)

    def select_doctor(self, event, frame):
        if self.selected_doctor:
            self.change_state(self.selected_doctor, False)
            print(f"Current selected doctor: {self.selected_doctor}")

            self.selected_doctor = frame
            print(f"New doctor: {self.selected_doctor}")
            self.change_state(self.selected_doctor, True)

    def get_selected(self):
        return self.selected_doctor

    def create_header(self):
        self.header_frame = CTkFrame(self, corner_radius=0, fg_color='white')
        self.header_frame.grid(row=0, column=0, sticky='ew', pady=5, padx=5, ipadx=20)

        for count, name in enumerate(self.header_list):
            print(count, name)
            self.header = CTkEntry(self.header_frame, justify='left', corner_radius=0, fg_color='white',
                                   text_color='black',
                                   border_width=0, font=('Arial Light', 18))
            self.header.insert(0, name)
            self.header.configure(state='readonly')

            if name.lower() == 'first name':
                self.header.grid(row=0, column=count, ipadx=20, pady=(5, 0))
            elif name.lower() == 'last name':
                self.header.grid(row=0, column=count, ipadx=20, pady=(5, 0), padx=(0, 5))
            else:
                self.header.grid(row=0, column=count, pady=(5, 0), padx=(5, 0))

    def create_labels(self):
        doctors = ClientCommands.request_doctor(self.client)

        if doctors:
            for count, doctor in enumerate(doctors):
                print(count, doctor)
                frame = CTkFrame(self, fg_color='#cecaca', corner_radius=3, border_width=0)
                frame.grid(row=count + 3, column=0, pady=(0, 5), padx=5, sticky='ew', ipadx=20)

                for col, info in enumerate(doctor):
                    print(col, info)
                    label = CTkEntry(frame, text_color='black', justify='left', fg_color='#cecaca', border_width=0,
                                     font=('Arial light', 15), height=10)
                    label.insert(0, info)
                    label.configure(state='readonly')
                    label.bind("<1>", lambda event, frame=frame: self.select_doctor(event, frame))

                    if col == 1:
                        label.grid(row=0, column=col, pady=5, ipadx=20, sticky='ew')
                    elif col == 2:
                        label.grid(row=0, column=col, pady=5, padx=(0, 5), ipadx=20, sticky='ew')
                    label.grid(row=0, column=col, pady=5, padx=(5, 0), sticky='ew')
        else:
            print('No doctors found.')


class SearchBar(CTkFrame):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(fg_color='white')
        self.container = None
        self.entry_box = None
        self.image = None

        self.create()
        self.setup()

    def create(self):
        image_path = join(dirname(__file__), 'Images/search.png')

        self.container = CTkFrame(self, fg_color='white')
        self.image = CTkLabel(self.container, image=CTkImage(Image.open(image_path), size=(40, 36)), fg_color='white',
                              text='')
        self.entry_box = CTkEntry(self.container, placeholder_text='Search for a patient', fg_color='white',
                                  border_width=0, text_color='#636363', font=('Arial light', 18))

    def setup(self):
        self.container.pack(side='top', fill='both', expand=True)
        self.image.pack(side='left', padx=10)
        self.entry_box.pack(fill='x', pady=5, ipadx=15)


class InfoEntry(CTkFrame):

    def __init__(self, master=None, placeholder="", show_bullet=False, font=None, min_width=None, **kwargs):
        super().__init__(master, **kwargs)

        # CONFIGURATIONS
        self.placeholder = placeholder
        self.show_bullet = ""

        if show_bullet:
            self.show_bullet = '*'

        self.label = CTkLabel(self, text=self.placeholder, fg_color='#4c70c0', text_color='white',
                              font=('Calibri Light', 25))
        self.label.grid(row=0, column=0, pady=5, padx=5, sticky='w')

        self.entry = CTkEntry(self, show=self.show_bullet, width=min_width, font=font, border_width=1,
                              corner_radius=10, fg_color='white', text_color='black', border_color='black')
        self.entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, ipady=20)

    def get_entry(self):
        current_val = self.entry.get()
        return current_val if current_val != self.placeholder else False

    def clear_entry(self):
        self.entry.delete(0, END)


class Button(CTkFrame):
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

        self.label = None

        self.configure(corner_radius=0, fg_color=self.DISABLED_BG)

        self.create_widgets()
        self.place_widgets()

    def __str__(self):
        return f"BUTTON: {self.placeholder}, {self.state}"

    def create_widgets(self):
        self.label = CTkLabel(self, text=self.placeholder, fg_color=self.DISABLED_BG, text_color=self.DISABLED_TEXT,
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


class DateFrame(CTkFrame):
    DISABLED_TEXT = '#0f0e0c'
    ENABLED_TEXT = '#ffffff'
    ENABLED_BG = '#4c6fbf'

    def __init__(self, master=None, day=None, date=None, month=None, year=None, colour='green', **kwargs):
        super().__init__(master, **kwargs)

        self.day = day
        self.date = date
        self.month = month
        self.year = year
        self.colour = colour
        self.state = 'DISABLED'

        self.day_label = None
        self.date_label = None

        self.configure(fg_color=self.colour)

    def __str__(self):
        return f"BUTTON: {self.day.upper()}, {self.date}, {self.state}"

    def create_labels(self):
        self.day_label = CTkLabel(self, text_color=self.DISABLED_TEXT, text=self.day, fg_color=self.colour,
                                  font=('Arial Bold', 35))
        self.date_label = CTkLabel(self, text_color=self.DISABLED_TEXT, text=self.date, fg_color=self.colour,
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


class Calendar(CTkFrame):
    LEFT_ARROW_PATH = "Images/Left_arrow.PNG"
    RIGHT_ARROW_PATH = "Images/Right_arrow.PNG"

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.year = None
        self.month = None
        self.current_week = None
        self.buttons = []
        self.selected_button = None

        self.left_arrow = None
        self.day_frame = None
        self.right_arrow = None

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
        today = datetime.now()

        if index == 0:
            for button in self.buttons:
                if button.date == today.day and button.month == today.month and button.year == today.year:
                    self.selected_button = button
                    self.selected_button.change_state()

                    break
        else:
            self.selected_button = random.choice(self.buttons)
            self.selected_button.change_state()

        print(f'{self.selected_button} has been chosen based on today.')

    def display_buttons(self):
        if len(self.buttons) > 0:
            for button in self.buttons:
                print(button)

    def set_current_date(self):
        today = datetime.now()
        self.year = today.year
        self.month = today.month

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
        self.day_frame = CTkFrame(self, fg_color='#f2f2f2')
        self.day_frame.grid(row=0, column=1, pady=40)

        left_image = Image.open(self.LEFT_ARROW_PATH)
        right_image = Image.open(self.RIGHT_ARROW_PATH)
        left_image_ck = CTkImage(left_image, size=(61, 73))
        right_image_ck = CTkImage(right_image, size=(69, 76))

        next_week = partial(self.change_week, True)
        prev_week = partial(self.change_week, False)

        self.left_arrow = CTkButton(self, image=left_image_ck, text='', fg_color='#f2f2f2', hover=False,
                                    command=prev_week)
        self.right_arrow = CTkButton(self, image=right_image_ck, text='', fg_color='#f2f2f2', hover=False,
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

        # Ensure that the current_week is within a valid range
        if 0 <= self.current_week < len(cal):
            week = cal[self.current_week]
            print(f"{self.current_week} is the current week we're in.")

            for i, day in enumerate(week):
                self.display_day(i, day)

    def display_day(self, column, day):
        frame = DateFrame(self.day_frame, colour='#f2f2f2')

        if day == 0:
            state = False
        else:
            state = True

        if state:
            weekday = self.get_day(datetime(self.year, self.month, day))
            frame.date = day
            frame.day = weekday
            frame.year = self.year
            frame.month = self.month

            print(frame.date, frame.day, frame.year, frame.month)

            frame.create_labels()
            frame.place_widgets()
            frame.grid(row=0, column=column, sticky='nsew', padx=15)

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
        self.select_date(1)

    def select_button(self, event, button):
        print(f"{button} has been selected. Current selected date is {self.selected_button}")

        if self.selected_button:
            self.selected_button.change_state()

            button.change_state()
            self.selected_button = button

        print(f"Selected date has been changed to: {self.selected_button}")


class ImageButton(CTkFrame):
    def __init__(self, master=None, description=None, path=None, size=None, fg=None, font=None, command=None, **kwargs):
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

        self.logo = None
        self.btn = None

        self.configure(fg_color=self.background_color, corner_radius=0)

        self.setup_widgets()
        self.place_widgets()

    def setup_widgets(self):
        image = Image.open(self.img_path)
        image_ck = CTkImage(image, size=self.size)

        if self.text is None:
            self.logo = CTkButton(self, image=image_ck, text='', hover_color='#202f50', fg_color=self.background_color)
        else:

            self.logo = CTkLabel(self, image=image_ck, text='')
            self.btn = CTkButton(self, text=self.text, text_color='white', font=self.font,
                                 fg_color=self.background_color, hover_color='#202f50', corner_radius=0,
                                 anchor='w', command=self.command)

    def place_widgets(self):
        if self.text is None:
            self.logo.grid(row=0, column=0, sticky='ew')

        else:
            self.logo.grid(row=0, column=0, sticky='ew')
            self.btn.grid(row=0, column=1, columnspan=2, sticky='ew')


class Notification_Box(CTkFrame):
    def __init__(self, master=None, message='None', header='service', status=None, timestamp=None, delete=None,
                 change=None, identifier=None, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color='white')
        self.headers = {

            'system':           ['System', '#7ed957'],
            'doctor':           ['Doctor', '#8c52ff'],
            'patient':          ['Patient', '#ff914d'],
            'reminder':         ['Reminder', '#f366ba'],
            'booking':          ['Booking', '#78d1cc'],
            'consultation':     ['Consultation', '#0cc0df']
        }

        self.type = self.headers[header]

        self.header = None
        self.title = None
        self.identifier = identifier
        self.message = message
        self.delete_func = delete
        self.change_func = change
        self.message_label = None
        self.time = timestamp
        self.status_label = None
        self.status = status
        self.exit_btn = None
        self.separator = None
        self.left_frame = None
        self.right_frame = None
        self.timestamp_frame = None
        self.clock = None
        self.timestamp = None
        self.header_frame = None

        self.patient_id = None
        self.doctor_id = None

        self.exit_image_path = join(dirname(__file__), "Images/Exit.PNG")
        self.clock_image_path = join(dirname(__file__), "Images/Clock.PNG")
        self.exit_ck = CTkImage(Image.open(self.exit_image_path), size=(40, 40))
        self.clock_ck = CTkImage(Image.open(self.clock_image_path), size=(40, 39))

        self.font_1 = CTkFont('Arial', 20, 'bold')
        self.font_2 = CTkFont('Arial', 14, 'normal')
        self.font_3 = CTkFont('Arial', 14, 'bold')

        self.setup()
        self.create()

        if self.type[0] == 'Patient':
            print('Notification type is PATIENT. Changing state.')

            self.patient_id = self.message[2]

            if self.right_frame:
                self.right_frame.bind('<Double-Button-1>', lambda event: self.change_func(self.patient_id, message[3:]))

        elif self.type[0] == 'Booking':
            print('Notification type is BOOKING. Changing state.')

            if self.right_frame:
                start_chat = CTkButton(self.right_frame, text='Start a new chat', text_color='white', fg_color='#b1c9eb'
                                       ,font=('Arial bold', 20), command=lambda: self.change_func)
                start_chat.pack(padx=10, anchor=W, ipadx=5)

        elif self.type[0] == 'Consultation':
            if self.right_frame:
                accept_invite = CTkButton(self.right_frame, text='Start a new chat', text_color='white', fg_color='#b1c9eb'
                                       ,font=('Arial bold', 20), command=lambda: self.change_func)

        # elif self.type[0] == 'System':
        #     self.doctor_id = self.message[2]

    def setup(self):
        self.left_frame = CTkFrame(self, fg_color='white', corner_radius=0, width=10)
        self.right_frame = CTkFrame(self, fg_color='white', corner_radius=0)
        self.exit_btn = CTkButton(self.left_frame, image=self.exit_ck, hover=False, fg_color='white',
                                  text='', height=10, width=10, command=self.delete_notification)

        self.header_frame = CTkFrame(self.right_frame, fg_color='white')
        self.header = CTkLabel(self.header_frame, text_color='white', text=self.type[0],
                               fg_color=self.type[1], font=self.font_1, justify='left', corner_radius=5)
        self.timestamp_frame = CTkFrame(self.header_frame, fg_color='white')
        self.clock = CTkLabel(self.timestamp_frame, image=self.clock_ck, fg_color='green', text='')
        self.timestamp = CTkLabel(self.timestamp_frame, text=self.time, text_color='#e7e5e5', font=self.font_3)

        self.title = CTkLabel(self.right_frame, text=self.message[0], text_color='#737373', font=self.font_1)
        self.message_label = CTkLabel(self.right_frame, text=self.message[1], text_color='#737373', justify='left',
                                      font=self.font_2)
        self.status = CTkLabel(self.right_frame, text=f'Status: {self.status}', text_color='#ff5757', font=self.font_3)
        self.separator = CTkFrame(self, fg_color='#e7e5e5', height=8, corner_radius=10)

    def create(self):
        self.left_frame.pack(side='left', padx=(2, 15), pady=5, fill='both', ipadx=10)
        self.right_frame.pack(padx=5, pady=5, fill='both', expand=True, ipadx=280)

        self.exit_btn.pack(side='top', anchor=W)
        self.header_frame.pack(padx=10, pady=(10, 0), anchor=W, fill='x', expand=True)

        self.header.pack(side='left', padx=10, anchor=W, ipadx=20)
        self.timestamp_frame.pack(side='right', padx=10, anchor=E)
        self.clock.pack(side='left', pady=5)
        self.timestamp.pack(side='left', padx=2, pady=10)

        self.title.pack(padx=10, anchor=W)
        self.message_label.pack(padx=10, anchor=W)
        self.status.pack(padx=10, anchor=W)
        self.separator.pack(side='bottom', padx=5, pady=5, fill='x', expand=True)

    def delete_notification(self):
        self.delete_func(self.identifier)
        self.destroy()


class Selector(CTkFrame):
    def __init__(self, master=None, label=None, times=None, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color='#f2f2f2')

        # Configs
        self.label = label
        self.times = times

        # Widgets
        self.label_w = None
        self.left_frame = None
        self.right_frame = None
        self.desc_w = None
        self.times_options = None
        self.separator = None

        self.create_widgets()
        self.setup_widgets()

    def get_time(self):
        return self.times_options.get()

    def create_widgets(self):
        self.left_frame = CTkFrame(self, fg_color='#f2f2f2')
        # self.right_frame = CTkFrame(self, fg_color='#f2f2f2')
        self.label_w = CTkLabel(self.left_frame, text=self.label, text_color='#737373', font=('Arial Bold', 18),
                                justify='left')
        self.times_options = CTkComboBox(self.left_frame, values=self.times, fg_color='white', border_color='#737373',
                                         button_color='#cecaca', button_hover_color='#a2a1a1')
        self.times_options.set(self.times[0])
        self.separator = CTkFrame(self, fg_color='#cecaca', height=2)

    def setup_widgets(self):
        self.left_frame.pack(side='top', padx=5, pady=10, fill='x', expand=True, ipadx=20, anchor=W)
        # self.right_frame.pack(side='top', padx=5, pady=10, fill='x', expand=True, anchor=E)
        self.label_w.pack(side='left', padx=10, pady=(10, 0), anchor=W)
        self.times_options.pack(side='right', padx=10, pady=10, anchor=E, ipadx=4)
        self.separator.pack(side='top', padx=15, pady=15, fill='x', expand=True)


class Chat_Button(CTkFrame):
    def __init__(self, master, patient_name, message, **kwargs):
        super().__init__(master, **kwargs)

        self.name = patient_name
        self.recent_message = message

        self.profile_picture = None
        self.left_frame = None
        self.right_frame = None
        self.separator = None
        self.name_label = None
        self.message_label = None

    def create_widgets(self):
        self.left_frame = CTkFrame(self, fg_color='white')
        self.right_frame = CTkFrame(self, fg_color='white')
        self.profile_picture = CTkFrame(self.left_frame, fg_color='blue')
        self.name_label = CTkLabel(self.right_frame, fg_color='white', text_color='#737373',
                                   font=('Arial bold', 23), justify='left')
        self.message_label = CTkLabel(self.right_frame, fg_color='white', text_color='#737373',
                                      font=('Arial light', 17), justify='left')

    def setup_widgets(self):
        self.left_frame.pack(side='left', padx=10, pady=10, fill='x', expand=True)
        self.right_frame.pack(padx=10, pady=10, fill='x', expand=True)
        self.profile_picture.pack(padx=10, pady=10, fill='both', expand=True)
        self.name_label.pack(side='top', padx=10, pady=25, anchor=W)
        self.message_label.pack(padx=10, pady=5, anchor=W)
