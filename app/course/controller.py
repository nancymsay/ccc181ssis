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
        name = request.form.get("course_name")
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

@course_bp.route('/update/', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        courseCode = request.form.get('courseCode')
        courseName = request.form.get('courseName')
        collegeCode = request.form.get("collegeCode")
        originalCode = request.form.get("originalCode")
        
        print(courseCode, courseName, collegeCode)
        
        course = Course()
        course.courseCode = courseCode
        course.courseName = courseName
        course.collegeCode = collegeCode
        
        course.update(courseCode, courseName, collegeCode, originalCode)               
        
        return redirect('/course/')

    colleges = Course().get_college_codes()  
    courseCode = request.args.get('courseCode')
    courseName = request.args.get('courseName')  
    collegeCode=request.args.get('collegeCode')
    return render_template("update_course.html", courseCode=courseCode, courseName=courseName, collegeCode=collegeCode, colleges=colleges)


@course_bp.route('/delete/', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        courseCode = request.form.get('courseCode')
        if Course.delete(courseCode):
            return redirect('/course/')
        else:
            return "Failed to delete the course."
    return render_template("delete_course.html")

@course_bp.route('/warning')
def warning():
    courseCode = request.args.get('courseCode')
    return render_template("delete_course.html", courseCode=courseCode)

@course_bp.route('/search/', methods=['GET', 'POST'])
def search():
    courses = []
    if request.method == 'POST':
        search_query = request.form.get('course_search')
        if search_query:
            courses = Course().search(search_query)
    return render_template('course.html', courses=courses)
