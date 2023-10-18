from flask import render_template, redirect, request
from flask import Blueprint
import app.models as models
#from app.student.forms import student_form
#from app.models.student import student

student_bp = Blueprint('student', __name__)

@student_bp.route("/")
def index():
    return render_template("student.html")

@student_bp.route('/add/')
def add():
    return render_template("add_course.html")

@student_bp.route('/update/')
def update():
    return render_template("update_course.html")

@student_bp.route('/delete/')
def delete():
    return render_template("delete_course.html")
