#!/bin/env python3

class CommandRegister(object):
    """
    A static class representing all commands registered to the bot.
    """
    commands = []

    @staticmethod
    def register_command(command):
        CommandRegister.commands.append(command)  # Add the command to the pool
        command.on_registration()  # Call the on_registration() method.

