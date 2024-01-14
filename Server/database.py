import sqlite3
import logging
import random
import hashlib

tables = {
    "CLINICIAN": '''

                Clinician_ID    integer,
                Title           text,
                First_Name      text,
                Last_Name       text,
                Email           text,
                Postcode        text,
                Tel_no          integer,
                DOB             text,
                Password        text,
                Capacity        integer,
                Max             integer,


                primary key (Clinician_ID)

        ''',
    "PATIENT": '''

                    Patient_ID      integer,
                    Clinician_ID    integer,
                    Title           text,
                    First_Name      text,
                    Last_Name       text,
                    Address         text,
                    Postcode        text,
                    Email           text,
                    Tel_no          integer,
                    DOB             text,
                    Password        text,

                    primary key (Patient_ID)
                    foreign key (Clinician_ID) references CLINICIAN (Clinician_ID)

        ''',
    "MEDICATIONS": '''

              Item_ID           integer,
              Booking_ID        integer,
              Patient_ID        integer,
              Name              text,
              

              primary key (Item_ID)
              foreign key (Booking_ID) references BOOKINGS (Booking_ID)
              foreign key (Patient_ID) references PATIENT (Patient_ID)

        ''',
    "BOOKINGS": '''

              Booking_ID        integer,
              Patient_ID        integer,
              Clinician_ID      integer,
              Date              text,
              Time              text,
              Status            text,
              

              primary key (Booking_ID)
              foreign key (Patient_ID) references PATIENT (Patient_ID)
              foreign key (Clinician_ID) references CLINICIAN (Clinician_ID)

        ''',
    "PRESCRIPTIONS": '''

              Prescription_ID   integer,
              Patient_ID        integer,
              Clinician_ID      integer,
              Item_ID           integer,
              
              primary key (Prescription_ID)
              foreign key (Patient_ID) references PATIENT (Patient_ID)
              foreign key (Clinician_ID) references CLINICIAN (Clinician_ID)
              foreign key (Item_ID) references MEDICATIONS (Item_ID)
        '''}


