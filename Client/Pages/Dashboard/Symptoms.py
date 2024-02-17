from customtkinter import *
from Client.Pages.Chat.Pages.Chat import aiChat
from Client.Pages.Dashboard.AppointmentDetails import *


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

    def change_to_confirmation_page(self, info):
        self.cancel_button.pack_forget()
        date, time, symptoms, images, doctor = info[0], info[1], info[2], info[3], info[4]

        values = (self.controller.main_frame, self.controller, date, time, symptoms, images, doctor)
        ClientCommands.add_page(AppointmentDetails, values, self.controller.frames, 'apt details')
        ClientCommands.show_frame('apt details', self.controller.frames)

    def create(self):
        self.title = CTkLabel(self, text='Discuss your symptoms', text_color='Black',
                              font=('Arial Bold', 30))
        # self.ai_chat = aiChat(self, user_data=self.user_data, client=self.client
        #                     callback=self.change_to_confirmation_page)
        print('starting up ai chat')
        self.ai_chat = aiChat(master=self, client=self.client, user_data=self.user_data,
                              callback=self.change_to_confirmation_page)
        print('Ai Chat has been created.')
        self.cancel_button = CTkButton(self, text='Cancel Request', text_color='white', font=('Arial Bold', 20),
                                       fg_color='#b1c9eb', corner_radius=5)

    def place(self):
        self.title.pack(pady=(80, 5), padx=30, anchor=W)
        self.ai_chat.pack(fill='both', expand=True, padx=30, pady=(20, 0))
        self.cancel_button.pack(side='right', padx=30, pady=(20, 120), ipadx=30, ipady=5)
