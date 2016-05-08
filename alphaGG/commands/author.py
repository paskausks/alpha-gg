#!/bin/env python3

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
