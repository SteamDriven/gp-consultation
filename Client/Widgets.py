from tkinter import *
from customtkinter import *
from functools import partial
from PIL import Image
from datetime import datetime
from configs import Commands
from helper import ClientCommands

import logging
import threading
import calendar

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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

        self.configure(fg_color=self.fg, corner_radius=4, border_width=1, border_color='light grey')

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
        self.configure(fg_color='#f2f2f2', corner_radius=0)

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

        self.configure(fg_color='#f2f2f2', corner_radius=3)
        self.create_widget()
        self.place_widgets()

    def create_widget(self):
        self.data_frame = CTkFrame(self, fg_color='#f2f2f2')
        self.name_lbl = CTkLabel(self.data_frame, text=self.name, text_color='#737373', font=('Arial light', 14))
        self.cur_time = CTkLabel(self.data_frame, text=f"{datetime.now().strftime('%H:%M')}", text_color='#737373',
                                 font=('Arial light', 13))
        self.cur_date = CTkLabel(self.data_frame, text=f"{datetime.now().strftime('%m/%d/%y')}",
                                 text_color='#737373', font=('Arial light', 13))
        self.message_text = CTkLabel(self, fg_color=self.fg, text=self.message, text_color='#525254',
                                     font=('Arial Light', 15), justify='left', corner_radius=5)

    def place_widgets(self):
        self.data_frame.pack(anchor=W)
        self.name_lbl.pack(side='left', padx=(5, 10))
        self.cur_time.pack(side='left', padx=5)
        self.cur_date.pack(side='right', padx=5)
        self.message_text.pack(padx=5, ipadx=10, ipady=10)


