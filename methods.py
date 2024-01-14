from configs import Commands
from tkinter import messagebox
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class UserAppointmentData:
    def __init__(self):
        self._currentUser = None

    def to_dict(self):
        return {
            'user': self.user,
        }

    @classmethod
    def from_dict(cls, data_dict):
        instance = cls()

        for key, value in data_dict.items():
            setattr(instance, key, value)
        return instance

    @property
    def user(self):
        return self._currentUser

    @user.setter
    def user(self, newUser):
        self._currentUser = newUser
        logging.info(f"Appointment data > USER: {self._currentUser}")


class DoctorData(UserAppointmentData):
    def __init__(self):
        super().__init__()
        self._current_patients = []

    def to_dict(self):
        user_data_dict = super().to_dict()
        user_data_dict.update({'current_patients': self.patients})

        return user_data_dict

    @property
    def patients(self):
        return self._current_patients

    @patients.setter
    def patients(self, newPatient):
        self._current_patients.append(newPatient)
        logging.info(f"Appointment data > DOCTOR: {self._current_patients} assigned to {self.user}")


class PatientData(UserAppointmentData):
    def __init__(self):
        super().__init__()

        self._assigned_doctor = None
        self._selected_time = None
        self._selected_day = None
        self._symptoms = []
        self._images = []

    def to_dict(self):
        user_data_dict = super().to_dict()
        user_data_dict.update({

            'assigned_doctor': self.doctor,
            'selected_time': self.time,
            'selected_day': self.day,
            'symptoms': self.symptoms,
            'images': self.images,
        })

        return user_data_dict

    @property
    def doctor(self):
        return self._assigned_doctor

    @property
    def time(self):
        return self._selected_time

    @property
    def images(self):
        return self._images

    @property
    def day(self):
        return self._selected_day

    @property
    def symptoms(self):
        return self._symptoms

    @symptoms.setter
    def symptoms(self, newSymptoms):
        self._symptoms = newSymptoms
        logging.info(f"Appointment data > SYMPTOMS: {self._symptoms}")

    @time.setter
    def time(self, newTime):
        self._selected_time = newTime
        logging.info(f"Appointment data > TIME: {self._selected_time}")

    @images.setter
    def images(self, newImage):
        self._images = newImage
        logging.info(f"Appointment data > IMAGE: {self._images}")

    @day.setter
    def day(self, newDay):
        self._selected_day = newDay
        logging.info(f"Appointment data > DAY: {self._selected_day}")

    @doctor.setter
    def doctor(self, newDoctor):
        self._assigned_doctor = newDoctor
        logging.info(f"Appointment data > DOCTOR: {self._assigned_doctor} assigned to {self.user}")


class Validator:
    @staticmethod
    def validate_email(email):
        """
        Validate an email address using a regular expression.
        """
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_password(password, confirm):
        """
        Compare two passwords to ensure they match.
        """
        return password == confirm

    @staticmethod
    def validate_name(name):
        """
        Validate a name based on various criteria.
        """
        if not isinstance(name, str) or len(name) < 2 or name.isnumeric() or not re.match('^[A-Z0-9._]*$', name):
            return False
        return True

    @staticmethod
    def validate_tel_no(no):
        """
        Validate a telephone number based on its length.
        """
        return len(no) == 11

    @staticmethod
    def validate_postcode(code):
        """
        Validate a postcode based on its length.
        """
        pattern = r"^[A-Z]{1,2}([0-9]{1,2}[" "][0-9][A-Z]{2}$"
        return bool(re.match(pattern, code))

    @staticmethod
    def validate_referral(user_input, referral):
        """
        Compare the user's input with the server's generated referral code.
        """
        return user_input == referral
