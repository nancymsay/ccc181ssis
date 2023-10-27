from app import mysql

class Student(object):
    
    def __init__(self, studentID=None, firstName=None, lastName=None, course=None, year=None, gender=None, college_code=None):
        self.studentID = studentID
        self.firstName = firstName
        self.lastName = lastName
        self.course = course
        self.year = year
        self.gender = gender
        self.college_code = college_code

    def add(self):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT studentID FROM student WHERE studentID = %s"
        cursor.execute(check_duplicate_sql, (self.studentID,))
        existing_student = cursor.fetchone()

        if existing_student:
            return False

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
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM student WHERE studentID = %s"
            cursor.execute(sql, (studentID,))
            mysql.connection.commit()
            return True
        except:
            return False
    
    @classmethod
    def update(cls, studentID, firstName, lastName, course, year, gender, originalCode):
        cursor = mysql.connection.cursor()
        sql = "UPDATE student SET studentID = %s, firstName = %s, lastName = %s, course = %s, year = %s, gender = %s WHERE studentID = %s"
        cursor.execute(sql, (studentID, firstName, lastName, course, year, gender, originalCode))
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