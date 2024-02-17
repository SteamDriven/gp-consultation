import json
from tkinter import *
from customtkinter import *
from os.path import *

from Client.Widgets import Selector
from Client.helper import ClientCommands
from PIL import Image as PILImage


class AcceptAppointment(CTkFrame):

    def __init__(self, parent, controller, booking="N/a", patientName="N/a", client=None, data=None):
        CTkFrame.__init__(self, parent)

        self.configure(fg_color='white')
        self.left_frame = None
        self.right_frame = None
        self.title = None
        self.client = client

        self.announcement_frame = None
        self.announcement_title_frame = None
        self.announce_title = None
        self.announce_info = None

        self.reference_frame = None
        self.booked_frame = None

        self.start_time = None
        self.finish_time = None
        self.buffer_before = None
        self.buffer_after = None

        self.options = {}
        self.description = "This is to allow you to choose a precise\n time for the appointment as well as\n" \
                           "estimated buffer time before and after. "

        self.description = ClientCommands.format_paragraph(self.description, 70)

        self.times = {

            'Morning': ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM"],
            'Early Afternoon': ["12:00 PM", "13:00 PM", "14:00 PM", "15:00 PM"],
            'Late Afternoon': ["16:00 PM", "17:00 PM", "18:00 PM", "19:00 PM"],
            'Evening': ["19:30 PM", "20:00 PM", "20:30", "21:00 PM"],
            'Buffer': ['0:10', '0:15', '0:20', '0:25', '0:30']
        }

        self.selections = {

            1: ['Select Start Time:'],
            2: ['Select Finish Time:'],
            3: ['Buffer Time Before:'],
            4: ['Buffer Time After:'],
        }

        self.details = {

            'Symptoms': (join(dirname(__file__), "../../Images/symptoms.PNG"), (74, 71)),
            'Images': (join(dirname(__file__), "../../Images/images.PNG"), (74, 74)),
            'Date': (join(dirname(__file__), "../../Images/calendar.PNG"), (74, 73)),
        }

        self.symptoms = data[0]
        self.images = data[1]

        self.detail_labels = []

        self.booking = booking
        self.patient_name = ' '.join(patientName[1:]).title()
        self.patient_id = patientName[0]
        self.timeOfDay = self.booking[4]

        print(self.timeOfDay)

        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        formatted_booking = ', '.join(map(str, self.booking[3:5]))
        self.title = CTkLabel(self, text='Current appointment', font=('Arial Bold', 30), justify='left',
                              fg_color='white', text_color='#0f0e0c')

        self.left_frame = CTkFrame(self, fg_color='white')
        self.right_frame = CTkFrame(self, fg_color='white')

        self.announcement_frame = CTkFrame(self.left_frame, fg_color='#f2f2f2', corner_radius=7)
        self.announcement_title_frame = CTkFrame(self.announcement_frame, fg_color='#f2f2f2')
        self.announce_title = CTkLabel(self.announcement_title_frame, fg_color='#f2f2f2', text=f'New Appointment: '
                                                                                               f'{self.patient_name}',
                                       font=('Arial bold', 25), text_color='#393939', justify='left')
        self.announce_info = CTkLabel(self.announcement_title_frame, fg_color='#f2f2f2', text_color='#cecaca',
                                      text='You have been requested for a consultation appointment.', font=(
                'Arial bold', 20), justify='left')

        self.reference = CTkLabel(self.announcement_frame, fg_color='#f2f2f2',
                                  text=f'Booking reference: {self.booking[0]}',
                                  text_color='#393939', font=('Arial bold', 20), justify='left')
        self.booked = CTkLabel(self.announcement_frame, fg_color='#f2f2f2',
                               text=f'Booked for: {formatted_booking}', justify='left',
                               font=('Arial bold', 20), text_color='#393939')

        self.info = CTkLabel(self.left_frame, fg_color='white', text='Appointment details', text_color='#393939',
                             font=('Arial bold', 20), justify='left')

        self.accept_frame = CTkFrame(self.right_frame, fg_color='#f2f2f2', corner_radius=7)
        self.accept_title = CTkLabel(self.accept_frame, fg_color='#f2f2f2', text='Accept booking', text_color='#393939',
                                     font=('Arial Bold', 25), justify='left')

        counter = 0
        for key, value in self.selections.items():
            if counter >= 2:
                selection = Selector(self.accept_frame, value[0], self.times['Buffer'])
            elif counter == 1:
                selection = Selector(self.accept_frame, value[0], self.times[self.timeOfDay][1:])
            else:
                selection = Selector(self.accept_frame, value[0], self.times[self.timeOfDay])

            self.options[counter] = selection
            counter += 1

        self.description_text = CTkLabel(self.accept_frame, fg_color='#f2f2f2', text=self.description,
                                         text_color='#737373', font=('Arial light', 18), justify='left')

        self.accept_button = CTkButton(self.accept_frame, fg_color='#b1c9eb', text='Accept booking', text_color='white',
                                       corner_radius=3, font=('Arial bold', 22), command=lambda: self.update_booking())

        self.reject_button = CTkButton(self.right_frame, fg_color='#ff5757', text='Reject booking', text_color='white',
                                       font=('Arial bold', 20))

    def setup_widgets(self):
        self.title.pack(side='top', pady=(80, 5), padx=30, anchor=W)

        self.left_frame.pack(side='left', padx=10, pady=(20, 80), fill='both', expand=True, ipadx=40, anchor=W)
        self.right_frame.pack(padx=(0, 10), pady=(20, 80), fill='both', expand=True, anchor=E)

        # Right Frame
        self.announcement_frame.pack(side='top', padx=10, pady=10, ipadx=140, anchor=W)
        self.announcement_title_frame.pack(side='top', padx=10, pady=10, fill='x', expand=True, anchor=W)
        self.announce_title.pack(side='top', padx=10, pady=7, anchor=W)
        self.announce_info.pack(padx=10, anchor=W)
        self.reference.pack(padx=20, pady=(10, 2), anchor=W)
        self.booked.pack(padx=20, pady=(0, 10), anchor=W)

        self.info.pack(side='top', padx=20, pady=10, anchor=W)

        formatted_booking = ', '.join(map(str, self.booking[3:5]))

        for key, value in self.details.items():
            image = CTkImage(PILImage.open(value[0]), size=value[1])
            frame = CTkFrame(self.left_frame, fg_color='white')

            left_frame = CTkFrame(frame, fg_color='white')
            logo = CTkLabel(left_frame, image=image, text='')

            right_frame = CTkFrame(frame, fg_color='white')
            label = CTkLabel(right_frame, fg_color='white', text=key, text_color='#737373', font=('Arial Bold', 20),
                             justify='left')
            label2 = CTkLabel(right_frame, fg_color='white', text='Testing', text_color='#cecaca',
                              font=('Arial light', 18), justify='left')

            if key == 'Symptoms':
                label2.configure(text=ClientCommands.format_paragraph(self.symptoms, 70))

            if key == 'Date':
                label2.configure(text=f"{formatted_booking}")

            frame.pack(side='top', padx=20, pady=10, anchor=W)
            left_frame.pack(side='left', padx=5)
            logo.pack(side='top')

            right_frame.pack(pady=10)
            label.pack(padx=10, pady=(10, 2), anchor=W)
            label2.pack(padx=10, pady=(0, 10), anchor=W)

        # Left Frame
        self.accept_frame.pack(side='top', padx=10, pady=10)
        self.accept_title.pack(side='top', padx=10, pady=5, anchor=W)

        for key, value in self.options.items():
            value.pack(side='top', pady=5, padx=5, anchor=W, fill='x', expand=True)

        self.description_text.pack(padx=2, pady=10, fill='x', expand=True)

        self.accept_button.pack(padx=10, pady=10, fill='x')
        self.reject_button.pack(padx=10, pady=10, ipadx=10)

    def calculate_time(self):
        self.start_time = self.options[0].get_time()
        self.finish_time = self.options[1].get_time()
        self.buffer_before = self.options[2].get_time()
        self.buffer_after = self.options[3].get_time()

        start = ClientCommands.convert_to_minutes(self.start_time)
        finish = ClientCommands.convert_to_minutes(self.finish_time)
        buffer_b = ClientCommands.convert_to_minutes(self.buffer_before)
        buffer_a = ClientCommands.convert_to_minutes(self.buffer_after)

        total_time = finish - start + buffer_b + buffer_a
        total_hours, total_minutes = divmod(total_time, 60)

        total_time_str = f"{int(total_hours)} hr {int(total_minutes)} mins"
        total_time_hours_str = f"{total_hours:.2f} hours"

        return total_time_str

    def update_booking(self):
        allocated_time = self.calculate_time()
        print(f"Doctor has chosen allocated time of: {allocated_time} for consultation.")
        start_time = self.options[0].get_time()

        message = (f"Your booking has been accepted. The time allotted for your "
                   f"consultation will be at {self.start_time} for {allocated_time}.\n"
                   f"The method of consultation will be via online chat.")

        packet = ['Time', [start_time, allocated_time], self.patient_id, ['Status', 'Accepted']]
        packet_2 = [self.patient_id, message, ClientCommands.format_time(), 'Accepted', 'doctor']

        ClientCommands.update_booking(self.client, packet)
        ClientCommands.send_patient_notification(self.client, packet_2)
