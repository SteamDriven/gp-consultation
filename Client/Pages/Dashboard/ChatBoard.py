from customtkinter import *
from configs import *


class ChatBoard(CTkFrame):
    def __init__(self, parent, controller, user_data, client):
        super().__init__(parent, controller, user_data, client)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.client = client
        self.user_data = user_data
        self.frames = {}
        self.pages_list = {}

        self.configure(fg_color='white')
        self.title = None

        self.top_bar = None
        self.side_bar = None
        self.container = None
        self.chat_frame = None
        self.window = None

        self.create()
        self.setup()

    def create(self):
        self.side_bar = CTkFrame(self, fg_color='#c1ff72', corner_radius=0)
        self.top_bar = CTkFrame(self, fg_color='#8c52ff', corner_radius=0)
        self.container = CTkFrame(self, fg_color='white', corner_radius=0)
        self.chat_frame = CTkFrame(self.container, fg_color='#78d1cc', corner_radius=0)
        self.window = CTkFrame(self.container, fg_color='#ed451d', corner_radius=0)

    def update_chats(self):
        pass

    def setup(self):
        self.side_bar.pack(side='left', fill='y', expand=True)
        self.top_bar.pack(side='top', fill='x', expand=True)
        self.container.pack(side='top', fill='both', expand=True)
        self.chat_frame.pack(side='left', fill='both', expand=True)
        self.window.pack(fill='both', expand=True, ipadx=20)