class Chat(CTkFrame):
    DEFAULT_TEXT = 'white'
    DEFAULT_BG = '#4c6fbf'
    DEFAULT_CHAT_BG = '#f2f2f2'

    def __init__(self, master=None, title='Chat', client=None, user_data=None, **kwargs):
        super().__init__(master, **kwargs)

        self.title = title
        self.user_data = user_data
        username = ' '.join(self.user_data.user[1][1:]).title()
        self.ai_states = {
            'greeting': (f"Hello, {username}!. "
                         "Please describe your symptoms in detail. \n"
                         "Include information such as when they started, "
                         "their intensity, \nand any other relevant information."),

            'images': (f"Fantastic, thank you {username}. "
                       "I'll be sure to note those down for you.\n"
                       "If possible, can you please attach any relevant images of affected areas\nor symptoms you're "
                       "having and if not, don't you worry about it."),

            'no-images': ("I see you've decided not to include any images.\n"
                          "That's no problem, you will be able to attach images to your profile later."),

            'yes-images': ("Thank you for submitting your images.\n"
                           "This will help aid your GP in diagnosis."),

            "prompt": ("Would you like to choose a specific GP from our\n"
                       "provided list of available clinicians?"),

            "declined": (f"Great thank you {username}, I really appreciate that. "
                         "Your request will be sent to an available clinician whom will be assigned\n"
                         "to you shortly. All your details provided today will be provided too. Be sure"
                         "to look out on your 'Notifications' tab for request acceptance.\n\nHave a nice day!."),

            'confused': f"I apologise {username}, I didn't get that. Could you please message again?",

            "accepted": "Please select one of the available GPs listed below:",

            "completed": f"""Great, thank you {username}. Your request has been sent to DR JANE DOE, 
                            along with all your submitted details today. You'll be notified on your dash when your 
                            request has been accepted. Be sure to keep a look out on your NOTIFICATIONS tab. 
                            
                            Have a nice day!"""
        }
        self.container = None
        self.client = client
        self.label = None
        self.chat_frame = None
        self.chat_box = None
        self.upload_frame = None
        self.state = 'client'
        self.user_responses = {}
        self.current_state = "greeting"
        self.cur_row = 0

        self.setup_chat()
        self.create_chat()

    def listen_for_messages(self):
        logging.info(f"Listening for messages.")
        while True:
            messages = self.client.receive_message()
            logging.info(f"Received message: {messages}")

            if messages['COMMAND'] == Commands.chat_commands['receive']:
                self.create_client_message(messages['DATA'], '#e8ebfa', messages['CLIENT'])

    def start_message_listener(self):
        logging.info(f"Creating message listener.")
        threading.Thread(target=self.listen_for_messages).start()

    def setup_chat(self):
        self.container = CTkFrame(self, fg_color=self.DEFAULT_CHAT_BG, corner_radius=0)
        self.label = Label(self.container, text=self.title)
        self.chat_frame = CTkScrollableFrame(self.container, fg_color=self.DEFAULT_CHAT_BG, corner_radius=0)

        if self.state == 'ai':
            self.chat_box = ChatEntry(self.container, command=self.handle_ai_chat)

        elif self.state == 'client':
            self.chat_box = ChatEntry(self.container, command=self.send_message)

    def disable_chat(self):
        self.chat_box.pack_forget()

    def create_chat(self):
        self.container.pack(fill='both', expand=True)
        self.label.pack(fill='x', ipady=5)
        self.chat_frame.pack(fill='both', expand=True, pady=(0, 10))
        self.chat_box.pack(side='bottom', fill='x', pady=15, padx=15, ipady=5)

    def ignore_upload(self):
        self.upload_frame.destroy()
        self.upload_frame = None

        self.create_service_message(f"{self.ai_states['no-images']}")
        self.current_state = 'prompt'

        self.create_service_message(f"{self.ai_states[self.current_state]}")

    def get_message(self):
        message = self.chat_box.txt.get_message()
        return message

    def send_message(self):
        message = self.get_message()
        user_id = self.user_data.user[1][0]

        logging.info(f"USER {user_id} is sending a message.")
        ClientCommands.handle_chat(self.client, message, Commands.chat_commands['broadcast'], user_id)
        self.create_client_message(message, 'white', 'Test')

    def handle_ai_chat(self):
        message = self.get_message()
        logging.info('Chat set to AI state, only one client connected.')

        logging.info(f"User response: {message}")
        logging.info(f"User chat state: {self.current_state}")

        if not message:
            self.create_service_message(f"{self.ai_states['confused']}")
            return

        if self.current_state == 'greeting':
            self.user_data.symptoms = message
            self.current_state = 'images'

        self.create_client_message(f"{message}", 'white', ' '.join(self.user_data.user[1][1:]))

        if self.current_state == 'images' and self.upload_frame is not None:
            logging.info("User has already received an offer to upload symptoms.")

            uploaded_images = self.upload_frame.get_children()
            if not uploaded_images:
                self.create_service_message(f"{self.ai_states['no-images']}")

            else:
                self.create_service_message(f"{self.ai_states['yes-images']}")

            self.current_state = 'prompt'
            self.create_service_message(f"{self.ai_states[self.current_state]}")
            return

        if self.current_state == 'prompt':
            if "yes" in message.lower():
                self.current_state = 'accepted'

            elif "no" in message.lower():
                self.current_state = 'declined'

                self.create_service_message(f"{(self.ai_states[self.current_state])}")
                self.disable_chat()

                if self.upload_frame:
                    self.user_data.images = self.upload_frame.images
            else:
                self.create_service_message(f"{self.ai_states['confused']}")

        if self.current_state == 'images' and not self.upload_frame:
            self.create_service_message(f"{self.ai_states[self.current_state]}")
            self.upload_frame = UploadFrame(self.chat_frame)
            self.upload_frame.cancel.configure(command=self.ignore_upload)
            self.upload_frame.pack()

    def create_service_message(self, message):
        chat = MessageBox(self.chat_frame, message=message, name="Service")
        chat.pack()

    def create_client_message(self, message, color, name):
        chat = MessageBox(self.chat_frame, message=message, fg=color,
                          name=name)
        chat.pack()


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

    def __init__(self, master=None, day=None, date=None, colour='green', **kwargs):
        super().__init__(master, **kwargs)

        self.day = day
        self.date = date
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
        week = cal[self.current_week]

        for row, day in enumerate(week):
            frame = DateFrame(self.day_frame, colour='#f2f2f2')

            if day == 0:
                state = False
            else:
                state = True

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


class ImageButton(CTkFrame):
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

        self.logo = None
        self.btn = None

        self.configure(fg_color=self.background_color, corner_radius=0)

        self.setup_widgets()
        self.place_widgets()

    def setup_widgets(self):
        image = Image.open(self.img_path)
        image_ck = CTkImage(image, size=self.size)

        self.logo = CTkLabel(self, image=image_ck, text='')
        self.btn = CTkButton(self, text=self.text, text_color='white', font=self.font,
                             fg_color=self.background_color, hover_color='#202f50', corner_radius=0,
                             anchor='w', command=self.command)

    def place_widgets(self):
        self.logo.grid(row=0, column=0, sticky='ew')
        self.btn.grid(row=0, column=1, columnspan=2, sticky='ew')
