from datetime import datetime
import logging
import threading

from customtkinter import *

from Client.Widgets import MessageBox, cmds, appt_cdms, Treeview, Label, ChatEntry, UploadFrame
from Client.helper import ClientCommands


class Chat(CTkFrame):
    DEFAULT_TEXT = 'white'
    DEFAULT_BG = '#4c6fbf'
    DEFAULT_CHAT_BG = 'white'
    MESSAGE_WIDTH = 80

    def __init__(self, master=None, title='Consultation', client=None, user_data=None, callback=None, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color='white')

        # Constants
        self.current_state = "greeting"
        today = (datetime.now().date()).strftime('%A')

        # Variables
        self.user_data = user_data
        self.client = client
        self.title = title
        self.callback = callback
        self.announcements = {
            1: [today, 'date'],
            2: ['You created a new consultation', 'message'],
            3: ['You invited Adriel McBean to the consultation', 'message'],
        }

        self.example_message_server = ('Dear [Patient], '
                                       'This is a friendly reminder about your current '
                                       'consultation. The session is about '
                                       'to commence.\nPlease ensure you are in a quiet and '
                                       'comfortable environment for the '
                                       'consultation.\nIf you have any questions or need '
                                       'assistance, feel free to ask.\n\n'
                                       'Thank you for choosing our consultation service. We '
                                       'look forward to assisting you.'
                                       '\nBest regards,\n'
                                       'GP Consultation Service')

        self.example_message_patient = ('Hello! I have a few questions about my recent test results. Could you please '
                                        'go over them with me during our scheduled consultation tomorrow at 2:00 PM? '
                                        'I want to better understand the implications and discuss potential treatment '
                                        'options. Thank you!')

        self.example_message_doctor = ("Hello Adriel! Thank you for reaching out. I appreciate your proactive "
                                       "approach to understanding your test results. I'll be prepared to discuss them "
                                       "with you during our scheduled consultation tomorrow at 2:00 PM. Please feel "
                                       "free to jot down any specific questions or concerns you have, so we can make "
                                       "the most of our time together. Looking forward to our discussion!")

        # Widgets
        self.container = None
        self.label = None
        self.chat_frame = None
        self.chat_box = None
        self.upload_frame = None
        self.left_frame = None
        self.right_frame = None
        self.spacer = None

        # Methods
        self.create_widgets()
        self.setup()

        self.start_message_listener()
        # self.create_service_message(self.example_message_server)
        # self.create_client_message(self.example_message_patient, '#f2f2f2', ['Adriel McBean', 'Patient'],
        #                            'sender')
        # self.create_client_message(self.example_message_doctor, '#f2f2f2', ['Dr John Doe', 'Doctor'],
        #                            'receiver')

    # def create_session(self, booking_reference, clinician, patient):
    #     if booking_reference not in self.session:
    #
    #         self.session[booking_reference] = {
    #             'doctor': clinician,
    #             'patient': patient,
    #             'messages': {}
    #         }

    def listen_for_messages(self):
        logging.info(f"Listening for messages.")
        while True:
            messages = self.client.receive_message()
            logging.info(f"Received message: {messages}")

            if messages['COMMAND'] == cmds.chat_commands['receive']:
                role, name, message = messages['DATA'][0], messages['DATA'][1], messages['DATA'][2]

                self.create_client_message(message, '#e8ebfa', [name, role], 'recipient')

    def start_message_listener(self):
        logging.info(f"Creating message listener.")
        threading.Thread(target=self.listen_for_messages).start()

    def create_widgets(self):
        self.header = CTkFrame(self, fg_color='white', bg_color='white', border_color='#e7e5e5', border_width=3,
                               height=30)
        self.label = CTkLabel(self.header, text=self.title, fg_color='white', text_color='grey',
                              font=('Arial light', 23))
        self.container = CTkScrollableFrame(self, fg_color=self.DEFAULT_CHAT_BG, corner_radius=0)
        self.chat_box = ChatEntry(self, command=self.send_message())

    def disable_chat(self):
        self.chat_box.pack_forget()

    def setup(self):
        self.header.pack(side='top', fill='x')
        self.label.pack(side='left', padx=10, pady=10)
        self.container.pack(side='top', fill='both', expand=True)
        self.introduction()

        self.chat_box.pack(side='bottom', fill='x', pady=(15, 2))

    def get_message(self):
        message = self.chat_box.txt.get_message()
        return message

    def send_message(self, recipient):
        message = self.get_message()
        username = ' '.join(self.user_data.user[1:]).title()

        message = ClientCommands.handle_chat(self.client, message, cmds.chat_commands['broadcast'])
        role, name, user_message = message[0], message[1], message[2]

        self.create_client_message(user_message, '#f2f2f2', [name, role], 'origin')

    def create_spacer(self, parent, anchor):
        spacer = CTkFrame(parent, fg_color=self.DEFAULT_CHAT_BG, corner_radius=0)
        spacer.pack(side='top', fill='x', anchor=anchor)

    def introduction(self):
        for msg in self.announcements.values():
            self.create_announcement(msg[1], msg[0])

    def create_announcement(self, state: str, message: str):
        container = CTkFrame(self.container, fg_color='white')
        if state == 'message':
            label = CTkLabel(container, text=message, text_color='#e7e5e5', anchor=CENTER, font=('Arial bold', 20))
            label.pack(side='top', anchor=CENTER)
            container.pack(side='top', anchor=CENTER, padx=10, pady=5, fill='x', expand=True)

        elif state == 'date':
            line = CTkFrame(container, fg_color='#e7e5e5', height=5)
            line2 = CTkFrame(container, fg_color='#e7e5e5', height=5)
            date = CTkLabel(container, fg_color='white', text=message, text_color='#cecaca',
                            font=('Arial bold', 20), anchor=CENTER)

            container.pack(side='top', anchor=CENTER, padx=10, pady=10, fill='x', expand=True)
            line.pack(side='left', padx=5, anchor=W, fill='x', expand=True)
            date.pack(side='left', padx=5, fill='x', expand=True)
            line2.pack(side='left', anchor=E, padx=5, fill='x', expand=True)

    def create_service_message(self, message):
        new_message = ClientCommands.format_paragraph(message, self.MESSAGE_WIDTH)
        print(new_message)

        chat = MessageBox(self.container, message=new_message, name=['GP Consultation: Customer Service', "Service"])
        chat.pack(side='top', anchor=W, pady=5)

    def create_client_message(self, message, color, name, client):
        new_message = ClientCommands.format_paragraph(message, self.MESSAGE_WIDTH)
        print(new_message)
        if client == 'origin':
            chat = MessageBox(self.container, message=new_message, fg=color, name=name)
            chat.pack(side='top', anchor=E, pady=5)

        elif client == 'recipient':
            chat = MessageBox(self.container, message=new_message, name=name)
            chat.pack(side='top', anchor=W, pady=5)


