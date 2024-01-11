from customtkinter import *
from Client.Widgets import Chat


class ChatRoom(CTkFrame):
    def __init__(self, parent, controller, user_data):
        CTkFrame.__init__(self, parent)

        self.configure(fg_color='white')
        self.title = None
        self.user_data = user_data
        self.controller = controller
        self.room = None

    def create(self):
        self.title = CTkLabel(self, text='Your chat room', text_color='Black',
                              font=('Arial Bold', 30))
        self.room = Chat(self, 'Chat', client=self.controller.client, user_data=self.user_data, state='client')

    def place(self):
        self.title.pack(pady=(80, 5), padx=30, anchor=W)
        self.room.pack(fill='both', expand=True, padx=30, pady=20)
        self.room.start_message_listener()
