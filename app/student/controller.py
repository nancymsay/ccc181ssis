from flask import render_template, redirect, request
from flask import Blueprint
import app.models as models
from app.student.forms import student_form
from app.models.student import *

student_bp = Blueprint('student', __name__)

@student_bp.route("/")
def index():
    students = Student().all()
    return render_template("student.html", students=students)

@student_bp.route('/add/', methods=['GET', 'POST'])
def add():
    form = student_form()
    success_message = None
    error_message = None

    if request.method == "POST":
        studentID = request.form.get("student_id")
        firstName = request.form.get("first_name")
        lastName = request.form.get("last_name")
        course = request.form.get("course")        
        year = request.form.get("year")
        gender = request.form.get("gender")
        
        new_student = Student()
        new_student.studentID = studentID
        new_student.firstName = firstName
        new_student.lastName = lastName
        new_student.course = course
        new_student.year = year
        new_student.gender = gender
        result = new_student.add()

        if result:
            success_message = "Student added successfully!"
        else:
            error_message = "Student already exists."
            
    courses = Student().get_course_codes()
    return render_template("add_student.html", student_form=form, success_message=success_message, error_message=error_message, courses=courses)

@student_bp.route('/update/', methods=["GET", "POST"])
def update():
    if request.method == 'POST':
        studentID = request.form.get('studentID')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        course = request.form.get('course')
        year = request.form.get('year')
        gender = request.form.get('gender')
        originalCode = request.form.get("originalCode")
        
        print(studentID, firstName, lastName, course, year, gender, originalCode)
        
        student = Student()
        student.studentID = studentID
        student.firstName = firstName
        student.lastName = lastName
        student.course = course
        student.year = year
        student.gender = gender
        student.update(studentID, firstName, lastName, course, year, gender, originalCode)
        
        return redirect('/student/')
      
    studentID = request.args.get('studentID')
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    course = request.args.get('course')
    year = request.args.get('year')
    gender = request.args.get('gender')
    courses = Student().get_course_codes()  
    return render_template("update_student.html", studentID=studentID, firstName=firstName, lastName=lastName, course=course, year=year, gender=gender, courses=courses)

@student_bp.route('/delete/')
def delete():
    return render_template("delete_student.html")
