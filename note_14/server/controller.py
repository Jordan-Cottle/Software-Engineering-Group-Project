""" Controller module for creating views.

Flask routes should be defined here.
"""

from database import create_user, get_note, get_notes, create_note, delete_note
from flask import g, redirect, render_template, request
from flask.helpers import url_for
from flask_login import current_user, login_required

from server import app, login


@app.route("/")
def main_page():
    """ Render the main landing page. """
    return render_template("index.html")


@app.route("/notes")
@login_required
def list_notes():
    """ Render the notes list page. """

    sort_by = request.args.get("sort", default="title")
    reverse = request.args.get("reverse", default="False") == "True"

    notes = get_notes(g.session, current_user)

    if sort_by == "owner":
        notes = sorted(notes, key=lambda note: note.owner.name, reverse=reverse)
    else:
        notes = sorted(notes, key=lambda note: getattr(note, sort_by), reverse=reverse)

    return render_template("notes.html", notes=notes, sort_by=sort_by, reverse=reverse)


@app.route("/notes/<note_id>")
@login_required
def view_note(note_id):
    """ Render individual note page. """
    return render_template(
        "note.html", note=get_note(g.session, int(note_id), current_user)
    )


@app.route("/login", methods=["GET", "POST"])
def user_login():
    """ Render login page and process login requests. """

    if request.method == "POST":
        form = request.form

        user_name = form["user_name"]
        password = form["password"]

        # Login and validate the user.
        login(user_name, password)

        return redirect(url_for("main_page"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def create_account():
    """ Render register page and process register requests. """

    if request.method == "POST":
        form = request.form

        user_name = form["user_name"]
        password = form["password"]

        # Register and Login the user.
        create_user(g.session, user_name, password)
        g.session.commit()

        login(user_name, password)

        return redirect(url_for("main_page"))

    return render_template("register.html")


@app.route("/notes/create", methods=["GET", "POST"])
@login_required
def create_new_note():
    """ Render create note page and create notes """

    if request.method == "POST":
        form = request.form

        title = form["title"]
        text = form["text"]
        user = current_user
        create_note(g.session, title, text, user)

        return redirect(url_for("list_notes"))

    return render_template("create_note.html")


@app.route("/notes/<note_id>/delete", methods=["POST"])
@login_required
def note_delete(note_id):
    """ Delete notes """
    delete_note(g.session, note_id)

    return redirect(url_for("get_notes"))