import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="newtest"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT `In_Time`FROM `attendance` WHERE (`Date` = CURDATE()) ")
in_tm = mycursor.fetchone()
a=str(in_tm[0])

mycursor.execute("SELECT `Out_Time`FROM `attendance` WHERE (`Date` = CURDATE())")
out_tm = mycursor.fetchone()
b=str(out_tm[0])


if b != "None"  :
    mycursor.execute("UPDATE `attendance` SET `Work_hours`=  (`Out_Time` - `In_Time`) + `Work_hours`  WHERE `Date` = CURDATE()")
    mydb.commit()
