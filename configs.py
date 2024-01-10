class Commands:
    REGISTER = 'REGISTER'
    LOGIN = 'LOGIN'
    REFERRAL = 'REFERRAL'
    VALIDATE_REGISTER = 'VALIDATE REGISTER'

    chat_commands = {

        'announcement':     'SERVER_ANNOUNCE',
        'broadcast':        'BROADCAST_MESSAGE',
        'delete':           'DELETE_MESSAGE',
        'receive':          'RECEIVE_MESSAGE',
    }


class UserTypes:
    CLINICIAN = 'CLINICIAN'
    PATIENT = 'PATIENT'
