""" Package for providing data to the application. """
import os
import sqlite3

DB_FILENAME = "note14.db"
EXISTS = os.path.isfile(DB_FILENAME)


class Connection:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(DB_FILENAME)

    def execute(self, sql):
        return self.connection.execute(sql)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.connection.commit()
        self.connection.close()


from .notes import *
