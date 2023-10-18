from flask import render_template, redirect, request
from app.college.forms import college_form
import app.models as models
from app.models.college import College
from flask import Blueprint

college_bp = Blueprint('college', __name__)

@college_bp.route("/")
def index():
    return render_template("college.html")

@college_bp.route('/add/', methods=["GET", "POST"])
def add():
    form = college_form()
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

    return render_template("add_college.html", college_form=form, success_message=success_message, error_message=error_message)

@college_bp.route('/update/')
def update():
    return render_template("update_college.html")

@college_bp.route('/delete/')
def delete():
    return render_template("delete_college.html")


# @college_bp.route('/', methods=["GET", "POST"])
# def index():
#     form = college_form()
#     success_message = None
#     error_message = None

#     if request.method == "POST" and form.validate_on_submit():
#         code = request.form['collegeCode'].upper()
#         name = request.form['collegeName'].upper()

#         new_college = College()
#         result = new_college.add(code, name)

#         if result:
#             success_message = "College added successfully!"
#         else:
#             error_message = "A college already exists."

#     return render_template("college.html", college_form=form, success_message=success_message, error_message=error_message)


# @college_bp.route('/college', methods=["GET"])
# def add_college():
#     return render_template("college.html")









# from flask import render_template, redirect, request
# from app.college.forms import college_form
# import app.models as models
# from app.models.college import College
# from flask import Blueprint

# college_bp = Blueprint('college', __name__)

# @college_bp.route('/', methods=["GET", "POST"])
# def index():
#     form = college_form()
#     success_message = None
#     error_message = None

#     if request.method == "POST" and form.validate_on_submit():
#         code = request.form['collegeCode'].upper()
#         name = request.form['collegeName'].upper()
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO students (collegeCode, collegeName) VALUES (%s, %s)", (collegeCode, collegeName))
#         mysql.connection.commit()

#         if result:
#             success_message = "College added successfully!"
#         else:
#             error_message = "A college already exists."

#     return render_template("college.html", college_form=form, success_message=success_message, error_message=error_message)
    
    # form = college_form()
    # success_message = None
    # error_message = None
	
    # if request.method == "POST" and form.validate_on_submit():  
    #     code = form.college_code.data.upper()  
    #     name = form.college_name.data.upper()

    #     new_college = college()
    #     new_college.collegeCode = code
    #     new_college.collegeName = name
    #     result = new_college.add()

    #     if result:
    #         success_message = "College added successfully!"
    #     else:
    #         error_message = "A college already exists."

    # return render_template("college.html", college_form=form, success_message=success_message, error_message=error_message)

# @college_bp.route('/list/')
# def college_list():
#     colleges_data = college.all()
#     print(colleges_data)
#     return render_template('college.html', colleges=colleges_data)