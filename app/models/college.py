from app import mysql

class College(object):

    def __init__(self, collegeCode=None, collegeName=None):
        self.collegeCode = collegeCode
        self.collegeName = collegeName
        
            
    def add(self):
        cursor = mysql.connection.cursor()

        check_duplicate_sql = "SELECT collegeCode FROM college WHERE collegeCode = %s"
        cursor.execute(check_duplicate_sql, (self.collegeCode,))
        existing_college = cursor.fetchone()

        if existing_college:
            return False

        sql = "INSERT INTO college(collegeCode, collegeName) VALUES(%s, %s)"
        cursor.execute(sql, (self.collegeCode, self.collegeName))
        mysql.connection.commit()
	
        return True

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM college"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
	
    @classmethod
    def delete(cls, id):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE FROM college WHERE id = {id}"
            cursor.execute(sql)
            mysql.connection.commit()
            return True
        except:
            return False
        
    @classmethod
    def update(cls, collegeCode, collegeName, originalCode):
        cursor = mysql.connection.cursor()
        #check duplicate
        sql = "UPDATE college SET collegeCode = %s, collegeName = %s WHERE collegeCode = %s"
        cursor.execute(sql, (collegeCode, collegeName, originalCode))
        mysql.connection.commit()
        
    @classmethod
    def search(cls, searchCollege):
        search_query = "%" + searchCollege + "%"
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM college WHERE collegeCode LIKE %s OR collegeName LIKE %s"
        cursor.execute(sql, (search_query, search_query))
        result = cursor.fetchall()
        return result

    @classmethod
    def get_colleges(cls):
        cursor = mysql.connection.cursor(dictionary=True)
        sql = "SELECT * FROM college"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result