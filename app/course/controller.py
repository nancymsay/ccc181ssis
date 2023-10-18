from flask import render_template, redirect, request
from flask import Blueprint
import app.models as models
#from app.course.forms import course_form
#from app.models.course import course
	
course_bp = Blueprint('course', __name__)
	
@course_bp.route("/")
def index():
    return render_template("course.html")

@course_bp.route('/add/')
def add():
    return render_template("add_course.html")

@course_bp.route('/update/')
def update():
    return render_template("update_course.html")

@course_bp.route('/delete/')
def delete():
    return render_template("delete_course.html")
