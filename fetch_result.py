import mysql.connector
from mysql.connector import Error
import pandas as pd
import numpy as np
import csv

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

        # Execute query
        sql = "SELECT * FROM examination.all_awards"
        cursor.execute(sql)
        # Fetch all the records
        result = cursor.fetchall()
        data_frame = pd.DataFrame(result , columns = ['branch_code','university_roll_no','subject_code','attendance_status','obtained_marks','max_marks','Int_Ext','umc_status','branch','credit','mcode','student_name','father_name']) 
        #print(data_frame)
        urns = data_frame['university_roll_no'].unique()
        subjectCodes = data_frame['subject_code'].unique()
        dictMarks = {}
        dictSubjectCode = {}
        dictMaxMarks = {}
        for urn in urns:
            dictMarks[urn] = []
            dictSubjectCode[urn] = []
            dictMaxMarks[urn] = []

        # map marks to urn
        for urn in urns:
            for subjectCode in subjectCodes:
                for row in data_frame.itertuples():
                    if row.university_roll_no == urn and row.subject_code == subjectCode:
                        dictSubjectCode[urn].append(subjectCode)
                        dictMarks[urn].append(row.obtained_marks)
                        dictMaxMarks[urn].append(row.max_marks)
       

        

        # Finding subject code have E in Int_Ext or not?
        dictHaveExt = {}
        for row in data_frame.itertuples():
            if row.Int_Ext == 'E' and row.subject_code not in dictHaveExt:
                dictHaveExt[row.subject_code] = True
        courseHavingExternal = list(dictHaveExt.keys())
        
        # failed subjects for each urn
        dictFailedSubjects = {}
        for urn in urns:
            dictFailedSubjects[urn] = []
            for subjectCode in dictSubjectCode[urn]:
                for row in data_frame.itertuples():
                    if row.university_roll_no == urn and row.subject_code == subjectCode and 100*(int(row.obtained_marks)/int(row.max_marks)) < 40:
                        dictFailedSubjects[urn].append(subjectCode)

        # Finding Grades for each urn and subject code
        dictGrades = {}
        dictObtainedMarksExt = {}
        dictMaxMarksExt = {}
        for urn in urns:
            dictGrades[urn] = {}
            for subjectCode in dictSubjectCode[urn]:
                if subjectCode in courseHavingExternal and subjectCode not in dictFailedSubjects[urn]:
                    for row in data_frame.itertuples():
                        # sum all the obtain marks having same subject code
                        if row.university_roll_no == urn and row.subject_code == subjectCode:
                            if subjectCode not in dictObtainedMarksExt:
                                dictObtainedMarksExt[subjectCode] = int(row.obtained_marks)
                                dictMaxMarksExt[subjectCode] = int(row.max_marks)
                            else:
                                dictObtainedMarksExt[subjectCode] += int(row.obtained_marks)
                                dictMaxMarksExt[subjectCode] += int(row.max_marks)
                    # find the grade for each subject code
                    if (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 >= 90 and (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 <= 100:
                        dictGrades[urn].update({subjectCode: 'O'})
                    elif (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 >= 80 and (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 < 90:
                        dictGrades[urn].update({subjectCode: 'A+'})
                    elif (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 >= 70 and (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 < 80:
                        dictGrades[urn].update({subjectCode: 'A'})
                    elif (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 >= 60 and (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 < 70:
                        dictGrades[urn].update({subjectCode: 'B+'})
                    elif (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 >= 50 and (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 < 60:
                        dictGrades[urn].update({subjectCode: 'B'})
                    elif (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 >= 45 and (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 < 50:
                        dictGrades[urn].update({subjectCode: 'C'})
                    elif (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 >= 40 and (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 < 45:
                        dictGrades[urn].update({subjectCode: 'D'})
                    elif (dictObtainedMarksExt[subjectCode]/dictMaxMarksExt[subjectCode])*100 < 40:
                        dictGrades[urn].update({subjectCode: 'F'})

                elif subjectCode not in courseHavingExternal and subjectCode not in dictFailedSubjects[urn]:
                    for row in data_frame.itertuples():
                        if row.university_roll_no == urn and row.subject_code == subjectCode:
                            if 100*(int(row.obtained_marks)/int(row.max_marks)) >= 90 and 100*(int(row.obtained_marks)/int(row.max_marks) )<= 100:
                                dictGrades[urn].update({subjectCode: 'O'})
                            elif 100*(int(row.obtained_marks)/int(row.max_marks)) >= 80 and 100*(int(row.obtained_marks)/int(row.max_marks)) <= 89:
                                dictGrades[urn].update({subjectCode: 'A+'})
                            elif 100*(int(row.obtained_marks)/int(row.max_marks)) >= 70 and 100*(int(row.obtained_marks)/int(row.max_marks)) <= 79:
                                dictGrades[urn].update({subjectCode: 'A'})
                            elif 100*(int(row.obtained_marks)/int(row.max_marks)) >= 60 and 100*(int(row.obtained_marks)/int(row.max_marks)) <= 69:
                                dictGrades[urn].update({subjectCode: 'B+'})
                            elif 100*(int(row.obtained_marks)/int(row.max_marks)) >= 50 and 100*(int(row.obtained_marks)/int(row.max_marks)) <= 59:
                                dictGrades[urn].update({subjectCode: 'B'})
                            elif 100*(int(row.obtained_marks)/int(row.max_marks)) >= 45 and 100*(int(row.obtained_marks)/int(row.max_marks)) <= 49:
                                dictGrades[urn].update({subjectCode: 'C'})
                            elif 100*(int(row.obtained_marks)/int(row.max_marks)) >= 40 and 100*(int(row.obtained_marks)/int(row.max_marks)) <= 44:
                                dictGrades[urn].update({subjectCode: 'P'})
                            elif 100*(int(row.obtained_marks)/int(row.max_marks)) >= 0 and 100*(int(row.obtained_marks)/int(row.max_marks)) <= 39:
                                dictGrades[urn].update({subjectCode: 'F'})
                elif subjectCode in dictFailedSubjects[urn]:
                    dictGrades[urn].update({subjectCode: 'Fail'})
        
        
        # map credit  for each subject code in each urn


        dictCredit = {}
        for urn in urns:
            dictCredit[urn] = {}
            for subjectCode in dictSubjectCode[urn]:
                for row in data_frame.itertuples():
                    if row.university_roll_no == urn and row.subject_code == subjectCode:
                        dictCredit[urn].update({subjectCode: row.credit})



        # Calculate total credit earned for each urn
        dictTotalCreditearned = {}
        for urn in urns:
            dictTotalCreditearned[urn] = 0
            for subjectCode in dictSubjectCode[urn]:
                if subjectCode in courseHavingExternal and subjectCode not in dictFailedSubjects[urn]:
                    dictTotalCreditearned[urn] += int(dictCredit[urn][subjectCode])
                elif subjectCode not in courseHavingExternal and subjectCode not in dictFailedSubjects[urn]:
                    dictTotalCreditearned[urn] += int(dictCredit[urn][subjectCode])
                elif subjectCode in dictFailedSubjects[urn]:
                    dictTotalCreditearned[urn] += 0
        # total credit for each urn
        dictTotalCredit = {}
        for urn in urns:
            dictTotalCredit[urn] = 0
            for subjectCode in dictSubjectCode[urn]:
                dictTotalCredit[urn] += int(dictCredit[urn][subjectCode])
        
                
        
        # Grade to grade point conversion
        dictGradePoint = {}
        for urn in urns:
            dictGradePoint[urn] = {}
            for subjectCode in dictSubjectCode[urn]:
                if subjectCode in courseHavingExternal and subjectCode not in dictFailedSubjects[urn]:
                    if dictGrades[urn][subjectCode] == 'O':
                        dictGradePoint[urn].update({subjectCode: 10})
                    elif dictGrades[urn][subjectCode] == 'A+':
                        dictGradePoint[urn].update({subjectCode: 9})
                    elif dictGrades[urn][subjectCode] == 'A':
                        dictGradePoint[urn].update({subjectCode: 8})
                    elif dictGrades[urn][subjectCode] == 'B+':
                        dictGradePoint[urn].update({subjectCode: 7})
                    elif dictGrades[urn][subjectCode] == 'B':
                        dictGradePoint[urn].update({subjectCode: 6})
                    elif dictGrades[urn][subjectCode] == 'C':
                        dictGradePoint[urn].update({subjectCode: 5})
                    elif dictGrades[urn][subjectCode] == 'D':
                        dictGradePoint[urn].update({subjectCode: 4})
                    elif dictGrades[urn][subjectCode] == 'F':
                        dictGradePoint[urn].update({subjectCode: 0})
                elif subjectCode not in courseHavingExternal and subjectCode not in dictFailedSubjects[urn]:
                    if dictGrades[urn][subjectCode] == 'O':
                        dictGradePoint[urn].update({subjectCode: 10})
                    elif dictGrades[urn][subjectCode] == 'A+':
                        dictGradePoint[urn].update({subjectCode: 9})
                    elif dictGrades[urn][subjectCode] == 'A':
                        dictGradePoint[urn].update({subjectCode: 8})
                    elif dictGrades[urn][subjectCode] == 'B+':
                        dictGradePoint[urn].update({subjectCode: 7})
                    elif dictGrades[urn][subjectCode] == 'B':
                        dictGradePoint[urn].update({subjectCode: 6})
                    elif dictGrades[urn][subjectCode] == 'C':
                        dictGradePoint[urn].update({subjectCode: 5})
                    elif dictGrades[urn][subjectCode] == 'D':
                        dictGradePoint[urn].update({subjectCode: 4})
                    elif dictGrades[urn][subjectCode] == 'F':
                        dictGradePoint[urn].update({subjectCode: 0})
                elif subjectCode in dictFailedSubjects[urn]:
                    dictGradePoint[urn].update({subjectCode: 0})

        # Calculate sgpa for each urn
        dictSgpa = {}
        for urn in urns:
            dictSgpa[urn] = 0
            for subjectCode in dictSubjectCode[urn]:
                if subjectCode in courseHavingExternal and subjectCode not in dictFailedSubjects[urn]:
                    dictSgpa[urn] += (int(dictCredit[urn][subjectCode]) * int(dictGradePoint[urn][subjectCode]))
                elif subjectCode not in courseHavingExternal and subjectCode not in dictFailedSubjects[urn]:
                    dictSgpa[urn] += (int(dictCredit[urn][subjectCode]) * int(dictGradePoint[urn][subjectCode]))
                elif subjectCode in dictFailedSubjects[urn]:
                    dictSgpa[urn] += 0
        for urn in urns:
            dictSgpa[urn] = dictSgpa[urn]/dictTotalCredit[urn]
    
        
        
        # map urn to banch_name
        dictBranch = {}
        for urn in urns:
            for row in data_frame.itertuples():
                if row.university_roll_no == urn:
                    dictBranch[urn] = row.branch

        #map student name to urn
        dictStudentName = {}
        for urn in urns:
            for row in data_frame.itertuples():
                if row.university_roll_no == urn:
                    dictStudentName[urn] = row.student_name
        # map urn to father name
        dictFatherName = {}
        for urn in urns:
            for rows in data_frame.itertuples():
                if rows.university_roll_no == urn:
                    dictFatherName[urn] = rows.father_name
        # result in the form of OE2-101 (A+) / PEC3-101 (B) / PEC3-102 / EL-11 (O) / MPD-104 (B) / EL-11 (A+)
        # subject_code + " /" + " (" + grade + ")"
        dictResult = {}
        for urn in urns:
            dictResult[urn] = {}
            for subjectCode in dictSubjectCode[urn]:
                if subjectCode in courseHavingExternal and subjectCode not in dictFailedSubjects[urn]:
                    dictResult[urn].update({subjectCode: subjectCode + " /" + " (" + dictGrades[urn][subjectCode] + ")"})
                elif subjectCode not in courseHavingExternal and subjectCode not in dictFailedSubjects[urn]:
                    dictResult[urn].update({subjectCode: subjectCode + " /" + " (" + dictGrades[urn][subjectCode] + ")"})
                elif subjectCode in dictFailedSubjects[urn]:
                    if subjectCode in courseHavingExternal:
                        dictResult[urn].update({subjectCode: subjectCode + " /" + " (" + "F_ext" + ")"})
                    elif subjectCode not in courseHavingExternal:
                        dictResult[urn].update({subjectCode: subjectCode + " /" + " (" + "Fail" + ")"})


        # export to csv file having branch_name,urn,s_name / f_name,result,sgpa,credit_earned,total_credit
        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Branch Name', 'University_roll_no' ,'Student Name','Fathers name','Result' , 'SGPA', 'Credit Earned', 'Total Credit'])
            for urn in urns:
                writer.writerow([dictBranch[urn], urn ,dictStudentName[urn],dictFatherName[urn],dictResult[urn].values(),round(dictSgpa[urn], 2), dictTotalCreditearned[urn], dictTotalCredit[urn]])
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        
