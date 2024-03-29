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
        'request doctor':       'R_DOCTOR',
        'return doctor':        'RETURN_DOCTOR',
        'find p':               'FIND PATIENT',
        'find b':               'FIND BOOKING',
        'update b':             'UPDATE BOOKING',

        'page commands': {
            'change p':         'CHANGE TO PATIENT DASH',
            'change d':         'CHANGE TO DOCTOR DASH',
            'warning':          'SHOW LOGIN WARNING'
        },

        'appointments': {
            'create apt':           'CREATE APT',
            'accept apt':           'ACCEPT APT',
            'reject apt':           'DENY APT',
            'update apt':           'UPDATE APT',
        },

        'notifications': {
            'send patient': 'SEND PATIENT NOTIFICATION',
            'send doctor':  'SEND DOCTOR NOTIFICATION',
            'search':       'SEARCH FOR NOTIFICATIONS',
            'send':         'SEND NOTIFICATION',
            'invite':       'INVITE USER',
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
