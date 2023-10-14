from flask import Flask, render_template
from flask_mysql_connector import MySQL
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, BOOTSTRAP_SERVE_LOCAL
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
    bootstrap.init_app(app)
    mysql.init_app(app)
    CSRFProtect(app)

    @app.route('/')
    def student():
        return render_template("student.html")

    @app.route('/course')
    def course():
        return render_template("course.html")

    @app.route('/college')
    def college():
        return render_template("college.html")


    # from .user import user_bp as user_blueprint
    # app.register_blueprint(user_blueprint)


    return app