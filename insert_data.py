import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='examination',
                                         user='root',
                                         password='admin')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        all_awards = pd.read_csv('all_awards.csv', index_col=False, delimiter = ',')
        all_awards.head()
        branch_code = pd.read_csv('branch_code.csv', index_col=False, delimiter = ',')
        branch_code.head()
        grades = pd.read_csv('grades.csv', index_col=False, delimiter = ',')
        grades.head()
        schema_data = pd.read_csv('schema_data.csv', index_col=False, delimiter = ',')
        schema_data.head()
        student_data = pd.read_csv('student_data.csv', index_col=False, delimiter = ',')
        student_data.head()

        for i,row in branch_code.iterrows():
            sql = """INSERT INTO examination.branch_code (branch_code,branch_name) VALUES (%s,%s)"""
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            connection.commit()
        print("Data updated successfully")
        
        for i,row in all_awards.iterrows():
            sql = """INSERT INTO examination.all_awards (branch_code,university_roll_no,subject_code,attendance_status,obtained_marks,max_marks,Int_Ext,umc_status,branch,credit,mcode,student_name,father_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            connection.commit()
        print("Data updated successfully")

        for i,row in schema_data.iterrows():
            sql = """INSERT INTO examination.schema_data (branch_code,subject_code,m_code,credit,theory_practical) VALUES (%s,%s,%s,%s,%s)"""
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            connection.commit()
        print("Data updated successfully")

        for i,row in student_data.iterrows():
            sql = """INSERT INTO examination.student_data(branch_code,university_roll_no,student_name,father_name) VALUES (%s,%s,%s,%s)"""
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            connection.commit()
        print("Data updated successfully")

        sql = "Update all_awards as a, branch_code as b SET a.branch = b.branch_name WHERE a.branch_code = b.branch_code";
        cursor.execute(sql)
        connection.commit()
        print("Data updated successfully")
        

        sql = "update all_awards as a , student_data as s set a.student_name = s.student_name ,a.father_name = s.father_name WHERE a.university_roll_no = s.university_roll_no";
        cursor.execute(sql)
        connection.commit()
        print("Data updated successfully")

        sql = "update all_awards as a , schema_data as s set a.mcode = s.m_code ,a.credit = s.credit WHERE a.subject_code = s.subject_code"
        cursor.execute(sql)
        connection.commit()
        print("Data updated successfully")
        
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


