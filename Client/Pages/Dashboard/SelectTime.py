from tkinter import *
from customtkinter import *
from Client.Widgets import Selector


class SelectTime(CTkFrame):
    def __init__(self, parent, controller, timeOfDay, patientName):
        CTkFrame.__init__(parent, controller)

        self.configure(fg_color='white')

        # Widgets
        self.title = None
        self.selection = None
        self.info = None

        self.options = []

        # Configs
        self.times = {

            'Morning': ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM"],
            'Early Afternoon': ["12:00 PM", "13:00 PM", "14:00 PM", "15:00 PM"],
            'Late Afternoon': ["16:00 PM", "17:00 PM", "18:00 PM", "19:00 PM"],
            'Evening': ["19:30 PM", "20:00 PM", "20:30", "21:00 PM"]
        }

        self.selections = {
            1: ['Select Start Time:', 'Select the starting time for the appointment.'],
            2: ['Select Finish Time:', 'Select the finishing time for the appointment.'],
            3: ['Buffer Time Before:', 'Set the extra time for potential concerns for additional info at the end.'],
            4: ['Buffer Time After:', 'Set the extra time for potential concerns for additional info at the end.'],
        }

        self.timeOfDay = timeOfDay
        self.patientName = patientName

    def create_labels(self):
        self.title = CTkLabel(self, text='Select a specified time', text_color='Black',
                              font=('Arial Bold', 30))
        self.info = CTkLabel(self, text=f'{self.patientName} | Time of Day: {self.timeOfDay}', text_color='Black',
                             font=('Arial light', 15))

        for key, value in self.selections.items():
            selection = Selector(self, value[0], value[1])
            self.options.append(selection)

    def setup_page(self):
        self.title.pack(pady=(80, 5), padx=30, anchor=W)
        self.info.pack(padx=30, anchor=W)

        for i, frame in self.options:
            if i == 0:
                frame.pack(side='top', pady=30, padx=10, anchor=W)

            frame.pack(pady=10, padx=10, anchor=W)
