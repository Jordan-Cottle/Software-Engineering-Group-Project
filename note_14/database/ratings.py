"""
This module contains utilities for accessing rating data in the database
create_rating: Creates a rating for a note.
"""

from models import Rating


def create_rating(session, user, note, rating):
    """Creates a rating based on a unique owner, note, and the value of the rating """
    rating = Rating(owner_id=user.id, note_id=note.id, value=rating)
    session.add(rating)
    return rating
