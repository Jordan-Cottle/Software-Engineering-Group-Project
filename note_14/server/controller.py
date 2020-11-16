""" Controller module for creating views.

Flask routes should be defined here.
"""

from server import app

from flask import render_template, g

from database import get_note, get_notes


@app.route("/")
def main_page():
    """ Render the main landing page. """
    return render_template("index.html")


@app.route("/notes")
def list_notes():
    """ Render the notes list page. """
    return render_template("notes.html", notes=get_notes(g.session))


@app.route("/notes/<note_id>")
def view_note(note_id):
    """ Render individual note page. """
    return render_template("note.html", note=get_note(g.session, int(note_id)))
