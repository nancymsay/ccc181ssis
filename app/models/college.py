from app import mysql

class College(object):

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
        cursor = mysql.connection.cursor()

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
