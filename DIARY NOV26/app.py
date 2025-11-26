from flask import Flask, render_template, request, session, redirect
from dotenv import load_dotenv
import os
import mysql.connector

app = Flask(__name__) 

app.secret_key = os.getenv('SECRET_KEY')

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

conn = mysql.connector.connect(
host=app.config['MYSQL_HOST'],
user=app.config['MYSQL_USER'],
password=app.config['MYSQL_PASSWORD'],
database=app.config['MYSQL_DB']
)

cursor = conn.cursor(dictionary=True)

@app.route("/logout")
def process_logout():
  session.clear()
  return render_template('logout.html')

@app.route("/process-login", methods=['POST'])
def process_login():
  if request.method == 'POST':

    username = request.form.get('username')
    password = request.form.get('password')

    cursor.execute('''SELECT * 
                   FROM `person` 
                   WHERE `username` = %s 
                   AND `password`  =%s''', (username, password))

    record = cursor.fetchone()

    if(record):
      #start session
      session['personId'] = record['personId']
      session['role'] = record['role']
      session['fname'] = record['fname']

      #return render_template("logged-in.html", fname=session['fname'], role=session['role'],personId=session['personId'] )
      return redirect("/")

    else:
      return render_template("not-logged-in.html")


@app.route("/login")
def show_login_page():
  return render_template("login.html")

@app.route("/show-user-moods/<personId>")
def show_user_games(personId):
  cursor.execute('''SELECT * FROM `person-mood` 
                 INNER JOIN `mood` 
                 ON `mood`.`moodid` = `person-mood`.moodid
                 WHERE `personId`= %s;''', (personId,))

  rows = cursor.fetchall()
  print(rows)
  
  return render_template("user-moods.html", rows=rows)
  

@app.route("/confirm-edit", methods=['POST'])
def confirm_edit():
  if request.method == 'POST':

    personId = request.form.get('personId')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    dob = request.form.get('DOB')
    profilePic = request.form.get('profilePic')


    cursor.execute('''UPDATE `person` 
                   SET `fname` = %s, 
                   `lname` = %s, 
                   `DOB` = %s,
                   `profilePic` = %s,  
                   WHERE `person`.`personId` = %s;''', (fname, lname, dob, profilePic, personId))
    conn.commit()

  return render_template("confirm-edit.html")



@app.route("/edit/<personId>")
def edit(personId):

  cursor.execute('''SELECT * FROM `person` WHERE `personId` = %s''', (personId, ))

  rows = cursor.fetchone()
    
  return render_template("edit.html", personId=personId, rows=rows)



@app.route("/confirm-delete", methods=['POST'])
def confirm_delete():
  if request.method == 'POST':

    personId = request.form.get('personId')
    cursor.execute('''DELETE FROM person WHERE `person`.`personId` = %s''', (personId, ))
    conn.commit()

  return render_template("confirm-delete.html")



@app.route("/delete/<personId>")
def delete(personId):

  cursor.execute('''SELECT * FROM `person` WHERE `personId` = %s''', (personId, ))

  rows = cursor.fetchone()
  print(rows)

    
  return render_template("delete.html", personId=personId, rows=rows)




@app.route("/")
def landingpage():
  return render_template("landingpage.html")


@app.route("/list-records")
def records():
    
  cursor.execute('''SELECT * FROM `person`''')

  rows = cursor.fetchall()

  fname = 'Not logged in'

  if "fname" in session:
    fname = session['fname']
    
  return render_template("list-records.html", rows=rows, fname=fname)

@app.route("/createentry")
def createentry():
  return render_template("createentry.html")

@app.route("/moodsummary")
def moodsummary():
  return render_template("moodsummary.html")

@app.route("/settings")
def settings():
  return render_template("settings.html")

@app.route("/dashboard")
def dashboard():
  return render_template("dashboard.html")

@app.route("/signup")
def signup():
  return render_template("signup.html")

@app.route("/admin")
def admin():
    
  cursor.execute('''SELECT * FROM `personmood`''')

  rows = cursor.fetchall()

  fname = 'Not logged in'

  if "fname" in session:
    fname = session['fname']
    
  return render_template("admin.html", rows=rows, fname=fname)




@app.route("/zimdiary")
def zimdiary():
  return render_template("zimdiary.html")

@app.route("/insert-form")
def insert():
    role = session['role']
    return render_template("form.html", role=role)

@app.route("/submit-insert-form", methods=['POST'])
def submit_form():
    role = session['role']
    if(role != 2):
      return "Stop hacking"
    else:
      if request.method == 'POST':

          fname = request.form.get('fname')
          lname = request.form.get('lname')
          dob = request.form.get('DOB')
          profilePic = request.form.get('profilePic')

          cursor.execute('''
    INSERT INTO `Person` (personId, fname, lname, DOB, profilePic)
    VALUES (%s, %s, %s, %s, %s)
    ''', ('NULL',fname, lname, dob, profilePic))

          conn.commit()


          data = {
            "fname": fname,
            "lname": lname,
            "dob": dob,
            "profilePic": profilePic
          }

          return render_template("submit-form.html", **data)