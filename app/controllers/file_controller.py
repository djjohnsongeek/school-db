from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, current_app
from app.repo import class_repo
from app.auth import login_required
from app.services import files_service

files_blueprint = Blueprint("files", __name__)

# /files/classes/1/roster
# /files/classes/2/attendance
@login_required
@files_blueprint.route("/files/<category>/<int:class_id>/<item>", methods=["GET"])
def download(category: str, class_id: int, item: str):
    # TODO: use cat, and item to direct method call
    file_name = files_service.get_class_roster_file(class_id)
    return send_from_directory(current_app.config["DOWNLOAD_DIR"], file_name)
