from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def student():
    return render_template("student.html")

@views.route('/course')
def course():
    return render_template("course.html")

@views.route('/college')
def college():
    return render_template("college.html")