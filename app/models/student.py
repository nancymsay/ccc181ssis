from app import mysql

class Student(object):
    
    def __init__(self, studentID=None, firstName=None, lastName=None, course=None, year=None, gender=None, college_code=None, profilepic=None):
        self.studentID = studentID
        self.firstName = firstName
        self.lastName = lastName
        self.course = course
        self.year = year
        self.gender = gender
        self.college_code = college_code
        self.profilepic = profilepic

    def add(self):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT studentID FROM student WHERE studentID = %s"
        cursor.execute(check_duplicate_sql, (self.studentID,))
        existing_student = cursor.fetchone()

        if existing_student:
            return False

        # Check if a profile picture URL is provided
        if self.profilepic:
            sql = "INSERT INTO student(studentID, firstName, lastName, course, year, gender, profilepic) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.studentID, self.firstName, self.lastName, self.course, self.year, self.gender, self.profilepic))
        else:
            # If no profile picture, insert without the profilepic column
            sql = "INSERT INTO student(studentID, firstName, lastName, course, year, gender) VALUES(%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (self.studentID, self.firstName, self.lastName, self.course, self.year, self.gender))

        mysql.connection.commit()
        return True

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = """
        SELECT s.*, c.collegeCode as college_code 
        FROM student s
        INNER JOIN course c 
        ON s.course = c.courseCode
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
 
    @classmethod
    def delete(cls, studentID):
        try:
            # Get the profile picture URL before deleting the student
            profile_pic_url = cls.get_profile_pic_url(studentID)

            cursor = mysql.connection.cursor()
            sql = "DELETE FROM student WHERE studentID = %s"
            cursor.execute(sql, (studentID,))
            mysql.connection.commit()

            # If a profile picture exists, return the URL, otherwise, return None
            return profile_pic_url
        except:
            return None
    
    @classmethod
    def update(cls, studentID, firstName, lastName, course, year, gender, profilepic, originalCode):
        cursor = mysql.connection.cursor()
        sql = "UPDATE student SET studentID = %s, firstName = %s, lastName = %s, course = %s, year = %s, gender = %s, profilepic = %s WHERE studentID = %s"
        cursor.execute(sql, (studentID, firstName, lastName, course, year, gender, profilepic, originalCode))
        mysql.connection.commit()
    
    @classmethod
    def search(cls, search_category, search_query):
        search_query = "%" + search_query + "%"
        cursor = mysql.connection.cursor(dictionary=True)

        if search_category == 'all':
            sql = "SELECT s.*, c.collegeCode as college_code FROM student s INNER JOIN course c ON s.course = c.courseCode WHERE s.studentID LIKE %s OR s.firstName LIKE %s OR s.lastName LIKE %s OR s.course LIKE %s OR s.year LIKE %s OR s.gender LIKE %s OR c.collegeCode LIKE %s"
            cursor.execute(sql, (search_query, search_query, search_query, search_query, search_query, search_query, search_query))
        else:
            sql = f"SELECT s.*, c.collegeCode as college_code FROM student s INNER JOIN course c ON s.course = c.courseCode WHERE {search_category} LIKE %s"
            cursor.execute(sql, (search_query,))
        result = cursor.fetchall()
        return result
    
    @classmethod
    def get_course_codes(cls):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT courseCode FROM course"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    @classmethod
    def get_profile_pic_url(cls, studentID):
        cursor = mysql.connection.cursor()
        sql = "SELECT profilepic FROM student WHERE studentID = %s"
        cursor.execute(sql, (studentID,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            return None