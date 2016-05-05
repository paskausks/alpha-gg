#!/bin/env python3
from .commands.sc2cm import (Top, Player, ClanWar)
from .commands import help as help_command
from .commands.teamliquid import TeamLiquidFeed

# Configuration for AlphaGG

# Auth token
BOT_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

COMMAND_PREFIX = '.'

# Registered commands/plugins
COMMANDS = [
    help_command.Help,
    Top,
    Player,
    ClanWar,
    TeamLiquidFeed
]
