#!/bin/env python3

import discord
import requests
from alphaGG.register import Command

""""
Commands to interact with the API of SC2CM
https://github.com/pundurs/sc2cm
"""

SC2CM_HOST = 'http://t11.ka2.lv'


class Top(Command):
    command = 'top'
    help = 'Returns the top 10 players in Galactic Gaming by ladder points.'
    verbose_help = '`top` - Returns the top 10 players in Galactic Gaming by ladder points.'

    def handle(self, message: discord.Message, client: discord.Client):
        response = requests.get('{}/api/top'.format(SC2CM_HOST))

        self.response = 'The top 10 players in Galactic Gaming by ladder points, at the moment are:\n'

        for i, player in enumerate(response.json()['players']):
            self.response += '{pos}. **{name}** ({league} {race}) - *{points}*\n'.format(
                pos=i + 1,
                name=player['name'],
                league=player['league'],
                race=player['race'],
                points=player['score']
            )

        self.response += '\n\nSee the whole list at {}'.format(SC2CM_HOST)


class Player(Command):
    command = 'player'
    help = 'Returns the details of a clan player in the GG SC2CM database.'
    verbose_help = '`player <keyword>` - Returns the details of a clan player in the GG SC2CM database.'

    def handle(self, message: discord.Message, client: discord.Client):
        kw = ' '.join(message.content.split(' ')[1:])  # Ignore the first arg, which is the command itself
        if not kw:
            Player.response = 'You must provide a player argument!'
            return

        response = requests.get('{}/api/player/{}'.format(SC2CM_HOST, kw))

        if response.status_code == 404:
            self.response = 'This person either isn\'t a clan member or just doesn\'t exist in my database.'
            return

        p = response.json()['player']
        self.response = """**{name}**, a rank {rank} {league} {race} from {country} with {points} points
W/L: {wins}/{losses} ({winrate} % winrate in {total} games)
Last played: {last_played}

More on Battle.net: *{bnet_url}*
        """.format(
            name=p['name'],
            rank=p['rank'],
            league=p['league'],
            race=p['race'],
            country=p['country'],
            points=p['score'],
            wins=p['wins'],
            losses=p['losses'],
            winrate=p['winrate'],
            total=p['total_games'],
            last_played=p['last_game'],
            bnet_url=p['bnet_profile_url']
        )

        if p['twitch_url']:
            self.response += '\nWatch live at: *{}*\n'.format(p['twitch_url'])


class ClanWar(Command):
    command = 'cw'
    help = 'Returns a list of upcoming clan wars or, if an ID is supplied, details of a clan war.'
    verbose_help = """`cw <optional ID>` - Returns a list of upcoming clan wars.\n If an optional ID is supplied, \
details for that specific clan war are shown."""

    def handle(self, message: discord.Message, client: discord.Client):

        # TODO: Refactor getting the arguments into an instance method!
        cw_id = ' '.join(message.content.split(' ')[1:])  # Ignore the first arg, which is the command itself

        if cw_id:
            try:
                cw_id = int(cw_id)
            except ValueError:
                self.response = 'The clan war ID has to be a number!'
                return

            response = requests.get('{}/api/cw/{}'.format(SC2CM_HOST, cw_id))

            if response.status_code == 404:
                self.response = 'A clan war with the ID {} wasn\'t found.'.format(cw_id)
                return

            r = response.json()['clanwar']

            self.response = """*{date}* vs **{opponent}**
In game channel: *{chan}*

Notes:
{notes}
""".format(
                date=r['datetime'],
                opponent=r['opponent'],
                chan=r['ingame_channel'],
                notes=r['notes']
            )

            if r['players']:
                self.response += '\nPlayers:\n'
                for p in r['players']:
                    self.response += '{name} ({league} {race})\n'.format(
                        name=p['name'],
                        league=p['league'],
                        race=p['race']
                    )
            else:
                self.response += '\nNo registered players.'

            return

        response = requests.get('{}/api/cw'.format(SC2CM_HOST)).json()

        if not response['clanwars']:
            self.response = 'No upcoming clan wars.'
            return

        self.response = 'Upcoming clan wars are:\n'

        for cw in response['clanwars']:
            self.response += 'ID *{id}*, at *{date}* vs **{opponent}** - {url}\n'.format(
                id=cw['id'],
                date=cw['datetime'],
                opponent=cw['opponent'],
                url='{}/cw/{}'.format(SC2CM_HOST, cw['id'])
            )

        self.response += '\nSee the whole list at {}/cw'.format(SC2CM_HOST)
