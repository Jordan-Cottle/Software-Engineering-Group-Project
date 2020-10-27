from server import app

from flask import render_template

from data import NOTES

@app.route("/")
@app.route("/index")
def main_page():
    return render_template("index.html")

@app.route("/notes")
def list_notes():
    return render_template("notes.html", notes=NOTES)

@app.route("/notes/<note_id>")
def view_note(note_id):
    return render_template("note.html", note=NOTES[int(note_id)])
