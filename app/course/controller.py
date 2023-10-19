from flask import render_template, redirect, request
from flask import Blueprint
import app.models as models
from app.course.forms import course_form
from app.models.course import *
	
course_bp = Blueprint('course', __name__)
	
@course_bp.route("/")
def index():
    courses = Course().all()
    return render_template("course.html", courses=courses)

@course_bp.route('/add/', methods=['GET', 'POST'])
def add():
    form = course_form()
    success_message = None
    error_message = None

    if request.method == "POST":
        code = request.form.get("course_code").upper()
        name = request.form.get("course_name").upper()
        collegeCode = request.form.get("college_code")

        new_course = Course()
        new_course.courseCode = code
        new_course.courseName = name
        new_course.collegeCode = collegeCode
        result = new_course.add()

        if result:
            success_message = "Course added successfully!"
        else:
            error_message = "Course already exists."
            
    colleges = Course().get_college_codes()
    return render_template("add_course.html", course_form=form, success_message=success_message, error_message=error_message, colleges=colleges)

@course_bp.route('/update/')
def update():
    return render_template("update_course.html")

@course_bp.route('/delete/')
def delete():
    return render_template("delete_course.html")
