from PIL import Image
from customtkinter import *
from os.path import *

from Client.Pages.Chat.Pages.Start_Chat import startChat
from Client.Pages.Chat.Pages.Chat import Chat, aiChat
from Client.Widgets import ImageButton, SearchBar
from Client.helper import ClientCommands


class ChatOverview(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)

        self.configure(fg_color='white')

        self.tabs = None
        self.top_bar = None
        self.controller = controller
        self.client = controller.client
        self.container = None
        self.chat_window = None
        self.left_frame = None
        self.right_frame = None
        self.dash_btn = None
        self.search_bar = None
        self.username = None
        self.filter_frame = None
        self.chats_frame = None
        self.add_btn = None
        self.chat_title = None

        self.pages = {}
        self.pages_list = {

            'create': startChat,
        }

        self.buttons = {
            'Appointments': {
                "path": f'{join(dirname(__file__), "../../Images/Appointments.png")}',
                "size": (66, 70),
                "command": None
            },
            'Profile': {
                "path": f'{join(dirname(__file__), "../../Images/Profile.PNG")}',
                "size": (65, 67),
                "command": None
            },
            'Patients': {
                "path": f'{join(dirname(__file__), "../../Images/Patient.PNG")}',
                "size": (69, 66),
                "command": None
            },
            'Notifications': {
                "path": f'{join(dirname(__file__), "../../Images/Notifications.PNG")}',
                "size": (68, 68),
                "command": lambda: None
            },
            'Chat': {
                "path": f'{join(dirname(__file__), "../../Images/Chat2.PNG")}',
                "size": (60, 66),
                "command": lambda: None
            },
        }

        self.create()
        self.setup()
        self.configure_menu()
        self.create_pages()

        ClientCommands.add_page(frame=Chat, values=[self.right_frame, self.client], my_dict=self.pages, cont='chat room')
        ClientCommands.show_frame('chat room', self.pages)

    def start(self):
        print('Starting message listener.')
        self.pages['chat room'].start_message_listener()

    def create_pages(self):
        for page, data in self.pages_list.items():
            self.pages[page] = data(self.right_frame)

    def configure_menu(self):
        self.tabs.grid_columnconfigure(0, weight=0)
        self.tabs.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)

        for label, info in self.buttons.items():
            button = ImageButton(

                self.tabs,
                description=None,
                path=info['path'],
                size=info['size'],
                command=info['command']
            )

            button.logo.configure(width=80)
            button.pack(pady=10)

    def create(self):
        self.tabs = CTkFrame(self, fg_color='#3c5691', corner_radius=0, width=80)
        self.container = CTkFrame(self, fg_color='white', corner_radius=0)
        self.top_bar = CTkFrame(self.container, fg_color='white', corner_radius=7, height=80, border_color='#e7e5e5',
                                border_width=3)
        self.search_bar = SearchBar(self.top_bar)
        self.username = CTkLabel(self.top_bar, text='Dr John Doe', fg_color='white', text_color='#cecaca',
                                 font=('Arial bold', 25))

        path = join(dirname(__file__), "../../Images/Logo.png")
        path2 = join(dirname(__file__), "../../Images/Add.png")
        image = CTkImage(Image.open(path), size=(76, 70))
        image2 = CTkImage(Image.open(path2), size=(55, 55))
        self.dash_btn = CTkButton(self.tabs, fg_color='#2a3e6a', image=image, text='', width=80, corner_radius=0)

        self.chat_window = CTkFrame(self.container, fg_color='white', corner_radius=0)
        self.left_frame = CTkFrame(self.chat_window, fg_color='white', corner_radius=0)
        self.right_frame = CTkFrame(self.chat_window, fg_color='white', corner_radius=0)

        self.filter_frame = CTkFrame(self.left_frame, fg_color='white', border_color='#e7e5e5', border_width=3,
                                     height=60)
        self.chats_frame = CTkScrollableFrame(self.left_frame, fg_color='white', corner_radius=0)
        self.add_btn = CTkButton(self.filter_frame, text='', image=image2, fg_color='white', height=5, width=5)

    def setup(self):
        self.tabs.pack(side='left', fill='y', anchor=W)
        self.container.pack(side='left', fill='both', expand=True)
        self.top_bar.pack(side='top', fill='x')
        self.search_bar.pack(side='left', anchor=W, padx=10, pady=10)
        self.username.pack(side='right', anchor=E, padx=10, pady=10)
        self.dash_btn.pack(side='top', pady=(0, 20))
        self.chat_window.pack(side='top', fill='both', expand=True)
        self.left_frame.pack(side='left', fill='both', expand=True)
        self.right_frame.pack(side='left', fill='both', expand=True, ipadx=300)

        self.filter_frame.pack(side='top', fill='x')
        self.chats_frame.pack(fill='both', expand=True)
        self.add_btn.pack(side='right', anchor=E, padx=5, pady=5)