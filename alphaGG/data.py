#!/bin/env python3

import sqlite3


class Database(object):
    """
    Central storage class for bot data.
    """
    connection = sqlite3.connect('bot.sqlite3')
    cursor = connection.cursor()

