"""
Module for containing user related models
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models import Base


class User(Base):
    """ Represents a registered user of the application. """

    __tablename__ = "user"

    id = Column("user_id", Integer, primary_key=True)
    name = Column("name", String, unique=True, index=True)
    password = Column("password", String)
    salt = Column("salt", String)

    notes = relationship("Note", order_by="Note.id", backref="owner")

    def __str__(self):
        return f"User {self.name}"

    def __repr__(self) -> str:
        return f"User (id={self.id}, name='{self.name}')"
