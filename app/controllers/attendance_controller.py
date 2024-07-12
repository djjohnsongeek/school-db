from flask import Blueprint, render_template, request, redirect, url_for
from app.services import class_service, controller_service

attendance_blueprint = Blueprint("attendance", __name__)

@attendance_blueprint.route("/attendance", methods=["GET"])
def home():
    return render_template("/attendance/index.html")