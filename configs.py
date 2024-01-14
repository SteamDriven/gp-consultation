class Commands:

    packet_commands = {
        'register':             'REGISTER',
        'login':                'LOGIN',
        'referral':             'REFERRAL',
        'validate register':    'VALIDATE REGISTER',
        'end':                  'END',
        'complete':             'COMPLETED',
        'pass':                 'PASSED',
        'fail':                 'FAILED',
        'accept':               'ACCEPT',
        'deny':                 'DENY',
        'request_doctor':       'R_DOCTOR',
        'return doctor':        'RETURN_DOCTOR',

        'appointments': {
            'create apt':           'CREATE APT',
            'accept apt':           'ACCEPT APT',
            'reject apt':           'DENY APT',
            'update apt':           'UPDATE APT',
        },

        'notifications': {
            'send patient': 'SEND PATIENT NOTIFICATION',
            'send doctor':  'SEND DOCTOR NOTIFICATION',
        },
    }

    chat_commands = {

        'announcement':     'SERVER_ANNOUNCE',
        'broadcast':        'BROADCAST_MESSAGE',
        'delete':           'DELETE_MESSAGE',
        'receive':          'RECEIVE_MESSAGE',
    }


class UserTypes:
    CLINICIAN = 'CLINICIAN'
    PATIENT = 'PATIENT'
