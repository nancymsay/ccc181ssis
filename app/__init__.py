import cloudinary
from flask import Flask, render_template
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, BOOTSTRAP_SERVE_LOCAL, CLOUD_NAME, API_KEY, API_SECRET 
from flask_wtf.csrf import CSRFProtect

mysql = MySQL()
bootstrap = Bootstrap()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DATABASE=DB_NAME,
        MYSQL_HOST=DB_HOST,
        #BOOTSTRAP_SERVE_LOCAL=BOOTSTRAP_SERVE_LOCAL
    )
    
    cloudinary.config(
       cloud_name=CLOUD_NAME,
       api_key=API_KEY,
       api_secret=API_SECRET,
       secure=True,
    )

    bootstrap.init_app(app)
    mysql.init_app(app)
    CSRFProtect(app)

    @app.route('/')
    def home():
        return render_template("home.html")

    from app.college.controller import college_bp
    from app.course.controller import course_bp
    from app.student.controller import student_bp
    
    app.register_blueprint(college_bp, url_prefix='/college/')
    app.register_blueprint(course_bp, url_prefix='/course/')
    app.register_blueprint(student_bp, url_prefix='/student/')

    return app