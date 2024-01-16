import json
import logging
import threading

from customtkinter import *
from configs import *

from Client.Widgets import Notification_Box
from Client.helper import *


class Notifications(CTkFrame):
    def __init__(self, parent, controller, user_data):
        CTkFrame.__init__(self, parent)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.configure(fg_color='white')
        self.title = None
        self.client = controller.client
        self.notifications = {}
        self.container = None

        self.create()
        self.place()
        # self.create_placeholders()

    def update_notifications(self):
        notifications = ClientCommands.update_notes(Commands.packet_commands['notifications']['search'], self.client)

        if notifications:
            print(f'You have {len(notifications)} new notification/s from the server. Displaying them now...')

            for notification in notifications:
                print(notification)
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
        text = json.loads(message[1])
        status = message[3]
        header = message[4]
        timestamp = message[2]

        notification = Notification_Box(self.container, text, header, status, timestamp,
                                        self.clear_notification)
        notification.pack(side='top', padx=20, pady=10, anchor=W)
        self.notifications[notification.identifier] = notification
        logging.info(f'Notification: {notification.identifier} has been added.')

    def clear_notification(self, key):
        del self.notifications[key]
        logging.info(f'Notification: {key} has been removed.')

    # def listen_for_notifications(self):
    #     logging.info(f"Listening for notifications.")
    #     while True:
    #         messages = self.client.receive_message()
    #         logging.info(f"Received message: {messages}")
    #
    #         if messages['COMMAND'] == Commands.packet_commands['notifications']['send patient']:
    #             self.create_notification(messages['DATA'])
    #         if messages['COMMAND'] == Commands.packet_commands['notifications']['send doctor']:
    #             self.create_notification(messages['DATA'])
    #
    # def start_listening(self):
    #     logging.info(f"Creating message listener.")
    #     threading.Thread(target=self.listen_for_notifications).start()
