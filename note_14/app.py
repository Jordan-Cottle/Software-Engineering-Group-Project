import os

from flask import Flask, render_template


from data import NOTES

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "127.0.0.1"), port=int(os.getenv("PORT", 5000)), debug=True
    )