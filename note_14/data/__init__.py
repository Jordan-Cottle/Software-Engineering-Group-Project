""" Package for providing data to the application. """
# pylint: disable=wrong-import-position

import os
import sqlite3

DB_FILENAME = "note14.db"
EXISTS = os.path.isfile(DB_FILENAME)


class Connection:
    """ Class for handling connections to the database. """

    def __init__(self) -> None:
        self.connection = sqlite3.connect(DB_FILENAME)

    def execute(self, sql):
        """ Executes a raw sql string and returns a cursor to the results. """
        return self.connection.execute(sql)

    def __enter__(self):
        """ Set up for the context manager. """
        return self

    def __exit__(self, *args):
        """ Commit and close connection after we're done with it. """

        self.connection.commit()
        self.connection.close()


from .notes import *
