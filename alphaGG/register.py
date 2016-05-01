#!/bin/env python3

import discord


class CommandRegister(object):
    """
    A static class representing all commands registered to the bot.
    """
    commands = []

    @staticmethod
    def register_command(command):
        CommandRegister.commands.append(command)  # Add the command to the pool
        command.on_registration()  # Call the on_registration() method.


class Command(object):
    """
    A class representing a bot command.
    """
    command = None
    help = ''  # Short help command
    verbose_help = ''  # Verbose help command for when the user types 'help <commandname>'

    def __init__(self):
        # This parameter is used to optionally respond back in the channel
        self.response = ''

    def handle(self, message: discord.Message, client: discord.Client):
        """
        Handler method for when command matches the called command
        """
        pass

    @staticmethod
    def on_registration():
        """
        This method get's called whenever a command get's registered via the CommandRegister's register_command() method
        """
        pass
