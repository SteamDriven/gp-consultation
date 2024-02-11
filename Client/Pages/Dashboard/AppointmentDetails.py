from tkinter import *
from customtkinter import *
from os.path import *
from textwrap import *
from Client.helper import ClientCommands

from PIL import Image as PILImage


class AppointmentDetails(CTkFrame):

    def __init__(self, parent, controller, apt_date="N/a", apt_time="N/a", symptoms="N/a", images=None, doctor=None):
        CTkFrame.__init__(self, parent)

        self.configure(fg_color='white')

        self.controller = controller
        self.date = apt_date
        self.time = apt_time
        self.symptoms = symptoms
        self.images = images
        self.doctor = doctor

        self.title = None
        self.container = None
        self.left_frame = None
        self.right_frame = None
        self.exit_button = None

        self.doctor_profile = join(dirname(__file__), "../../Images/Profiles/5.png")
        self.checkmark = join(dirname(__file__), "../../Images/check.png")
        self.checkmark_img = None
        self.profile_img = None

        self.booking_title = None
        self.title_frame = None
        self.doctor_frame = None
        self.doctor_frame_right = None
        self.summary = None
        self.doctor_label = None
        self.doctor_info = None
        self.clinician_info = None
        self.estimate_label = None

        doctor_text = {
            1: f'Dr {self.doctor} will review your request shortly.',
            2: f'A doctor will be assigned to you ready to you review your request shortly.'
        }

        if self.doctor is not None:
            self.selected_doctor_text = doctor_text[1]
        else:
            self.selected_doctor_text = doctor_text[2]

        self.summary_labels = {

            'Date:': self.date,
            'Time:': self.time,
            'Symptoms:': ClientCommands.format_paragraph(self.symptoms, 70),
        }

        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        self.title = CTkLabel(self, text='Appointment Details', font=('Arial Bold', 30), justify='left',
                              fg_color='white', text_color='#0f0e0c')
        self.container = CTkFrame(self, fg_color='#f2f2f2', corner_radius=0)
        self.left_frame = CTkFrame(self.container, fg_color='white', corner_radius=3)
        self.right_frame = CTkFrame(self.container, fg_color='white', corner_radius=3)
        self.exit_button = CTkButton(self, fg_color='#7b96d4', text_color='white', text='Take me back',
                                     font=('Arial bold', 20), corner_radius=3)

        checkmark = CTkImage(PILImage.open(self.checkmark), size=(63, 63))
        profile = CTkImage(PILImage.open(self.doctor_profile), size=(90, 89))

        self.title_frame = CTkFrame(self.left_frame, fg_color='white')
        self.checkmark_img = CTkLabel(self.title_frame, image=checkmark, text='')
        self.booking_title = CTkLabel(self.title_frame, fg_color='white', text_color='#7ed957', font=('Arial Bold', 35),
                                      text='Booking confirmed')

        self.doctor_frame = CTkFrame(self.left_frame, fg_color='white')
        self.profile_img = CTkLabel(self.doctor_frame, image=profile, text='')
        self.doctor_frame_right = CTkFrame(self.doctor_frame, fg_color='white')
        self.doctor_label = CTkLabel(self.doctor_frame_right, text=self.selected_doctor_text,
                                     font=('Arial bold', 25), text_color='#393939', justify='left')
        self.doctor_info = CTkLabel(self.doctor_frame_right, text='In the meantime, feel free to look around.',
                                    font=('Arial light', 22), text_color='#393939', justify='left')

        self.clinician_info = CTkLabel(self.left_frame, text='Clinician should review between', text_color='#737373',
                                       font=('Arial bold', 22), justify='left')
        self.estimate_label = CTkLabel(self.left_frame, text='1-2 business days', text_color='#393939',
                                       font=('Arial bold', 20), justify='left')

        self.summary = CTkLabel(self.right_frame, text='Booking summary', justify='left', text_color='#393939',
                                font=('Arial bold', 25))

    def setup_widgets(self):
        self.title.pack(pady=(80, 5), padx=30, anchor=W)
        self.container.pack(pady=5, side='top', fill='x', expand=True, ipady=60)
        self.left_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True, ipadx=100, anchor=W)
        self.right_frame.pack(padx=10, pady=10, fill='both', expand=True, anchor=E)

        self.title_frame.pack(side='top', padx=10, pady=20, anchor=W)
        self.checkmark_img.pack(side='left', padx=10, pady=10)
        self.booking_title.pack(padx=10, pady=15)

        self.doctor_frame.pack(side='top', padx=10, pady=25, anchor=W)
        self.profile_img.pack(side='left', padx=10, pady=20, anchor=CENTER)
        self.doctor_frame_right.pack(padx=5, pady=20, anchor=CENTER)
        self.doctor_label.pack(side='top', pady=(22, 2), anchor=W)
        self.doctor_info.pack(side='top', anchor=W)

        self.clinician_info.pack(side='top', padx=20, pady=(40, 2), anchor=W)
        self.estimate_label.pack(side='top', padx=20, anchor=W)

        self.summary.pack(side='top', padx=10, pady=20, anchor=W)

        for label, info in self.summary_labels.items():
            frame = CTkFrame(self.right_frame, fg_color='white')
            label1 = CTkLabel(frame, fg_color='white', text=label, text_color='#393939', font=('Arial bold', 20),
                              justify='left')

            label2 = CTkLabel(frame, fg_color='white', text=info, text_color='#737373', font=('Arial light', 20),
                              justify='right')

            if label == 'Symptoms':
                label2.configure(justify='left')

            label1.pack(side='left', padx=10, pady=10)
            label2.pack(side='right', padx=10, pady=10)

            if label == 'Date':
                frame.pack(padx=10, pady=20, fill='x', expand=True)
            if label == 'Time':
                frame.pack(padx=10, pady=10, fill='x', expand=True)

            if label == 'Symptoms':
                frame.pack(padx=10, pady=20, fill='x', expand=True)
            frame.pack(padx=10, pady=10, fill='x', expand=True)

        self.exit_button.pack(side='bottom', padx=30, pady=(0, 80), anchor=E, ipadx=10)