class aiChat(Chat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.username = ' '.join(self.user_data.user[1][1:]).title()
        self.username = ''
        self.ai_states = {
            'greeting': (f"Hello, {self.username}! "
                         "Please describe your symptoms in detail.\n"
                         "Include information such as when they started,"
                         "their intensity,\nand any other relevant information."),

            'images': (f"Fantastic, thank you {self.username}. "
                       "I'll be sure to note those down for you.\n"
                       "If possible, can you please attach any relevant images of affected areas\nor symptoms you're "
                       "having and if not, don't you worry about it."),

            'no-images': ("I see you've decided not to include any images.\n"
                          "That's no problem, you will be able to attach images to your profile later."),

            'yes-images': ("Thank you for submitting your images.\n"
                           "This will help aid your GP in diagnosis."),

            "prompt": ("Would you like to choose a specific GP from our\n"
                       "provided list of available clinicians?"),

            "declined": (f"Great thank you {self.username}, I really appreciate that. "
                         "Your request will be sent to an available clinician whom will be assigned\n"
                         "to you shortly. All your details provided today will be provided too. Be sure"
                         "to look out on your 'Notifications' tab for request acceptance.\n\nHave a nice day!."),

            'confused': f"I apologise {self.username}, I didn't get that. Could you please message again?",

            "accepted": "Please select one of the available GPs listed below:",

            "completed": (f"Great, thank you {self.username}, I really appreciate your cooperation today.\n"
                          f"Your request has been sent to your chosen GP, named Dr John Doe along\n"
                          "with all your entered details. You will be notified on your dashboard when your request\n"
                          "has been accepted. Be sure to keep a look out on your NOTIFICATIONS tab.\n\nHave a nice day!"
                          )}

        self.title = 'Discuss your symptoms'
        self.chat_box.configure(command=self.handle_ai_chat)
        self.create_service_message(f"{self.ai_states[self.current_state]}")

    def ignore_upload(self):
        self.upload_frame.destroy()
        self.upload_frame = None

        self.create_service_message(f"{self.ai_states['no-images']}")

        self.current_state = 'prompt'
        self.create_service_message(f"{self.ai_states[self.current_state]}")
        self.current_state = 'accepted'

    def handle_ai_chat(self):
        message = self.get_message()
        logging.info('Chat set to AI state, only one client connected.')

        logging.info(f"User response: {message}")
        logging.info(f"User chat state: {self.current_state}")

        if not message:
            if self.current_state == 'completed':
                if self.doctor_list:
                    doctor_info = []
                    selected = self.doctor_list.get_selected()

                    for label in selected.winfo_children():
                        doctor_info.append(label.get())

                    logging.info(f"User has selected DOCTOR: {doctor_info}")
                    self.assigned_doctor = doctor_info
                    self.user_data.doctor = ['DOCTOR', self.assigned_doctor]

                    if "John Doe" in self.ai_states['completed']:
                        print(' '.join(self.user_data.doctor[1][1:]).title())
                        self.ai_states['completed'] = self.ai_states['completed'].replace("John Doe",
                                                                                          ' '.join(
                                                                                              self.user_data.doctor[
                                                                                                  1][
                                                                                              1:]).title())

                    self.create_service_message(f"{(self.ai_states['completed'])}")
                    self.disable_chat()

                    logging.info(f"Sending USER: {self.user_data.user}'s appointment booking for processing.")

                    print(f"{self.user_data.user}'s is the USER who has requested a booking.")
                    print(f"{self.user_data.doctor} is the USER's assigned doctor.")

                    data_dict = self.user_data.to_dict()

                    received_update = ClientCommands.set_appointment(
                        self.client,
                        self.user_data.user[0],
                        appt_cdms['create apt'],
                        data_dict
                    )

                    page_packet = [self.user_data.day, self.user_data.time, self.user_data.symptoms,
                                   self.user_data.images, ' '.join(self.user_data.doctor[1][1:]).title()]

                    self.callback(page_packet)

                    if received_update:
                        logging.info(f'Received notification: {received_update}')

            self.create_service_message(f"{self.ai_states['confused']}")
        # return

        if self.current_state == 'greeting':
            self.user_data.symptoms = message
            self.current_state = 'images'

        self.create_client_message(message, 'white', ' '.join(self.user_data.user[1][1:]).title())

        if self.current_state == 'images' and self.upload_frame is not None:
            logging.info("User has already received an offer to upload symptoms.")

            uploaded_images = self.upload_frame.get_children()
            if not uploaded_images:
                self.create_service_message(f"{self.ai_states['no-images']}")

            else:
                self.create_service_message(f"{self.ai_states['yes-images']}")

            self.current_state = 'prompt'
            self.create_service_message(f"{self.ai_states[self.current_state]}")
            self.current_state = 'accepted'

        if self.current_state == 'accepted':
            if "yes" in message.lower():

                self.create_service_message(f"{(self.ai_states[self.current_state])}")
                self.doctor_list = Treeview(self.left_frame, self.client, ['ID', 'First Name', 'Last Name'])
                self.doctor_list.pack(side='top', pady=10, padx=40, anchor=W)

                done = CTkButton(self.left_frame, text='Done', text_color='white', fg_color='#7b96d4',
                                 command=self.handle_ai_chat, height=10, width=10)
                done.pack(side='top', pady=10, padx=10, anchor=W, ipadx=10, ipady=5)
                self.current_state = 'completed'

            elif "no" in message.lower():
                self.current_state = 'declined'
                self.create_service_message(f"{(self.ai_states[self.current_state])}")
                self.disable_chat()

                if self.upload_frame:
                    self.user_data.images = self.upload_frame.images

                    logging.info(f"Sending USER: {self.user_data.user}'s appointment booking for processing.\n"
                                 f"They've chosen to have a doctor assigned. Assigning random doctor.")

                    print(f"{self.user_data.user}'s is the USER who has requested a booking.")

                    data_dict = self.user_data.to_dict()

                    ClientCommands.set_appointment(
                        self.client,
                        self.user_data.user[0],
                        appt_cdms['create apt'],
                        data_dict
                    )

                    page_packet = [self.user_data.day, self.user_data.time, self.user_data.symptoms,
                                   self.user_data.images, None]

            else:
                self.create_service_message(f"{self.ai_states['confused']}")

        if self.current_state == 'images' and not self.upload_frame:
            self.create_service_message(f"{self.ai_states[self.current_state]}")
            self.upload_frame = UploadFrame(self.left_frame)
            self.upload_frame.cancel.configure(command=self.ignore_upload)
            self.upload_frame.pack(side='top', pady=5, anchor=W)
            self.create_spacer(self.right_frame, 'e')
