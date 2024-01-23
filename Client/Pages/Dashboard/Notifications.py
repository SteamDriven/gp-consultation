import json
import logging
import threading

from customtkinter import *
from configs import *

from Client.Widgets import Notification_Box
from Client.Pages.Dashboard.SelectTime import *
from Client.helper import *


class Notifications(CTkFrame):
    def __init__(self, parent, controller, user_data):
        CTkFrame.__init__(self, parent)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.configure(fg_color='white')
        self.title = None
        self.client = controller.client
        self.controller = controller
        self.notifications = {}
        self.container = None

        self.create()
        self.place()

    def update_notifications(self):
        notifications = ClientCommands.update_notes(Commands.packet_commands['notifications']['search'], self.client)

        if notifications:
            print(f'You have {len(notifications)} new notification/s from the server. Displaying them now...')

            for notification in notifications:
                if notification[0] in notifications:
                    continue
                self.create_notification(notification)

        else:
            print(f'You have 0 new notification/s from the server. Look again later.')

    def create(self):
        print('Creating notifications title')
        self.title = CTkLabel(self, text='Your notifications', text_color='Black',
                              font=('Arial Bold', 30))
        self.container = CTkScrollableFrame(self, fg_color='white')

    def place(self):
        self.title.pack(side='top', pady=(80, 5), padx=30, anchor=W)
        self.container.pack(side='top', fill='both', expand=True)

    def create_placeholders(self):
        status = 'Completed'
        title = 'Booking accepted: Dr John Doe'
        message = [title, "Your booking with Dr John Doe on Mon 13 Dec, 2024 has been accepted. Your\n"
                          "appointment is scheduled for a chat at 8:45 AM."]
        placeholder = Notification_Box(self.container, message, 'doctor', status, '15 Jan 2024 at 8:30 PM',
                                       self.clear_notification)
        placeholder.pack(side='top', padx=20, pady=10, anchor=W)
        self.notifications[placeholder.identifier] = placeholder

    def create_notification(self, message):
        identifier = message[0]
        text = json.loads(message[2])
        status = message[4]
        header = message[5]
        timestamp = message[3]

        notification = Notification_Box(self.container, text, header, status, timestamp,
                                        self.clear_notification)
        notification.pack(side='top', padx=20, pady=10, anchor=W)
        self.notifications[identifier] = notification
        logging.info(f'Notification: {notification.identifier} has been added.')

    def change_page(self, patient_id):
        patient_name = self.client.handle_server_messages(Commands.packet_commands['find p'], None, patient_id)
        time_of_day = self.client.handle_server_messages(Commands.packet_commands['find b'], None, patient_id)

        frame = SelectTime(self.controller.main_frame, self.controller, time_of_day, patient_name)

        for f in self.controller.frames.values():
            f.pack_forget()

        frame.pack(side="top", fill="both", expand=True)
        frame.tkraise()

    def clear_notification(self, key):
        del self.notifications[key]
        logging.info(f'Notification: {key} has been removed.')
