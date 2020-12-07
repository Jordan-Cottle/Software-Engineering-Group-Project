""" 
This module contains utilities for accessing rating data in the database 

"""

from models import Note, User, Rating


def create_rating(session, user, note, rating):
    """Creates a rating based on a unique owner, note, and the value of the rating """
    rating = Rating(owner=user.id, note_id=note.id, value=rating)
    session.add(rating)
    return rating
