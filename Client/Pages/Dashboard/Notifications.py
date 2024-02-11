import json
import logging
import threading

from customtkinter import *
from configs import *

from Client.Widgets import Notification_Box
from Client.Pages.Dashboard.AcceptAppointment import *
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

        if notifications is not None:
            for notification in notifications:
                print(notification[0])

                if self.notifications.get(notification[0]) is None:
                    print(f"{notification[0]} doesn't exist. Creating it now!")
                    self.create_notification(notification)

                continue
        else:
            print("No notifications. Try again later.")

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
                                        delete=self.clear_notification, change=self.change_page)

        notification.pack(side='top', padx=20, pady=10, anchor=W, fill='x')

        self.notifications[identifier] = notification
        logging.info(f'Notification: {notification.identifier} has been added.')

    def change_page(self, patient_id, data):
        patient_name = self.client.handle_server_messages(Commands.packet_commands['find p'], None, patient_id)
        booking = self.client.handle_server_messages(Commands.packet_commands['find b'], None, patient_id)

        print(patient_name, booking)

        frame = AcceptAppointment(self.controller.main_frame, self.controller, booking, patient_name, self.client, data)

        for f in self.controller.frames.values():
            f.pack_forget()

        print('Cleared pages, displaying time selection.')

        frame.pack(side="top", fill="both", expand=True)
        frame.tkraise()

    def clear_notification(self, key):
        del self.notifications[key]
        logging.info(f'Notification: {key} has been removed.')
