#!/bin/env python3

import discord
import datetime
from dateutil import parser
import feedparser
from math import floor

from alphaGG.command import Command

"""
Posts new TeamLiquid.net news into a server channel.
"""


class TeamLiquidFeed(Command):

    TL_FEED = 'http://www.teamliquid.net/rss/news.xml'
    CHANNEL = 'news'
    LAST_CHECK = None  # Check on initialization
    CHECKING_PERIOD = 10  # Minutes, how often will the bot check for new RSS items

    @staticmethod
    async def background(client: discord.Client):

        # TODO: Refactor into method for determining if to launch background process
        now = datetime.datetime.now(datetime.timezone.utc)

        if TeamLiquidFeed.LAST_CHECK:
            if not TeamLiquidFeed.LAST_CHECK + datetime.timedelta(minutes=TeamLiquidFeed.CHECKING_PERIOD) <= now:
                return

        # Set up next check
        TeamLiquidFeed.LAST_CHECK = now

        # Get RSS feed
        feed = feedparser.parse(TeamLiquidFeed.TL_FEED)

        for f in feed.entries:
            pub_utc = parser.parse(f["published"]).astimezone(datetime.timezone.utc)

            # Only post news items which have appeared since the last checking period
            if pub_utc < now - datetime.timedelta(minutes=TeamLiquidFeed.CHECKING_PERIOD):
                continue

            feed_channel = None
            for s in list(client.servers):
                feed_channel = discord.utils.find(lambda c: c.name == TeamLiquidFeed.CHANNEL, s.channels)

                if feed_channel:
                    break

            if not feed_channel:
                # Channel wasn't found
                return

            rv = """**{title}** by *{author}*.
{description}
Read more: {link}
Posted: {dt} hours ago"""
            await client.send_message(feed_channel, rv.format(
                title=f.title,
                author=', '.join(a.get('name') for a in f.authors),
                description=f.summary,
                link=f.link,
                dt=floor((now - pub_utc).total_seconds() / 60 / 60)
            ))
