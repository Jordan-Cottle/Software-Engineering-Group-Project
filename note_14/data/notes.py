from data import EXISTS, Connection

from datetime import date

if not EXISTS:
    with Connection() as db:
        db.execute(
            """
            CREATE TABLE notes(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TITLE CHAR(64),
                TEXT CHAR(256),
                DATE CHAR(64)
            );"""
        )

DATE_FORMAT = "%B %d, %Y"


def today():
    return date.today().strftime(DATE_FORMAT)


def get_notes():
    with Connection() as db:
        data = db.execute("SELECT id, title, text, date FROM notes").fetchall()

    return [
        {"id": note[0], "title": note[1], "text": note[2], "date": note[3]}
        for note in data
    ]


def get_note(id):
    with Connection() as db:
        note = db.execute(
            f"SELECT id, title, text, date FROM notes WHERE id = {id}"
        ).fetchone()
    return {"id": note[0], "title": note[1], "text": note[2], "date": note[3]}


def create_note(title, text):
    with Connection() as db:
        db.execute(
            f"""
        INSERT INTO NOTES (title, text, date)  
    VALUES ('{title}', '{text}', '{today()}');
        """
        )


if not EXISTS:
    create_note("Test note 1", "This note is here for testing")
    create_note("Test note 2", "This note should be in a database")
