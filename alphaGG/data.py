#!/bin/env python3

import sqlite3


class Database(object):
    """
    Central storage class for bot data.
    """
    def __init__(self):
        self.connection = sqlite3.connect('bot.sqlite3')
        self.cursor = self.connection.cursor()
