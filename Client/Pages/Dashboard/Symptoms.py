from customtkinter import *
from Client.Widgets import Chat


class Symptoms(CTkFrame):
    def __init__(self, parent, controller, user_data):
        CTkFrame.__init__(self, parent)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.controller = controller
        self.client = self.controller.client
        self.configure(fg_color='white')
        self.user_data = user_data

        self.title = None
        self.ai_chat = None
        self.cancel_button = None

        self.create()
        self.place()

    def create(self):
        self.title = CTkLabel(self, text='Discuss your symptoms', text_color='Black',
                              font=('Arial Bold', 30))
        self.ai_chat = Chat(self, user_data=self.user_data, client=self.client, state='ai')
        self.cancel_button = CTkButton(self, text='Cancel Request', text_color='white', font=('Arial Bold', 20),
                                       fg_color='#b1c9eb', corner_radius=5)

    def place(self):
        self.title.pack(pady=(80, 5), padx=30, anchor=W)
        self.ai_chat.pack(fill='both', expand=True, padx=30, pady=(20, 0))
        self.cancel_button.pack(side='right', padx=30, pady=(20, 120), ipadx=30, ipady=5)
