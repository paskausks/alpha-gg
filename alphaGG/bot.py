#!/bin/env python3

import sys
import os
import discord

sys.path.extend([os.path.dirname(os.path.dirname(os.path.abspath(__file__)))])

from alphaGG import register

try:
    from alphaGG import config
except ImportError:
    sys.stderr.write('config.py not found. Please create it by using config.example.py as a template!')
    sys.exit(1)

try:
    command_prefix = config.COMMAND_PREFIX
except AttributeError:
    sys.stderr.write('COMMAND_PREFIX not found in config.py. Please, define it!')
    sys.exit(1)

description = 'An interactive bot for Galactic Gaming\'s Discord server'

client = discord.Client()

# Register commands
commands = config.COMMANDS

if not commands:
    sys.stderr.write('No commands registered in config.py!')

for c in commands:
    register.CommandRegister.register_command(c)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    for cls in register.CommandRegister.commands:
        # look through all registered command classes. See if there's a match for the command trigger, initialize it
        # and call it's handle() method.
        if message.content.startswith('{}{}'.format(command_prefix, cls.command)):
            cmd = cls()
            cmd.handle(message, client)
            if cmd.response:
                # Send a response if it has been defined.
                await client.send_message(message.channel, cmd.response)


try:
    client.run(config.BOT_TOKEN)
except discord.errors.LoginFailure:
    sys.stderr.write('Token incorrect. Please check the value of BOT_TOKEN in config.py!\n')
    sys.exit(1)
