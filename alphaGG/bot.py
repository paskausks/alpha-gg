#!/bin/env python3

import sys
import os
import asyncio
import discord
from alphaGG.data import Database
from alphaGG.register import CommandRegister

sys.path.extend([os.path.dirname(os.path.dirname(os.path.abspath(__file__)))])

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
    CommandRegister.register_command(c)


@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user.name))

    status = discord.Game()
    status.name = '{}help Simulator'.format(config.COMMAND_PREFIX)
    await client.change_status(status)

    while True:
        # Run background tasks once in a second.
        for cls in CommandRegister.commands:
            try:
                await cls.background(client)
            except TypeError:
                cls.background(client)

        await asyncio.sleep(1)  # Run background tasks once in a second


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    for cls in CommandRegister.commands:
        # look through all registered command classes. See if there's a match for the command trigger, initialize it
        # and call it's handle() method.
        if cls.trigger(message):
            cmd = cls(message, client)
            try:
                await cmd.handle()
            except TypeError:
                # handle() Not a coroutine
                cmd.handle()

            if cmd.response:
                # Send a response if it has been defined.
                await client.send_message(message.channel, cmd.response)


try:
    client.run(config.BOT_TOKEN)
except discord.errors.LoginFailure:
    sys.stderr.write('Token incorrect. Please check the value of BOT_TOKEN in config.py!\n')
    Database.connection.close()
    sys.exit(1)
