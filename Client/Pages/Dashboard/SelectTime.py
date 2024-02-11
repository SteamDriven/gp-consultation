from tkinter import *
from customtkinter import *
from Client.Widgets import Selector
from Client.helper import ClientCommands


class SelectTime(CTkFrame):
    def __init__(self, parent, controller, booking, patientName, client):
        CTkFrame.__init__(self, parent)

        self.configure(fg_color='white')

        # Widgets
        self.title = None
        self.client = client
        self.selection = None
        self.info = None
        self.confirm_bt = None

        self.options = {}

        # Configs
        self.times = {

            'Morning': ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM"],
            'Early Afternoon': ["12:00 PM", "13:00 PM", "14:00 PM", "15:00 PM"],
            'Late Afternoon': ["16:00 PM", "17:00 PM", "18:00 PM", "19:00 PM"],
            'Evening': ["19:30 PM", "20:00 PM", "20:30", "21:00 PM"],
            'Buffer': ['0:10', '0:15', '0:20', '0:25', '0:30']
        }

        self.selections = {
            1: ['Select Start Time:', 'Select the starting time for the appointment.'],
            2: ['Select Finish Time:', 'Select the finishing time for the appointment.'],
            3: ['Buffer Time Before:', 'Set the extra time for potential concerns for additional info at the end.'],
            4: ['Buffer Time After:', 'Set the extra time for potential concerns for additional info at the end.'],
        }

        self.booking = booking
        self.patientName = ' '.join(patientName[1:]).title()
        self.patient_id = patientName[0]
        self.timeOfDay = self.booking[4]

        self.start_time = None
        self.finish_time = None
        self.buffer_before = None
        self.buffer_after = None

        self.create_labels()
        self.setup_page()

    # def calculate_time(self):
    #     self.start_time = self.options[0].get_time()
    #     self.finish_time = self.options[1].get_time()
    #     self.buffer_before = self.options[2].get_time()
    #     self.buffer_after = self.options[3].get_time()
    #
    #     start = ClientCommands.convert_to_minutes(self.start_time)
    #     finish = ClientCommands.convert_to_minutes(self.finish_time)
    #     buffer_b = ClientCommands.convert_to_minutes(self.buffer_before)
    #     buffer_a = ClientCommands.convert_to_minutes(self.buffer_after)
    #
    #     total_time = finish - start + buffer_b + buffer_a
    #     total_hours, total_minutes = divmod(total_time, 60)
    #
    #     total_time_str = f"{int(total_hours)} hr {int(total_minutes)} mins"
    #     total_time_hours_str = f"{total_hours:.2f} hours"
    #
    #     return total_time_str

    # def update_booking(self):
    #     allocated_time = self.calculate_time()
    #     print(f"Doctor has chosen allocated time of: {allocated_time} for consultation.")
    #     start_time = self.options[0].get_time()
    #
    #     message = (f"Your booking has been accepted. The time allotted for your "
    #                f"consultation will be at {self.start_time} for {allocated_time}.\n"
    #                f"The method of consultation will be via online chat.")
    #
    #     packet = ['Time', allocated_time, self.patient_id, ['Status', 'Accepted']]
    #     packet_2 = [self.patient_id, message, ClientCommands.format_time(), 'Accepted', 'doctor']
    #
    #     ClientCommands.update_booking(self.client, packet)
    #     ClientCommands.send_patient_notification(self.client, packet_2)

    def create_labels(self):
        self.title = CTkLabel(self, text='Choose a specified time', text_color='Black',
                              font=('Arial Bold', 30))
        self.info = CTkLabel(self, text=f'Patient: {self.patientName} | Time of Day: {self.timeOfDay}',
                             text_color='Black', font=('Arial light', 25))

        counter = 0
        for key, value in self.selections.items():
            if counter >= 2:
                selection = Selector(self, value[0], value[1], self.times['Buffer'])
            elif counter == 1:
                selection = Selector(self, value[0], value[1], self.times[self.timeOfDay][1:])
            else:
                selection = Selector(self, value[0], value[1], self.times[self.timeOfDay])

            self.options[counter] = selection
            counter += 1

        self.confirm_bt = CTkButton(self, fg_color='#b1c9eb', text='Accept Booking', text_color='white',
                                    font=('Arial Bold', 22), command=lambda: self.update_booking(), corner_radius=3)

    def setup_page(self):
        self.title.pack(pady=(80, 5), padx=30, anchor=W)
        self.info.pack(padx=30, anchor=W)

        for key, value in self.options.items():
            if key == 0:
                value.pack(side='top', pady=(50, 0), padx=10, anchor=W, fill='x')
            else:
                value.pack(pady=10, padx=10, anchor=W, fill='x')

        self.confirm_bt.pack(pady=30, padx=10, anchor=E, ipadx=3, ipady=2)

        # for i, frame in enumerate(self.options):
        #     if i == 0:
        #         frame.pack(side='top', pady=50, padx=10, anchor=W, fill='x')
        #
        #     frame.pack(pady=10, padx=20, anchor=W, fill='x')
