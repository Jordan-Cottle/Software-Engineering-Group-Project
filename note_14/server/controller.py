""" Controller module for creating views.

Flask routes should be defined here.
"""

from database import (
    create_user,
    get_note,
    get_notes,
    create_note,
    delete_note,
    edit_note,
    UnauthorizedError,
    get_user,
    add_permission,
    has_permission,
)
from config import permissions
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

    return render_template(
        "notes.html",
        notes=notes,
        sort_by=sort_by,
        reverse=reverse,
    )


@app.route("/notes/<int:note_id>")
@login_required
def view_note(note_id):
    """ Render individual note page. """
    return render_template(
        "note.html",
        note=get_note(g.session, note_id, current_user),
        admin=has_permission(
            g.session,
            permissions.PermissionType.ADMIN,
            current_user,
            note=get_note(g.session, note_id, current_user),
        ),
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

    error = request.args.get("error")

    return render_template("login.html", error=error)


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


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
@login_required
def note_delete(note_id):
    """ Delete notes """
    delete_note(g.session, note_id, current_user)

    return redirect(url_for("list_notes"))


@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def note_edit(note_id):
    """ Edit note view controller """
    if request.method == "GET":
        return render_template(
            "edit_note.html", note=get_note(g.session, note_id, current_user)
        )

    title = request.form["title"]
    text = request.form["note_text"]
    edit_note(g.session, title, text, note_id, current_user)

    return redirect(url_for("view_note", note_id=note_id))


@app.route("/notes/<int:note_id>/permissions", methods=["GET", "POST"])
@login_required
def set_permissions(note_id):
    """ Permissions table view controller """
    if request.method == "POST":
        form = request.form
        username = form["user"]
        user = current_user
        otheruser = get_user(g.session, username)
        note = get_note(g.session, note_id, user)
        add_permission(
            g.session,
            permissions.PermissionType.READ,
            otheruser,
            note,
            triggered_by=current_user,
        )

    return render_template(
        "permission_table.html",
        note=get_note(g.session, note_id, current_user),
    )


@app.route("/not_found")
def unauthorized():
    """ Display a generic 404 page for unauthorized requests. """
    return render_template("unauthorized.html")


@app.errorhandler(UnauthorizedError)
def unauthorized_redirect(error):
    """ Send user to the unauthorized page. """
    print(f"UNAUTHORIZED: {error}")
    return redirect(url_for("unauthorized"))
