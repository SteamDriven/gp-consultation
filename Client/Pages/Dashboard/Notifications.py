from customtkinter import *


class Notifications(CTkFrame):
    def __init__(self, parent, controller, user_data):
        CTkFrame.__init__(self, parent)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.configure(fg_color='white')
        self.title = None

        self.create()
        self.place()

    def create(self):
        self.title = CTkLabel(self, text='Your notifications', text_color='Black',
                              font=('Arial Bold', 30))

    def place(self):
        self.title.pack(pady=(80, 5), padx=30, anchor=W)

    def create_notification(self, message):
        pass

    def place_notification(self):
        pass

    def clear_notification(self, note):
        pass
