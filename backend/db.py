import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="placement_user",
        password="placement@123",
        database="student_placement_db"
    )
