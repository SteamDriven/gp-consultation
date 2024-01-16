from customtkinter import *
from Client.Widgets import Button, Calendar


class Appointments(CTkFrame):
    def __init__(self, parent, controller, user_data):
        CTkFrame.__init__(self, parent)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.configure(fg_color='white')

        # Method calls
        self.create()
        self.place()

        # Widgets
        self.title = None

    # Methods
    def create(self):
        self.title = CTkLabel(self, text='Your appointments', text_color='Black',
                              font=('Arial Bold', 30))

    def place(self):
        self.title.pack(pady=(80, 5), padx=30, anchor=W)


class RequestAppointments(CTkFrame):

    def __init__(self, parent, controller, user_data):
        CTkFrame.__init__(self, parent)

        print(f"{self.__class__.__name__} successfully initialised.")

        self.configure(fg_color='white')
        self.available_times = ['Morning', 'Early Afternoon', 'Late Afternoon', 'Evening']
        self.selected_time = None
        self.user_data = user_data
        self.buttons = []
        self.control = controller
        self.title = None
        self.date_entry = None
        self.time_frame = None
        self.confirm = None

        self.create()
        self.place()
        self.update_selected(0)

    def create_buttons(self):
        for index, time in enumerate(self.available_times):
            print(index, time)

            button = Button(self.time_frame, time)
            button.col = index

            button.bind("<1>", lambda event, widget=button: self.select_button(event, widget))
            self.buttons.append(button)

        return self.buttons

    def select_button(self, event, widget):
        if self.selected_time:
            self.selected_time.change_state()

            widget.change_state()
            self.selected_time = widget

        print(f"Selected time has been changed to: {self.selected_time}")

    def update_selected(self, index):
        if len(self.buttons) > 0:
            self.selected_time = self.buttons[index]
            self.selected_time.change_state()

        return print(f"Selected time has been updated to: {self.selected_time}")

    def update_time(self):
        day = self.date_entry.selected_button
        day_info = [day.day, str(day.date), str(day.year)]
        time = self.selected_time.placeholder

        print(f"Day: {day_info} at {time}")
        self.user_data.day = ' '.join(day_info)
        self.user_data.time = time
        self.control.show_frame("symptoms")

    def create(self):
        self.title = CTkLabel(self, text='Request new appointment', text_color='Black',
                              font=('Arial Bold', 35))
        self.date_entry = Calendar(self)
        self.time_frame = CTkFrame(self, fg_color='white', corner_radius=0)
        self.confirm = CTkButton(self, fg_color='#b1c9eb', corner_radius=2, text='Confirm Booking',
                                 font=('Arial Bold', 25), text_color='white', hover_color='#7c99c4',
                                 command=lambda: self.update_time())

    def place(self):
        self.title.pack(pady=(80, 5), padx=30, anchor=W)
        self.date_entry.pack(pady=10, padx=30, anchor=W, ipadx=200)
        self.time_frame.pack(pady=15, padx=30, anchor=CENTER)

        buttons = self.create_buttons()
        for button in buttons:
            button.grid(row=0, column=button.col, padx=25, pady=10, sticky='nsew', ipadx=80)

        self.confirm.pack(side='bottom', pady=80, anchor=CENTER, ipadx=20, ipady=5)
