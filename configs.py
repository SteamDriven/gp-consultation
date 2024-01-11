class Commands:
    REGISTER = 'REGISTER'
    LOGIN = 'LOGIN'
    REFERRAL = 'REFERRAL'
    VALIDATE_REGISTER = 'VALIDATE REGISTER'
    COMMAND_REFERRAL = 'REFERRAL'
    COMMAND_END = 'END'
    COMMAND_COMPLETED = 'COMPLETED'
    COMMAND_PASSED = 'PASSED'
    COMMAND_FAILED = 'FAILED'
    COMMAND_ACCEPT = 'ACCEPT'
    COMMAND_DENY = 'DENY'
    COMMAND_REQUEST_DOCTOR = 'R_DOCTOR'
    RETURN_DOCTORS = 'RETURN_DOCTOR'

    chat_commands = {

        'announcement':     'SERVER_ANNOUNCE',
        'broadcast':        'BROADCAST_MESSAGE',
        'delete':           'DELETE_MESSAGE',
        'receive':          'RECEIVE_MESSAGE',
    }


class UserTypes:
    CLINICIAN = 'CLINICIAN'
    PATIENT = 'PATIENT'
