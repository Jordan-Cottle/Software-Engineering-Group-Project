"""
Module for defining database models involving notes

Note -- The main model for representing a note

NoteSection -- Represents a single section of a note.

Rating -- Represents the rating of a single note
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


DATE_FORMAT = "%B %d, %Y"


class Note(Base):
    """ Represents a Note. """

    __tablename__ = "note"
    id = Column("note_id", Integer, primary_key=True)
    title = Column(String)
    created = Column(Date)
    views = Column(Integer)
    owner = Column(Integer, ForeignKey("user.user_id"))
    sections = relationship("NoteSection", order_by="NoteSection.index")
    ratings = relationship("Rating")

    @property
    def text(self):
        """ Gather all of the NoteSection values into a single string. """

        lines = [section.content for section in self.sections]

        return "\n".join(lines)

    @property
    def date(self):
        """ Get a formatted string version of the created date. """

        return self.created.strftime(DATE_FORMAT)

    @property
    def rating(self):
        """ Computes the average of ratings for a single note """
        return sum(rating.value for rating in self.ratings) / len(self.ratings)


class NoteSection(Base):
    """ Represents a section within a Note. """

    __tablename__ = "note_section"
    id = Column("section_id", Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey("note.note_id"), index=True)
    content = Column(String)
    index = Column(Integer)

    def __str__(self):
        return f"{self.index}: {self.content}"

    def __repr__(self) -> str:
        return (
            "NoteSection("
            f"id={self.id}, "
            f"note_id={self.note_id}, "
            f"content='{self.content}', "
            f"index={self.index})"
        )


class Rating(Base):
    """ Represents a rating of a note """

    __tablename__ = "rating"
    owner = Column(Integer, ForeignKey("user.user_id"), index=True, primary_key=True)
    note_id = Column(Integer, ForeignKey("note.note_id"), index=True, primary_key=True)
    value = Column("value", Integer)

    def __str__(self):
        return f"{self.value}"

    def __repr__(self) -> str:
        return (
            f"Rating (owner={self.owner}, note_id={self.note_id}, value={self.value})"
        )