# CLASSES
class Database:  # Created a class for Database along with necessary attributes
    USER_ROLE_CLINICIAN = 'CLINICIAN'
    USER_ROLE_PATIENT = 'PATIENT'

    def __init__(self, data):
        self.conn = sqlite3.connect(data, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.sql = ''
        self.login_list = []
        self.query_data = []

    def query(self, query, data):  # Method to execute queries handling with and without data
        try:
            if data:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)

        except sqlite3.Error as err:
            logging.error(f"SQLite error: {err}")

        finally:
            self.conn.commit()

    def find_doctor(self, user_data):
        self.sql = '''SELECT Clinician_ID, First_Name, Last_Name from ClINICIAN where Clinician_ID=?'''
        self.query(self.sql, user_data)

        result = self.cursor.fetchone()
        if result:
            return result
        return False

    def find_patient(self, user_data):
        self.sql = '''SELECT Patient_ID, First_Name, Last_Name from PATIENT where Patient_ID=?'''
        self.query(self.sql, user_data)

        result = self.cursor.fetchone()
        if result:
            return result
        return False

    def request_doctors(self):
        print('>: Database is searching for available doctors')
        self.sql = '''Select Clinician_ID, First_Name, Last_Name from CLINICIAN'''
        self.query(self.sql, None)
        results = self.cursor.fetchall()

        if len(results) > 0:
            print(results)
            return results
        else:
            print('No doctors currently available in database.')
            return None

    @staticmethod
    def generate_id():
        """
           Generate a unique user ID.

           Returns:
               int: Unique user ID.
        """
        return random.randint(10000, 99999)

    @staticmethod
    def handle_password(password):
        """
        Hash a given password and return the hash.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        hash_alg = hashlib.new("SHA256")
        hash_alg.update(password.encode())

        return hash_alg.hexdigest()

    def register_user(self, data, user):
        print(data)
        """
        Register a user in the database.

        Args:
            data (list): List of user data.
            user (str): User role (e.g., 'CLINICIAN' or 'PATIENT').

        Returns:
            bool: True if registration is successful, False otherwise.
        """
        self.sql = ""
        self.query_data = []

        unique_id = self.generate_id()

        title = data['title']
        first_name = data['first_name']
        last_name = data['last_name']
        email_address = data['email']
        tel_no = data['tel_no']
        postcode = data['postcode']

        print(f"{data['password']} belongs to {title}:{first_name}{last_name}")
        password = self.handle_password(data['password'])

        if title == 'DR':
            self.sql = '''INSERT INTO CLINICIAN(Clinician_ID, Title, First_Name, Last_Name, Tel_no, Postcode, 
                            Email, Password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

            self.query_data.extend(
                [unique_id, title, first_name, last_name, tel_no, postcode, email_address, password])
            logging.debug(self.query_data)

        else:
            self.sql = '''INSERT INTO PATIENT(Patient_ID, Title, First_Name, Last_Name,
                            Postcode, Email, Tel_no, Password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
            self.query_data.extend(
                [unique_id, title, first_name, last_name, postcode, email_address, tel_no, password])

        self.query(self.sql, self.query_data)
        logging.info(
            f">: {user}: {title} {first_name} {last_name} has been registered to the database successfully.")
        return True

    def get_bookings(self):
        self.sql = '''SELECT * FROM BOOKINGS'''
        self.query(self.sql, None)

        result = self.cursor.fetchall()
        if result:
            print(result)
            return result

    def create_booking(self, data):
        self.sql = '''INSERT INTO BOOKINGS (Booking_ID, Patient_ID, Clinician_ID, Date, Time, Status)
        VALUES (?, ?, ?, ?, ?, ?);'''

        self.query_data = []

        booking_id = self.generate_id()
        patient_id = data['patient'][1][0]
        doctor_id = data['doctor'][1][0]
        date = data['date']
        time = data['time']
        status = 'Pending'

        packet = (booking_id, patient_id, doctor_id, date, time, status)
        print(f">: Database is storing booking info: {packet}")

        self.query_data.extend(packet)
        self.query(self.sql, self.query_data)
        print(f">: Booking information successfully registered to database.")

        return True

    def check_records(self, data):
        self.sql = " "
        print(f'Database received: {data}')
        patient_sql = '''SELECT Patient_ID, First_Name, Last_Name FROM PATIENT WHERE EMAIL=? AND Password=?'''
        doctor_sql = '''SELECT Patient_ID, First_Name, Last_Name FROM CLINICIAN WHERE EMAIL=? AND Password=?'''

        if data['CLIENT']:
            if isinstance(data['CLIENT'], int):
                self.sql = '''Select First_Name, Last_Name from CLINICIAN where Clinician_ID=?'''
                self.cursor.execute(self.sql, (data['CLIENT'],))

                if self.cursor.fetchone():
                    logging.info(f"USER {data['CLIENT']}, Name: {self.cursor.fetchone()}")
                    return self.cursor.fetchone()
                else:
                    self.sql = '''Select First_Name, Last_name from PATIENT where Patient_ID=?'''
                    self.cursor.execute(self.sql, (data['CLIENT'],))
                    logging.info(f"USER {data['CLIENT']}, Name: {self.cursor.fetchone()}")
                    return self.cursor.fetchone()

        if data['CLIENT'] is None:  # This will return a number that will be used to identify the type of user.
            email, password = data["DATA"][0], data["DATA"][1]
            logging.debug(f"Checking login for {email}")

            for role in [self.USER_ROLE_CLINICIAN, self.USER_ROLE_PATIENT]:
                self.sql = f'''SELECT Email, Password FROM {role} WHERE Email=? AND Password=?'''
                self.cursor.execute(self.sql, [email, password])

                if self.cursor.fetchone():
                    logging.info(f"User is a {role}")

                    if role == self.USER_ROLE_PATIENT:
                        self.sql = patient_sql

                    else:
                        self.sql = doctor_sql

                    self.cursor.execute(self.sql, [email, password])
                    return [1 if role == self.USER_ROLE_PATIENT else 2, self.cursor.fetchone()]

            logging.debug('User is not a CLINICIAN or PATIENT')
            return [-1, None]

            # if not self.cursor.fetchone():
            #     print(">: Login credentials do not exist.")
            #     return False
            # else:
            #     print(">: Login credentials accepted.")
            #     return True

    def create_tables(self, table_names):
        for table, attributes in table_names.items():
            query = f'CREATE TABLE IF NOT EXISTS {table} ({attributes})'
            self.query(query, None)

    def show_all(self, column):  # This method is for displaying all the information via a query in a specific column
        self.sql = f'select * from {column}'
        self.cursor.execute(self.sql)

        return self.cursor.fetchall()
