""" Controller module for creating views.

Flask routes should be defined here.
"""

from server import app

from flask import render_template

from data import NOTES


@app.route("/")
def main_page():
    """ Render the main landing page. """
    return render_template("index.html")


@app.route("/notes")
def list_notes():
    """ Render the notes list page. """
    return render_template("notes.html", notes=NOTES)


@app.route("/notes/<note_id>")
def view_note(note_id):
    """ Render individual note page. """
    return render_template("note.html", note=NOTES[int(note_id)])
