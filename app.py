from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import INSERT
import INSERT_Values_DB
import In_Out_calculation

""" Get and Post using SQL Querries """
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="hrms"
)
mycursor = mydb.cursor()
mydb.commit()
app = Flask(__name__)
app.secret_key = "Happy!!!"

E_id = 1000133

#def employee_id(id):
#    E_id = id

    

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "You are logged in"

@app.route('/login', methods=['POST'])
def do_admin_login():
    if 'e_ID' not in do_admin_login.__dict__:
        do_admin_login.e_ID = 0
    do_admin_login.e_ID = request.form['username']
    sql = "SELECT `Password` FROM `Admin_login_creds` WHERE `e_ID` = " + str(do_admin_login.e_ID)
    mycursor.execute(sql)
    password_from_db = mycursor.fetchone()

    if password_from_db is None:
        flash("Wrong credentials!! ", "danger")
        flash(" Invalid username !!", "danger")
        return render_template('login.html')
    if (request.form['password'] == str(password_from_db[0])):
        session['logged_in'] = True
        return render_template('protected.html')
    else:
        flash("Wrong credentials!! ", "danger")
        flash(" Invalid password!!", "danger")
        return render_template('login.html')
  

@app.route('/logout')
def dropsession():
    session.clear()
    return render_template('login.html')
@app.route('/register')
def dropsession1():
    session.clear()
    return render_template('old_registration.html')
@app.route('/per_details')
def dropsession2():
    session.clear()
    return render_template('Personal_Details.html')
@app.route('/Home')
def dropsession3():
    session.clear()
    return render_template('protected.html')
@app.route('/Attend')
def dropsession4():
    session.clear()
    return render_template('atten.html')
    
@app.route('/dash')
def dropsession5():
    session.clear()
    return render_template('DashBoard.html')    

@app.route('/get_per_details')
def dropsession6():
    session.clear()
    return Get_per_details()    

@app.route('/org_details')
def dropsession7():
    session.clear()
    return Get_org_details()  

@app.route('/attend_details')
def dropsession8():
    session.clear()
    return Get_attend_details()      


@app.route('/insertReg', methods=['POST'])
def insertReg():
    if request.method == 'POST':
        eid = request.form['e_id']
        efname = request.form['e_fname']
        elname = request.form['e_lname']
        pemail = request.form['e_pemail']
        oemail = request.form['e_oemail']
        edep = request.form['e_dep']
        ephone = request.form['e_ph']
        edoj = request.form['e_doj']
        edes = request.form['e_des']
        repman = request.form['e_repman']
        x = INSERT.dup_check(eid)
        #print(len(x))

        if (len(x) != 0):
            flash("Eployee ID already exists", "error")
            return render_template('old_registration.html')
        else:
            INSERT.insert_entry(eid, efname, elname, pemail, oemail, edoj, edes, ephone, edep, repman)
            flash("Data store Successefully ", "error")
            return render_template('old_registration.html')

    else:
        return "Nothing"


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        ######
        eid = request.form['EID']
        gender = request.form['gender']
        BloodGrp = request.form["bldgrp"]
        Addr_Line_1 = request.form['Addr_Line_1']
        Addr_Line_2 = request.form['Addr_Line_2']
        City = request.form['City']
        State = request.form['State']
        PIN = request.form['PIN']
        x = INSERT_Values_DB.dup_check(eid)
        #print(x)
        if(x!=None):
            flash("Eployee ID Alerady exist", "error")
            return render_template('Personal_Details.html')

        else:
            INSERT_Values_DB.insertValues(eid, gender, BloodGrp, Addr_Line_1, Addr_Line_2, City, State, PIN)
            flash("Data store Successefully ", "error")
            return render_template('Personal_Details.html')
        ######
        #return render_template('protected.html')
    else:
        return "Nothing"


@app.route('/hi', methods=["POST"])
def getvalue():
    ab = request.form['e_id']
    cd = request.form['Date']
    ef = request.form['Punch_In']
    gh = request.form['Punch_Out']

    sql = "INSERT INTO `attendance`(`e_id`, `Date`, `Punch_In`, `Punch_Out`) VALUES (%s, %s, %s, %s)"
    val = (ab, cd, ef, gh)
    sql1 = "SELECT `e_id` FROM `attendance` WHERE `e_id` =" + str(ab)
    mycursor.execute(sql1)
    x = mycursor.fetchall()
    if(len(x) == 0):
        mycursor.execute(sql, val)
        # insert(ab, cd, ef, gh)
        mydb.commit()

        sql = "SELECT `e_id` FROM `attendance` WHERE `e_id` = " + str(ab)
        mycursor.execute(sql)
        e_id_from_db = mycursor.fetchone()
        # mydb.commit()

        if (request.form['e_id'] == str(e_id_from_db[0])):
            flash("Successfully updated")
            mycursor.execute("UPDATE `attendance` SET `Punch_hours`=(`Punch_Out` - `Punch_In`) WHERE (`Date` = CURDATE() )")
            mydb.commit()
            # return render_template('atten.html')
        else:
            flash("Failed to update")
    else:
        flash("Eployee ID Alerady exist", "error")
    return render_template('atten.html')
 
@app.route('/get_per_details', methods=['GET','POST'])
def Get_per_details():
 
  E_id = do_admin_login.e_ID
  sql_org = "SELECT * FROM `org_details` WHERE `e_id` = "+ str(E_id)
  print(E_id)
  #sql_per="SELECT * FROM `per_details` WHERE `e_id` = 1000160"
   
  sql_per = "SELECT * FROM `per_details` WHERE `e_id` = "+ str(E_id)
  print(E_id)
  #mycursor.execute(sql_per, (ID, '1000133'))
  mycursor.execute(sql_per)
  x=mycursor.fetchall()
  print(x)
  return render_template("Get_per_details.html", value = x)
    
@app.route('/get_org_details', methods=['GET','POST'])
def Get_org_details():

  E_id = do_admin_login.e_ID
  sql_org = "SELECT * FROM `org_details` WHERE `e_id` = "+ str(E_id)
  print(E_id)
  #sql_org = "SELECT  `e_id`,`First_Name`,`Last_Name`,`per_email`,`org_email`,`DOJ`,`desig_id`,`ph_num`,`depart_id`,`report_man` FROM `org_details` "
  mycursor.execute(sql_org)
  y=mycursor.fetchall()
  print(y)
  return render_template("Get_org_details.html", value = y)
    
    
@app.route('/get_attend_details', methods=['GET','POST'])
def Get_attend_details():

  E_id = do_admin_login.e_ID
  sql_attend = "SELECT * FROM `attendance` WHERE `e_id` = "+ str(E_id)
  print(E_id)
  #sql_attend = "SELECT  `e_id`,`RFID_num`,`Date`,`In_Time`,`Out_Time`,`Work_hours`,`Punch_In`,`Punch_Out`,`Punch_hours`,`locale` FROM ` attendance`"
  mycursor.execute(sql_attend)
  z=mycursor.fetchall()
  print(z)
  return render_template("Get_attend_details.html", value = z)
  
#In_Out_calculation.wrk_hrs_calc()
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
