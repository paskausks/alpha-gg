#!/bin/env python3
import time

from alphaGG.command import Command

"""
Return some info about the bot author.
"""

AUTHOR_ID = 124137111975755776


class Author(Command):
    command = 'author'
    help = 'Returns some info about the author.'
    verbose_help = '`author` - Returns some information about the author as well as a link to the source code.'

    def handle(self):
        self.response = 'Made with :heart: by <@{}>. Source: {}'.format(
            AUTHOR_ID,
            'https://github.com/pundurs/alpha-gg'
        )


class Uptime(Command):
    """
    Uptime command borrowed from Grifs99' Refrigerator
    https://github.com/Grifs99/Refrigerator/
    """
    command = 'uptime'
    help = 'Returns bot uptime.'
    verbose_help = '`uptime` - Returns bot uptime.'
    init_time = None

    @staticmethod
    def on_registration():
        Uptime.init_time = int(time.time())

    def handle(self):
        timenow = int(time.time())
        dt = timenow - Uptime.init_time
        days = divmod(dt, 86400)
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)
        seconds = minutes[1]
        self.response = 'Uptime - {[0]} days, {[0]} hours, {[0]} minutes, {} seconds.'.format(
            days, hours, minutes, seconds
        )