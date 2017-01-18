from switch_command import SwitchCommand

class CommandFactory:
    @staticmethod
    def get_command(command_string):
        command_args = command_string.split()
        command_name = command_args[0]
        del command_args[0]
        if command_name == 'SWITCH':
            return SwitchCommand(" ".join(command_args))
   