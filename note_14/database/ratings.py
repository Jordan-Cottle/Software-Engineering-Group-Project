"""
This module contains utilities for accessing rating data in the database
create_rating: Creates a rating for a note.
"""

from config import PermissionType
from models import Rating
from database import check_permission


def create_rating(session, user, note, rating):
    """Creates a rating based on a unique owner, note, and the value of the rating """

    check_permission(session, PermissionType.READ, user, note)

    rating = Rating(owner_id=user.id, note_id=note.id, value=rating)
    session.add(rating)
    return rating


def get_rating(session, user, note):
    """Creates retrieves a rating based on a unique owner, note"""

    check_permission(session, PermissionType.READ, user, note)

    rating = session.query(Rating).filter_by(owner_id=user.id, note_id=note.id).first()

    return rating
