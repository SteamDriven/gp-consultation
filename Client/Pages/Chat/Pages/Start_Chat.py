from PIL import Image
from customtkinter import *
from os.path import *
from Client.helper import ClientCommands


class startChat(CTkFrame):
    title_text = 'Connect, consult and support'
    desc_text = ClientCommands.format_paragraph('Connect with your patients, consult on their needs, and collaborate '
                                                'on their health journey securely in real-time.', 70)

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color='white')

        self.logo = None
        self.logo_path = join(dirname(__file__), '../../../Images/Chatlogo.png')
        self.title = None
        self.description = None
        self.new_btn = None

        self.create()
        self.setup()

    def create(self):
        self.logo = CTkLabel(self, image=CTkImage(Image.open(self.logo_path), size=(634, 344)), text='')
        self.title = CTkLabel(self, text_color='#393939', text=self.title_text, font=('Arial Bold', 23))
        self.description = CTkLabel(self, text_color='#c0c0c0', text=self.desc_text, font=('Arial light', 20), width=10)
        self.new_btn = CTkButton(self, text='Start a new chat', fg_color='#b1c9eb', font=('Arial bold', 20),
                                 corner_radius=3, text_color='white')

    def setup(self):
        self.logo.pack(side='top', anchor=CENTER, pady=(100, 0))
        self.title.pack(anchor=CENTER, pady=5)
        self.description.pack(anchor=CENTER, pady=8)
        self.new_btn.pack(anchor=CENTER, pady=15, ipadx=10, ipady=5)