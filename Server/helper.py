from configs import Commands


class ServerCommands:
    @staticmethod
    def get_referral(client):
        return client.handle_server_messages(Commands.REFERRAL, None, None)

    @staticmethod
    def validate_register(user_type, data, client):
        return client.handle_server_messages(Commands.VALIDATE_REGISTER, user_type, data)
