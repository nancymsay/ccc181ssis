from app import mysql

class Course(object):

    def add(self):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT courseCode FROM course WHERE courseCode = %s"
        cursor.execute(check_duplicate_sql, (self.courseCode,))
        existing_course = cursor.fetchone()

        if existing_course:
            return False

        sql = "INSERT INTO course(courseCode, courseName, collegeCode) VALUES(%s, %s, %s)"
        cursor.execute(sql, (self.courseCode, self.courseName , self.collegeCode))
        mysql.connection.commit()
	
        return True

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM course"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
	
    @classmethod
    def delete(cls, id):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE FROM course WHERE id = {id}"
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except:
            return False
    
    @classmethod
    def update(cls, courseCode, courseName, collegeCode, originalCode):
        cursor = mysql.connection.cursor()
        #check duplicate
        sql = "UPDATE course SET courseCode = %s, courseName = %s, collegeCode = %s WHERE courseCode = %s"
        cursor.execute(sql, (courseCode, courseName, collegeCode, originalCode))
        mysql.connection.commit()
    

    @classmethod
    def search(cls, searchCourse):
        search_query = "%" + searchCourse + "%"
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM course WHERE courseCode LIKE %s OR courseName LIKE %s OR collegeCode LIKE %s"
        cursor.execute(sql, (search_query, search_query, search_query))
        result = cursor.fetchall()
        return result
    
    
    @classmethod
    def get_college_codes(cls):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT collegeCode FROM college"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    
