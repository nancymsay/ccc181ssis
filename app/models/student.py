from app import mysql

class Student(object):
    
    def __init__(self, studentID=None, firstName=None, lastName=None, course=None, year=None, gender=None):
        self.studentID = studentID
        self.firstName = firstName
        self.lastName = lastName
        self.course = course
        self.year = year
        self.gender = gender

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
        sql = "SELECT * FROM student"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
	
    @classmethod
    def delete(cls, id):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE FROM student WHERE id = {id}"
            cursor.execute(sql)
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
    def search(cls, searchStudent):
        search_query = "%" + searchStudent + "%"
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM student WHERE studentID LIKE %s OR firstName LIKE %s OR lastName LIKE %s OR course LIKE %s OR year LIKE %s OR gender LIKE %s"
        cursor.execute(sql, (search_query, search_query, search_query, search_query, search_query, search_query))
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
    
    
    
