#!/bin/env python3

import discord
from alphaGG import (config, register)

"""
Dynamic help command. Responds with the help properties of the registered command classes.
"""


class Help(register.Command):
    command = 'help'
    help = 'Shows this message.'

    def handle(self, message: discord.Message, client: discord.Client):
        kw = ' '.join(message.content.split(' ')[1:])  # Ignore the first arg, which is the command itself
        if kw:
            # Detailed information for a command request
            for c in config.COMMANDS:
                if kw == c.command:
                    self.response = c.verbose_help
                    return

            self.response = 'A command called {} wasn\'t found'.format(kw)
            return

        self.response = 'Available commands:\n\n'
        for c in config.COMMANDS:
            # General information for all commands
            self.response += '**{}{}**    {}\n'.format(config.COMMAND_PREFIX, c.command, c.help)

        self.response += '\n\ntype {}{} <command> to get more detailed help about a particular command!'.format(
            config.COMMAND_PREFIX,
            Help.command
        )
