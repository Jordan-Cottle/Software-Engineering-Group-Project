"""
Module for defining database models involving notes

Note -- The main model for representing a note

NoteSection -- Represents a single section of a note.

Rating -- Represents the rating of a single note
"""
import datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey, LargeBinary, DateTime
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
    sections = relationship(
        "NoteSection", order_by="NoteSection.index", cascade="all, delete-orphan"
    )
    ratings = relationship("Rating", cascade="all, delete-orphan")
    comments = relationship("Comment", cascade="all, delete-orphan")
    attachments = relationship("Attachment", cascade="all, delete-orphan")

    @property
    def text(self):
        """ Gather all of the NoteSection values into a single string. """

        lines = [section.content for section in self.sections]

        return "\n".join(lines)

    @text.setter
    def text(self, value):
        sections = [
            NoteSection(content=line, index=i)
            for i, line in enumerate(value.split("\n"))
        ]
        self.sections = sections

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


class Attachment(Base):
    """ Represents a attachment on a note: Work in progress"""

    __tablename__ = "attachment"
    id = Column("attachment_id", Integer, primary_key=True)
    file_name = Column(String)
    display_name = Column(String)
    note_id = Column(Integer, ForeignKey("note.note_id"), index=True)
    owner = Column(Integer, ForeignKey("user.user_id"), index=True)
    data = Column("data", LargeBinary)

    def __str__(self):
        return f"{self.data}"

    def __repr__(self) -> str:
        return f"Attachment (owner={self.owner}, note_id={self.note_id})"


class Comment(Base):
    """ Represents a comment on a note """

    __tablename__ = "comment"
    id = Column("comment_id", Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey("note.note_id"), index=True)
    owner = Column(Integer, ForeignKey("user.user_id"), index=True)
    body = Column(String)
    date_created = Column("date", DateTime, default=datetime.date.today())

    @property
    def date(self):
        """ Get a formatted string version of the created date. """
        return self.date_created.strftime(DATE_FORMAT)

    def __str__(self):
        return f"{self.body}"

    def __repr__(self) -> str:
        return f"Comment (owner={self.owner}, note_id={self.note_id})"
