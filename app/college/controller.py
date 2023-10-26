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
        name = request.form.get("college_name")

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

@college_bp.route('/delete/', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        collegeCode = request.form.get('collegeCode')
        if College.delete(collegeCode):
            return redirect('/college/')
        else:
            return "Failed to delete college."
    return render_template("college.html")

@college_bp.route('/warning')
def warning():
    collegeCode = request.args.get('collegeCode')
    return render_template("delete_College.html", collegeCode=collegeCode)

@college_bp.route('/search/', methods=['POST'])
def search():
    colleges = []
    if request.method == 'POST':
        search_category = request.form.get('search_category')
        search_query = request.form.get('college_search')
        if not search_query and search_category == 'all':
            colleges = College().all()
        elif search_query:
            colleges = College.search(search_category, search_query)
    return render_template('college.html', colleges=colleges)