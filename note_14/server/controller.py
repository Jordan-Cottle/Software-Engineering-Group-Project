""" Controller module for creating views.

Flask routes should be defined here.
"""
import os
from database import (
    create_user,
    get_note,
    get_notes,
    create_note,
    delete_note,
    edit_note,
    UnauthorizedError,
    get_user,
    has_permission,
    update_permissions,
    add_comment,
    delete_comment,
    create_rating,
    get_rating,
    add_attachment,
    get_attachment,
    delete_attachment,
)
from config import PermissionType, ALLOWED_EXTENSIONS
from flask import g, redirect, render_template, request, flash, send_file
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
    note = get_note(g.session, note_id, current_user)
    note.views += 1
    g.session.commit()
    rating = get_rating(g.session, current_user, note)
    return render_template(
        "note.html",
        note=get_note(g.session, note_id, current_user),
        admin=has_permission(
            g.session,
            PermissionType.ADMIN,
            current_user,
            note=note,
        ),
        can_edit=has_permission(
            g.session, PermissionType.EDIT, current_user, note=note
        ),
        can_comment=has_permission(
            g.session, PermissionType.COMMENT, current_user, note=note
        ),
        rating=rating,
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


@app.route("/notes/<int:note_id>/rate", methods=["POST"])
@login_required
def rate_note(note_id):
    """ Controller for adding and editing ratings """
    note = get_note(g.session, note_id, current_user)
    rating = request.form["rate"]
    if get_rating(g.session, current_user, note) is None:
        create_rating(g.session, current_user, note, rating)
    else:
        get_rating(g.session, current_user, note).value = rating

    return redirect(url_for("view_note", note_id=note_id))


@app.route("/notes/<int:note_id>/comments", methods=["POST"])
def create_comment(note_id):
    """ Controller for adding comments """
    note = get_note(g.session, note_id, current_user)
    form = request.form
    body = form["body"]
    add_comment(g.session, body, note, current_user)

    return redirect(url_for("view_note", note_id=note_id))


@app.route("/notes/<int:note_id>/comments/<int:comment_id>/remove", methods=["POST"])
def remove_comment(comment_id, note_id):
    """ Controller for removing comments """
    note = get_note(g.session, note_id, current_user)
    delete_comment(g.session, comment_id, note, current_user)

    return redirect(url_for("view_note", note_id=note_id))


@app.route("/notes/<int:note_id>/permissions", methods=["GET", "POST"])
@login_required
def set_permissions(note_id):
    """ Permissions table view controller """
    note = get_note(g.session, note_id, current_user)

    permissions = {}

    for permission in note.permissions:
        if permission.user_id == current_user.id:
            continue

        permissions.setdefault(permission.user, {})[permission.type] = "true"

    if request.method == "POST":
        form = request.form

        i = 0
        # Update permissions for existing users
        while f"user_{i}" in form:
            user_id = form[f"user_{i}"]
            user = get_user(g.session, user_id=user_id)
            user_permissions = []
            for permission_type in PermissionType:
                if form.get(f"{permission_type.value}_{i}") is not None:
                    user_permissions.append(permission_type)

            new_permissions = update_permissions(
                g.session, user_permissions, user, note, triggered_by=current_user
            )
            permissions[user] = {
                permission.type: "true" for permission in new_permissions
            }
            i += 1

        # Process new user entry
        new_user_name = form["new_user"]
        if new_user_name:
            user = get_user(g.session, name=new_user_name)
            user_permissions = []
            for permission_type in PermissionType:
                if form.get(f"new_{permission_type.value}") is not None:
                    user_permissions.append(permission_type)

            new_permissions = update_permissions(
                g.session, user_permissions, user, note, triggered_by=current_user
            )
            permissions[user] = {
                permission.type: "true" for permission in new_permissions
            }

    return render_template(
        "permission_table.html",
        note=note,
        permissions=permissions,
        permission_types=list(PermissionType),
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


def allowed_file(filename):
    """ Checking file extensions """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/notes/<int:note_id>/uploads", methods=["GET", "POST"])
def upload_file(note_id):
    """ Controller for upload an attachment """
    g.pop("_flashes", None)
    if request.method == "POST":
        note = get_note(g.session, note_id, current_user)
        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(url_for("view_note", note_id=note_id))

        if file and allowed_file(file.filename):
            add_attachment(g.session, file, note, current_user)
            flash("File successsfully uploaded")
        else:
            flash("ERROR: File extension not allowed")

    return redirect(url_for("view_note", note_id=note_id))


@app.route(
    "/notes/<int:note_id>/<int:attachment_id>download",
    methods=["GET", "POST"],
)
def download(note_id, attachment_id):
    """ Controller for download an attachment """
    note = get_note(g.session, note_id, current_user)
    attachment = get_attachment(g.session, attachment_id, note, current_user)
    return send_file(
        attachment.file_name,
        attachment_filename=attachment.display_name,
        as_attachment=True,
    )


@app.route("/notes/<int:note_id>/uploads/<int:attachment_id>/delete", methods=["POST"])
def delete_file(note_id, attachment_id):
    """ Controller for  delete an attachment """
    note = get_note(g.session, note_id, current_user)
    attachment = get_attachment(g.session, attachment_id, note, current_user)
    os.remove(attachment.file_name)
    delete_attachment(g.session, attachment_id, note, current_user)
    return redirect(url_for("view_note", note_id=note_id))
