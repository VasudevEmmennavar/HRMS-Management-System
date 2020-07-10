from flask import Flask,  render_template, request, flash
import mysql.connector

mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      database="newtest"
    )
mycursor = mydb.cursor()


app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

@app.route('/')
def index():
    return render_template('atten.html')


@app.route('/hi', methods=["POST"])
def getvalue():
    ab = request.form['e_id']
    cd = request.form['Date']
    ef = request.form['Punch_In']
    gh = request.form['Punch_Out']

          
    sql = "INSERT INTO `attendance`(`e_id`, `Date`, `Punch_In`, `Punch_Out`) VALUES (%s, %s, %s, %s)"
    val = (ab, cd, ef, gh)

    
    mycursor.execute(sql, val)
    #insert(ab, cd, ef, gh)
    mydb.commit()

    
    sql= "SELECT `e_id` FROM `attendance` WHERE `e_id` = " + str(ab)
    mycursor.execute(sql)
    e_id_from_db =  mycursor.fetchone()
    #mydb.commit()

    if (request.form['e_id'] == str(e_id_from_db[0])):
        flash("Successfully updated")
        mycursor.execute("UPDATE `attendance` SET `Punch_hours`=(`Punch_Out` - `Punch_In`) WHERE (`Date` = CURDATE() )")
        mydb.commit()
        #return render_template('atten.html')
    else:
        flash("Failed to update")

        
    return render_template('atten.html')

if __name__ == "__main__":
    app.run(debug=True)
