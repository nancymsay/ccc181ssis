from flask import render_template, redirect, request
from flask import Blueprint
import app.models as models
from app.student.forms import student_form
from app.models.student import *
import cloudinary
from cloudinary.uploader import upload
from cloudinary.uploader import destroy
from cloudinary.utils import cloudinary_url

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
        firstName = request.form.get("first_name").title()
        lastName = request.form.get("last_name").title()
        course = request.form.get("course")        
        year = request.form.get("year")
        gender = request.form.get("gender")

        # Handle profile picture upload to Cloudinary
        profile_pic = request.files.get('profile_pic')
        if profile_pic:
            upload_result = upload(profile_pic)
            profile_pic_url, _ = cloudinary_url(upload_result['public_id'], format=upload_result['format'])
        else:
            profile_pic_url = None

        new_student = Student()
        new_student.studentID = studentID
        new_student.firstName = firstName
        new_student.lastName = lastName
        new_student.course = course
        new_student.year = year
        new_student.gender = gender
        new_student.profilepic = profile_pic_url  # Assuming there is a 'profilepic' field in your Student model
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
        originalProfilePic = request.form.get("originalProfilePic")

        # Handle profile picture upload to Cloudinary
        new_profile_pic = request.files.get('profile_pic')
        if new_profile_pic:
            # Upload new profile picture
            upload_result = upload(new_profile_pic)
            new_profile_pic_url, _ = cloudinary_url(upload_result['public_id'], format=upload_result['format'])
            
            # Destroy the old profile picture on Cloudinary
            if originalProfilePic:
                public_id = originalProfilePic.split('/')[-1].split('.')[0]
                destroy(public_id)

        else:
            new_profile_pic_url = originalProfilePic

        # Update student information including the profile picture URL
        student = Student()
        student.studentID = studentID
        student.firstName = firstName
        student.lastName = lastName
        student.course = course
        student.year = year
        student.gender = gender
        student.profilepic = new_profile_pic_url
        student.update(studentID, firstName, lastName, course, year, gender, new_profile_pic_url, originalCode)

        return redirect('/student/')
      
    studentID = request.args.get('studentID')
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    course = request.args.get('course')
    year = request.args.get('year')
    gender = request.args.get('gender')
    originalProfilePic = Student.get_profile_pic_url(studentID) 
    courses = Student().get_course_codes()  
    
    return render_template("update_student.html", studentID=studentID, firstName=firstName, lastName=lastName, course=course, year=year, gender=gender, profilepic=originalProfilePic, courses=courses)

@student_bp.route('/delete/', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        studentID = request.form.get('studentID')
        
        # Get the profile picture URL before deleting the student
        profile_pic_url = Student.get_profile_pic_url(studentID)

        # Delete the student
        if Student.delete(studentID):
            # If a profile picture exists, delete it from Cloudinary
            if profile_pic_url:
                public_id = profile_pic_url.split('/')[-1].split('.')[0]
                destroy(public_id)
            
            return redirect('/student/')
        else:
            return "Failed to delete the student."
    
    return render_template("student.html")

@student_bp.route('/warning')
def warning():
    studentID = request.args.get('studentID')
    return render_template("delete_student.html", studentID=studentID)


@student_bp.route('/search/', methods=['POST'])
def search():
    students = []
    if request.method == 'POST':
        search_category = request.form.get('search_category')
        search_query = request.form.get('student_search')
        if not search_query and search_category == 'all':
            students = Student.all()
        elif search_query:
            students = Student.search(search_category, search_query)
    return render_template('student.html', students=students)