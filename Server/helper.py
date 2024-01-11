import logging
import random
import string

from configs import Commands


class ServerCommands:
    @staticmethod
    def get_referral(client):
        return client.handle_server_messages(Commands.REFERRAL, None, None)

    @staticmethod
    def validate_register(user_type, data, client):
        return client.handle_server_messages(Commands.VALIDATE_REGISTER, user_type, data)

    @staticmethod
    def generate_code(size):
        """
            Generate an alphanumeric code of a given size.

            Args:
                size (int): Size of the code.

            Returns:
                str: Generated code.
        """
        length = size
        chars = (string.ascii_uppercase + string.digits)
        code = [random.choice(chars) for c in range(length)]

        return ''.join(code)

    @staticmethod
    def register_user(data, user, db):
        """
               Register a user in the database.

               Args:
                   data (list): List of user data.
                   user (str): User role (e.g., 'CLINICIAN' or 'PATIENT').
                   db (database): Database

               Returns:
                   bool: True if registration is successful, False otherwise.
               """
        return db.register_user(data, user)

    @staticmethod
    def compare_login(data, db):
        """
            Compare the given password's hash with the one stored in the database.

            Args:
                data (dict): User login data.
                db (database): Database

            Returns:
                tuple: Tuple containing user role code and hashed password.
        """
        password = data['DATA'][1]
        logging.debug(password)

        password_hash = db.handle_password(password)
        data['DATA'][1] = password_hash

        return db.check_records(data)

    @staticmethod
    def find_user(clients, client):
        for key, socket in clients.items():

            if client == socket:
                return key
