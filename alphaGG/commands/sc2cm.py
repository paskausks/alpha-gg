#!/bin/env python3
import datetime

import discord
import requests
from alphaGG.command import Command

""""
Commands to interact with the API of SC2CM
https://github.com/pundurs/sc2cm
"""

SC2CM_HOST = 'http://t11.ka2.lv'


class Top(Command):
    command = 'top'
    help = 'Returns the top 10 players in Galactic Gaming by ladder points.'
    verbose_help = '`top` - Returns the top 10 players in Galactic Gaming by ladder points.'

    def handle(self):
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

    def handle(self):
        kw = ' '.join(self.message.content.split(' ')[1:])  # Ignore the first arg, which is the command itself
        if not kw:
            Player.response = 'You must provide a player argument!'
            return

        response = requests.get('{}/api/player/{}'.format(SC2CM_HOST, kw))

        if response.status_code == 404:
            self.response = 'This person either isn\'t a clan member or just doesn\'t exist in my database.'
            return

        p = response.json()['player']

        country = p['country'] if p['country'] else 'an undisclosed location'

        player_description = """a rank {rank} {league} {race} from {country} with {points} points
W/L: {wins}/{losses} ({winrate} % winrate in {total} games).""".format(
            rank=p['rank'],
            league=p['league'],
            race=p['race'],
            country=country,
            points=p['score'],
            wins=p['wins'],
            losses=p['losses'],
            winrate=p['winrate'],
            total=p['total_games'],
        )
        if not p['ranked']:
            player_description = 'a unranked player from {}.'.format(country)
        self.response = """**{name}**, {player_description}
Last played: {last_played}

Battle.net: *{bnet_url}*
        """.format(
            name=p['name'],
            player_description=player_description,
            last_played=p['last_game'],
            bnet_url=p['bnet_profile_url']
        )

        if p['twitch_url']:
            self.response += '\nWatch live at: *{}*\n'.format(p['twitch_url'])

        if p['rankedftw_url']:
            self.response += '\nRFTW ladder rank: *{}*\n'.format(p['rankedftw_url'])

        if p['rankedftw_graph_url']:
            self.response += 'RFTW career graph: *{}*\n'.format(p['rankedftw_graph_url'])


class ClanWar(Command):
    CW_PLAYER_ROLE = 'CW Players'
    CW_CHANNEL = 'clanwars'

    LAST_CHECK = datetime.datetime.now()  # Timestamp when the bot last checked if a CW isn't coming soon
    CHECKING_PERIOD = 1  # Minutes, how often will the bot check for imminent clan wars
    TIME_TO_CW = 30  # When it's this amount of minutes until a clan war, it will trigger the announcement.
    TZ_OFFSET = 3  # All clan wars are specified in CEST

    command = 'cw'
    help = """Returns a list of upcoming clan wars or, if an ID and action is supplied, details of a clan war and \
promoting that clan war to CW players"""
    verbose_help = """`cw` - Returns a list of upcoming clan wars.
`cw get <id>` - Shows details about an upcoming clan war.
`cw promote <id>` - Promotes a clan war to the {role} role in the #{chan} channel and messages the role members \
privately.
""".format(
        role=CW_PLAYER_ROLE,
        chan=CW_CHANNEL
    )

    CW_LIST = '{}/api/cw'.format(SC2CM_HOST)  # URL for fetching upcoming clan wars.

    announced_cws = []  # To keep track if a CW has already been announced. TODO: Use a local datastore for this

    @staticmethod
    def background(client: discord.Client):
        now = datetime.datetime.now()
        if not ClanWar.LAST_CHECK + datetime.timedelta(minutes=ClanWar.CHECKING_PERIOD) <= now:
            return

        # Set up next check
        ClanWar.LAST_CHECK = now

        cw_list = requests.get(ClanWar.CW_LIST).json()['clanwars']

        # Check if any of the clan wars are nearer than
        for cw in cw_list:
            cw_time = datetime.datetime.fromtimestamp(
                cw['datetime_timestamp']
            ) - datetime.timedelta(hours=ClanWar.TZ_OFFSET)

            cw_id = cw['id']

            if cw_id not in ClanWar.announced_cws and \
                        now >= cw_time - datetime.timedelta(minutes=ClanWar.CHECKING_PERIOD):
                # Imminent CW found. Announce.
                ClanWar.announced_cws.append(cw_id)
                break

    # Decorated as a coroutine, so client.send_message can be used
    async def handle(self):

        args = self.message.content.split(' ')
        try:
            action = args[1]  # Ignore the first arg, which is the command itself
            cw_id = args[2]
        except IndexError:
            cw_id = None
            action = None

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

            if action == 'get':
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

            elif action == 'promote':
                # Promotion command invoked
                cw_role = discord.utils.find(lambda r: r.name == self.CW_PLAYER_ROLE, self.message.server.roles)
                cw_chan = discord.utils.find(lambda c: c.name == self.CW_CHANNEL, self.client.get_all_channels())
                self.response = ''

                cw_link = '{}/cw/{}'.format(SC2CM_HOST, r['id'])

                player_list = '\n{} players registered'.format(len(r['players']))

                if r['players']:
                    player_list += ' - '
                    for p in r['players']:
                        player_list += '{} '.format(p['name'])

                await self.client.send_message(
                    cw_chan,
                    '{}, take a look at an upcoming CW vs **{}** - {}{}!'.format(
                        cw_role.mention, r['opponent'], cw_link, player_list
                    )
                )

                # PM all of the members of the role
                for member in list(self.message.server.members):
                    if cw_role in member.roles:
                        await self.client.send_message(
                            member,
                            'Hey, {}! {} wants you to look at an upcoming CW vs **{}** - {}{}'.format(
                                member.name, self.message.author.name, r['opponent'], cw_link, player_list
                            )
                        )

                self.response = 'Success!'

                return

            return

        response = requests.get(ClanWar.CW_LIST).json()

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
