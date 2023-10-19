from flask import render_template, redirect, request
from app.college.forms import college_form
import app.models as models
from app.models.college import College
from flask import Blueprint

college_bp = Blueprint('college', __name__)

@college_bp.route("/")
def index():
    colleges = College().all()
    return render_template("college.html", colleges=colleges)

@college_bp.route('/add/', methods=["GET", "POST"])
def add():
    success_message = None
    error_message = None

    if request.method == "POST":
        code = request.form.get("college_code").upper()
        name = request.form.get("college_name").upper()

        new_college = College()
        new_college.collegeCode = code
        new_college.collegeName = name
        result = new_college.add()

        if result:
            success_message = "College added successfully!"
        else:
            error_message = "A college already exists."

    colleges = College().get_colleges()
    return render_template("add_college.html", success_message=success_message, error_message=error_message, colleges=colleges)

@college_bp.route('/update/', methods=["GET", "POST"])
def update():
    if request.method == 'POST':
        collegeCode = request.form.get('collegeCode')
        collegeName = request.form.get('collegeName')
        originalCode = request.form.get("originalCode")
        
        print(collegeCode, collegeName, originalCode)
        
        college = College()
        college.collegeCode = collegeCode
        college.collegeName = collegeName
        college.update(collegeCode, collegeName, originalCode)
        
        return redirect('/college/')
        
    collegeCode = request.args.get('collegeCode')
    collegeName = request.args.get('collegeName')
    return render_template("update_college.html", collegeCode=collegeCode, collegeName=collegeName)


@college_bp.route('/delete/')
def delete():
    return render_template("delete_college.html")