#!/bin/env python3

import discord
from alphaGG.data import Database

"""
The base class for defining commands and plugins to use with the bot.
"""


class Command(object):
    """
    A class representing a bot command.
    """
    command = None
    help = ''  # Short help command
    verbose_help = ''  # Verbose help command for when the user types 'help <commandname>'

    def __init__(self, message: discord.Message, client: discord.Client, database: Database):
        # This parameter is used to optionally respond back in the channel
        self.response = ''
        self.message = message
        self.client = client
        self.database = database

    @classmethod
    def trigger(cls, message: discord.Message):
        """
        This method determines if the handle() method of the instance should be called.
        By default it check's if the message starts with the bot command prefix and the current classes command,
        but of course can be used to check if the message content matches a regex, comes from a specific role, user etc.
        :return: boolean
        """
        from alphaGG.config import COMMAND_PREFIX
        return message.content.startswith('{}{}'.format(COMMAND_PREFIX.prefix, cls.command))

    def handle(self):
        """
        Handler method for when command matches the called command.
        Command can be a regular method as well as a asyncio coroutine.
        """
        pass

    @staticmethod
    def background(client: discord.Client):
        """
        Method ran once in a specified period of time for background tasks
        """
        pass

    @staticmethod
    def on_registration():
        """
        This method get's called whenever a command get's registered via the CommandRegister's register_command() method
        """
        pass