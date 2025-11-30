from flask import Flask, jsonify, request, session, redirect, render_template
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



#log in & process


@app.route("/")
def process_logout():
  session.clear()
  return render_template('landingpage.html')

@app.route("/logout")
def plogout():
  session.clear()
  return render_template('logout.html')

@app.route("/process-login", methods=['POST'])
def process_login():
    username = request.form.get('username')
    password = request.form.get('password')

    cursor.execute('''SELECT * 
                      FROM `person` 
                      WHERE `username` = %s 
                        AND `password` = %s''', (username, password))
    record = cursor.fetchone()

    if record:
        session['personId'] = record['personId']
        session['role'] = record['role']
        session['fname'] = record['fname']
        session['profilePic'] = record.get('profilePic', 'catto-2.webp')   
        return redirect("/dashboard")
    else:
        return redirect("/signup")

@app.route("/login")
def show_login_page():
  return render_template("login.html")






#dashboard
from datetime import datetime

@app.route("/dashboard")
def dashboard():
    personId = session.get("personId")  
    role = session.get("role", 1)
    if not personId:
        return redirect("/")   

    # Fetch last 10 mood entries for the current month
    cursor.execute('''
        SELECT entryDate, moodName
        FROM `person-mood`
        WHERE personId = %s
          AND MONTH(entryDate) = MONTH(CURDATE())
          AND YEAR(entryDate) = YEAR(CURDATE())
        ORDER BY entryDate DESC
        LIMIT 10
    ''', (personId,))
    monthly_mood = cursor.fetchall() or []

    # Format current date  
    now = datetime.now()
    current_date = now.strftime("%d %b %Y, %I:%M %p")   

    return render_template(
        "dashboard.html",
        monthly_mood=monthly_mood,
        role=role,
        current_date=current_date
    )







# insert user records / signup records


@app.route("/signup")
def show_signup_page():
  return render_template("signup.html")


@app.route("/insert-form")
def insert():
    role = session['role']
    return render_template("form.html", role=role)

@app.route("/submit-insert-form", methods=['POST'])
def submit_insertform():
        if request.method == 'POST':

          fname = request.form.get('fname')
          lname = request.form.get('lname')
          username = request.form.get('username')
          password = request.form.get('password')
          DOB = request.form.get('DOB')
          role = request.form.get('role')

          cursor.execute('''
    INSERT INTO `person` (personId, fname, lname, username, password, DOB, role)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', ('NULL',fname, lname, username, password, DOB, role))

          conn.commit()


          data = {
            "fname": fname,
            "lname": lname,
            "username": username,
            "password": password,
            "DOB": DOB,
            "role": role
          }

          return render_template("submit-form.html", **data)
        
@app.route('/upload-file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
      file = request.files['profilePic']
      filepath = os.path.join('static/images', file.filename) 
      
      file.save(filepath)

      data = {
        "filepath": file.filename
      }

    return render_template('file-uploaded.html', **data)





 
# Admin User Management
 

@app.route("/admin")
def admin():
    role = session.get("role")
    if role != 2:
        return "Stop hacking"
    cursor.execute("SELECT * FROM person")
    rows = cursor.fetchall()
    fname = session.get("fname", "Not logged in")
    return render_template("admin.html", rows=rows, fname=fname)

@app.route("/edit/<personId>")
def edit(personId):
    cursor.execute("SELECT * FROM person WHERE personId=%s", (personId,))
    row = cursor.fetchone()
    return render_template("edit.html", row=row)

@app.route("/confirm-edit", methods=["POST"])
def confirm_edit():
    personId = request.form.get("personId")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    dob = request.form.get("DOB")
    cursor.execute("""
        UPDATE person
        SET fname=%s, lname=%s, DOB=%s
        WHERE personId=%s
    """, (fname, lname, dob, personId))
    conn.commit()
    return render_template("confirm-edit.html")

@app.route("/delete/<personId>")
def delete(personId):
    cursor.execute("SELECT * FROM person WHERE personId=%s", (personId,))
    row = cursor.fetchone()
    return render_template("delete.html", row=row)

@app.route("/confirm-delete", methods=["POST"])
def confirm_delete():
    personId = request.form.get("personId")
    cursor.execute("DELETE FROM person WHERE personId=%s", (personId,))
    conn.commit()
    return render_template("confirm-delete.html")

 






# Admin Diary Management
 

@app.route("/adminA")
def adminpagea():
    role = session.get("role")
    if role != 2:
        return "Stop hacking"
    
    cursor.execute("SELECT * FROM `person-mood` ORDER BY entryDate DESC")
    rows = cursor.fetchall()

    return render_template("adminA.html", rows=rows)

@app.route("/editA/<entryID>")
def editA(entryID):
    cursor.execute("SELECT * FROM `person-mood` WHERE entryID=%s", (entryID,))
    row = cursor.fetchone()
    return render_template("editA.html", entry=row)

@app.route("/confirm-editA", methods=["POST"])
def confirm_editA():
    entryID = request.form.get("entryID")
    fname = request.form.get("fname")
    moodName = request.form.get("moodName")
    entryDate = request.form.get("entryDate")
    diaryEntry = request.form.get("diaryEntry")
    cursor.execute("""
        UPDATE `person-mood`
        SET fname=%s, moodName=%s, entryDate=%s, diaryEntry=%s
        WHERE entryID=%s
    """, (fname, moodName, entryDate, diaryEntry, entryID))
    conn.commit()
    return render_template("confirm-editA.html")

@app.route("/deleteA/<entryID>")
def deleteA(entryID):
    cursor.execute("SELECT * FROM `person-mood` WHERE entryID=%s", (entryID,))
    row = cursor.fetchone()
    return render_template("deleteA.html", entry=row)

@app.route("/confirm-deleteA", methods=["POST"])
def confirm_deleteA():
    entryID = request.form.get("entryID")
    cursor.execute("DELETE FROM `person-mood` WHERE entryID=%s", (entryID,))
    conn.commit()
    return render_template("confirm-deleteA.html")

@app.route("/insert-formA")
def insert_formA():
    role = session.get("role")
    if role != 2:
        return "Stop hacking"
    return render_template("formA.html")

@app.route("/submit-insert-formA", methods=["POST"])
def submit_insertformA():
    fname = request.form.get("fname")
    moodName = request.form.get("moodName")
    entryDate = request.form.get("entryDate")
    diaryEntry = request.form.get("diaryEntry")
    cursor.execute("""
        INSERT INTO `person-mood` (fname, moodName, entryDate, diaryEntry)
        VALUES (%s,%s,%s,%s)
    """, (fname, moodName, entryDate, diaryEntry))
    conn.commit()
    return render_template("submit-formA.html")

      






#settings 


@app.route("/settings", methods=['GET', 'POST'])
def settings():
    if "personId" not in session:
        return redirect("/")

    personId = session['personId']

    cursor.execute("SELECT * FROM person WHERE personId=%s", (personId,))
    user = cursor.fetchone()

    if request.method == "POST":
        if "fname" in request.form:  
            fname = request.form['fname']
            lname = request.form['lname']
            profilePic = request.form['profilePic']

            cursor.execute('''UPDATE person 
                              SET fname=%s, lname=%s, profilePic=%s 
                              WHERE personId=%s''', (fname, lname, profilePic, personId))
            conn.commit()
            session['fname'] = fname
            return redirect("/settings")

        elif "current_password" in request.form:  
            current_password = request.form['current_password']
            new_password = request.form['new_password']

            if user['password'] != current_password:
                return "Current password is incorrect"
            else:
                cursor.execute('''UPDATE person 
                                  SET password=%s 
                                  WHERE personId=%s''', (new_password, personId))
                conn.commit()
                return redirect("/settings")

    return render_template("settings.html", user=user)







#creatinng diary entries

@app.route("/createentry")
def show_create_entry():
    if "personId" not in session:
        return redirect("/")  
    return render_template("createentry.html") 

@app.route("/submit-diary", methods=['POST'])
def submit_diary():
    if "personId" not in session:
        return "Not logged in", 403

    personId = session['personId']
    fname = session.get('fname', '')
    diaryEntry = request.form.get('diaryEntry')
    entryDate = request.form.get('entryDate')
    moodName = request.form.get('moodName')

    cursor.execute('''
        INSERT INTO `person-mood` (personId, fname, moodName, entryDate, diaryEntry)
        VALUES (%s, %s, %s, %s, %s)
    ''', (personId, fname, moodName, entryDate, diaryEntry))
    conn.commit()

    return redirect("/dashboard")




#mood summary

@app.route("/moodsummary")
def mood_summary():

    personId = session.get('personId')  
    if not personId:
        return redirect('/')  

   
    cursor.execute('''
        SELECT moodName, COUNT(*) AS count
        FROM `person-mood`
        WHERE personId = %s AND MONTH(entryDate) = MONTH(CURDATE())
        GROUP BY moodName
    ''', (personId,))
    mood_counts = cursor.fetchall()  


    highest_count = 0
    dominant_mood = None
    for mood in mood_counts:
        if mood['count'] > highest_count:
            highest_count = mood['count']
            dominant_mood = mood['moodName']


    summary_message = "Your mood summary for this month:"
    if dominant_mood == 'Happy':
        summary_message = "You were a happy bunny this month!"
    elif dominant_mood == 'Sad':
        summary_message = "There were some sad days this month."
    elif dominant_mood == 'Angry':
        summary_message = "You had an angry streak this month."
    elif dominant_mood == 'Neutral':
        summary_message = "Mostly neutral mood this month."

    return render_template("moodsummary.html", mood_counts=mood_counts, summary_message=summary_message)





#search entries

@app.route("/search-records")
def search_records():
    rows = []
    return render_template("search-records.html", rows=rows)

@app.route("/search-results", methods=['POST'])
def search_results():
    diaryEntry = request.form['diaryEntry']
    cursor.execute("SELECT entryID, diaryEntry, moodName, entryDate " \
    "FROM `person-mood` " \
    "WHERE diaryEntry LIKE %s", ("%" + diaryEntry + "%",))
    results = cursor.fetchall()
    return render_template("search-results.html", results=results)

@app.route("/all-entries")
def all_entries():
    cursor.execute("SELECT entryID, diaryEntry, moodName, entryDate " \
    "FROM `person-mood`")
    rows = cursor.fetchall()
    return render_template("search-records.html", rows=rows)


#zim diary
@app.route("/zimdiary")
def zimdiary():
    return render_template("zimdiary.html")


#ajax

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="personnapp"
    )

@app.route('/add-prediction', methods=['POST'])
def add_prediction():
    
    data = request.get_json()  # read JSON sent from the form

    predictions = data.get('predictions')
    spirit = data.get('spirit')

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    cursor = conn.cursor()

    sql = "INSERT INTO prediction (predictions, spirit) VALUES (%s, %s)"
    values = (predictions, spirit)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"status": "success", "id": cursor.lastrowid})

@app.route("/predictions")
def get_predictions():
    predictions = [
        {"predictionID": 1, "predictions": "A joyful surprise awaits you.", "spirit": "Joy"},
        {"predictionID": 2, "predictions": "Be cautious in your choices today.", "spirit": "Caution"},
        {"predictionID": 3, "predictions": "You will make someone smile.", "spirit": "Smile"},
        {"predictionID": 4, "predictions": "A small challenge will teach you a lot.", "spirit": "Challenge"},
        {"predictionID": 5, "predictions": "Someone appreciates your efforts.", "spirit": "Gratitude"},
        {"predictionID": 6, "predictions": "A new opportunity is coming.", "spirit": "Hope"},
        {"predictionID": 7, "predictions": "Take time to relax and breathe.", "spirit": "Calm"},
        {"predictionID": 8, "predictions": "An old friend may reach out.", "spirit": "Connection"},
        {"predictionID": 9, "predictions": "Trust your instincts today.", "spirit": "Trust"},
        {"predictionID": 10, "predictions": "A small act of kindness will make a difference.", "spirit": "Kindness"},
        {"predictionID": 11, "predictions": "Your hard work will pay off soon.", "spirit": "Motivation"},
        {"predictionID": 12, "predictions": "Embrace change with an open mind.", "spirit": "Adaptability"},
        {"predictionID": 13, "predictions": "A creative idea will come to you.", "spirit": "Creativity"},
        {"predictionID": 14, "predictions": "You will learn something new today.", "spirit": "Curiosity"},
        {"predictionID": 15, "predictions": "Someone will make you laugh.", "spirit": "Joy"},
        {"predictionID": 16, "predictions": "Stay focused on your priorities.", "spirit": "Focus"},
        {"predictionID": 17, "predictions": "Your patience will be rewarded.", "spirit": "Patience"},
        {"predictionID": 18, "predictions": "Take a small step toward a big goal.", "spirit": "Progress"},
        {"predictionID": 19, "predictions": "A compliment will brighten your day.", "spirit": "Happiness"},
        {"predictionID": 20, "predictions": "Someone needs your support.", "spirit": "Compassion"},
        {"predictionID": 21, "predictions": "A positive change is coming.", "spirit": "Optimism"},
        {"predictionID": 22, "predictions": "You will find clarity in a decision.", "spirit": "Wisdom"},
        {"predictionID": 23, "predictions": "An unexpected gift will appear.", "spirit": "Surprise"},
        {"predictionID": 24, "predictions": "Your courage will inspire someone.", "spirit": "Courage"},
        {"predictionID": 25, "predictions": "A small victory will make you proud.", "spirit": "Achievement"},
        {"predictionID": 26, "predictions": "Take time to reflect on your goals.", "spirit": "Reflection"},
        {"predictionID": 27, "predictions": "You will receive helpful advice.", "spirit": "Guidance"},
        {"predictionID": 28, "predictions": "A kind gesture will return to you.", "spirit": "Reciprocity"},
        {"predictionID": 29, "predictions": "Trust the journey, not just the outcome.", "spirit": "Trust"},
        {"predictionID": 30, "predictions": "Someone will notice your efforts.", "spirit": "Recognition"},
        {"predictionID": 31, "predictions": "Stay optimistic during challenges.", "spirit": "Positivity"},
        {"predictionID": 32, "predictions": "A moment of clarity will guide you.", "spirit": "Insight"},
        {"predictionID": 33, "predictions": "Your creativity will be appreciated.", "spirit": "Creativity"},
        {"predictionID": 34, "predictions": "You will make a meaningful connection.", "spirit": "Connection"},
        {"predictionID": 35, "predictions": "A new perspective will help you solve a problem.", "spirit": "Wisdom"},
        {"predictionID": 36, "predictions": "Someone will bring joy to your day.", "spirit": "Joy"},
        {"predictionID": 37, "predictions": "Your effort in learning will pay off.", "spirit": "Motivation"},
        {"predictionID": 38, "predictions": "Take a chance on something new.", "spirit": "Courage"},
        {"predictionID": 39, "predictions": "A positive interaction will uplift your mood.", "spirit": "Happiness"},
        {"predictionID": 40, "predictions": "You will discover a hidden talent.", "spirit": "Discovery"},
        {"predictionID": 41, "predictions": "Someone will express gratitude to you.", "spirit": "Gratitude"},
        {"predictionID": 42, "predictions": "A small decision will have a big impact.", "spirit": "Wisdom"},
        {"predictionID": 43, "predictions": "Stay kind even when it's hard.", "spirit": "Compassion"},
        {"predictionID": 44, "predictions": "An exciting opportunity is on the horizon.", "spirit": "Hope"},
        {"predictionID": 45, "predictions": "Take time to enjoy simple pleasures.", "spirit": "Calm"},
        {"predictionID": 46, "predictions": "Your patience will inspire someone else.", "spirit": "Patience"},
        {"predictionID": 47, "predictions": "A positive habit will bring benefits.", "spirit": "Growth"},
        {"predictionID": 48, "predictions": "Someone will seek your advice.", "spirit": "Guidance"},
        {"predictionID": 49, "predictions": "Celebrate small wins today.", "spirit": "Achievement"},
        {"predictionID": 50, "predictions": "A meaningful conversation is coming.", "spirit": "Connection"}


    ]
    return jsonify(predictions)

@app.route("/jsevents")
def home():
    return render_template("jsevents.html")


@app.route("/moodspace")
def get_mood_space():
    return jsonify([
        {"word": "Serenity", "clue": "A state of being calm and peaceful"},
        {"word": "Joy", "clue": "A feeling of great happiness"},
        {"word": "Courage", "clue": "The ability to face fear or difficulty"},
        {"word": "Gratitude", "clue": "Feeling thankful and appreciative"},
        {"word": "Hope", "clue": "A feeling of expectation and desire"},
        {"word": "Peace", "clue": "Freedom from disturbance"},
        {"word": "Patience", "clue": "Ability to wait calmly"},
        {"word": "Compassion", "clue": "Sympathy for others' suffering"},
        {"word": "Inspiration", "clue": "Something that motivates you"},
        {"word": "Resilience", "clue": "Ability to recover quickly"},
        {"word": "Kindness", "clue": "Being friendly and considerate"},
        {"word": "Mindfulness", "clue": "Awareness of the present moment"},
        {"word": "Balance", "clue": "A state of stability and harmony"},
        {"word": "Empathy", "clue": "Understanding another person's feelings"},
        {"word": "Confidence", "clue": "Belief in oneself"},
        {"word": "Curiosity", "clue": "A strong desire to learn"},
        {"word": "Determination", "clue": "Firmness of purpose"},
        {"word": "Optimism", "clue": "Hopefulness about the future"},
        {"word": "Reflection", "clue": "Careful thought about the past"},
        {"word": "Forgiveness", "clue": "Letting go of resentment"},
        {"word": "Creativity", "clue": "Using imagination to create"},
        {"word": "Motivation", "clue": "Reason for taking action"},
        {"word": "Adventure", "clue": "Exciting or unusual experience"},
        {"word": "Strength", "clue": "The quality of being strong"},
        {"word": "Freedom", "clue": "The power to act or speak freely"},
        {"word": "Trust", "clue": "Reliance on the integrity of someone"},
        {"word": "Passion", "clue": "Strong enthusiasm or emotion"},
        {"word": "Harmony", "clue": "Agreement or peace between elements"},
        {"word": "Focus", "clue": "Concentration on a goal"},
        {"word": "Clarity", "clue": "Being clear and easy to understand"},
        {"word": "Giggle", "clue": "A light, silly laugh"},
        {"word": "Bubble", "clue": "Round, floating, and fun"},
        {"word": "Pixel", "clue": "Tiny dot on a screen"},
        {"word": "Robot", "clue": "A machine that can move or think"},
        {"word": "Cupcake", "clue": "Small, sweet treat in a paper cup"},
        {"word": "Rainbow", "clue": "Colors in the sky after rain"},
        {"word": "Slime", "clue": "Sticky, gooey, fun to squish"},
        {"word": "Joystick", "clue": "Controls your video game character"},
        {"word": "Noodle", "clue": "Twisty, slippery food"},
        {"word": "Sparkle", "clue": "Shiny, glittery shine"},
        {"word": "Alien", "clue": "A creature from outer space"},
        {"word": "Emoji", "clue": "Tiny picture to show feeling in messages"},
        {"word": "Puppy", "clue": "A young, playful dog"},
        {"word": "Banana", "clue": "Yellow fruit that monkeys love"},
        {"word": "Wizard", "clue": "Someone who can do magic"},
        {"word": "Dragon", "clue": "A mythical fire-breathing creature"},
        {"word": "Laptop", "clue": "Portable computer for work or play"},
        {"word": "Headphones", "clue": "Wear these to hear music privately"},
        {"word": "Candy", "clue": "Sweet treat for fun times"},
        {"word": "Rocket", "clue": "Shoots into space"},
        {"word": "Unicorn", "clue": "Magical horse with a horn"},
        {"word": "Meme", "clue": "Funny picture with text"},
        {"word": "Cheeseburger", "clue": "Juicy food with cheese on top"},
        {"word": "Joystick", "clue": "Helps you play video games"},
        {"word": "Marshmallow", "clue": "Soft, squishy treat for roasting"},
        {"word": "Tablet", "clue": "Touchscreen device for apps"},
        {"word": "Spaceship", "clue": "Vehicle to travel to the stars"},
        {"word": "Pencil", "clue": "Used for drawing or writing"},
        {"word": "Popcorn", "clue": "Fluffy snack for movies"},
        {"word": "Dragonfly", "clue": "Fast-flying insect with colorful wings"},
        {"word": "Socks", "clue": "Keep your feet warm"},
        {"word": "Keyboard", "clue": "Type letters to a computer"},
        {"word": "Cup", "clue": "Holds your drink"},
        {"word": "Icecream", "clue": "Cold, sweet dessert in a cone"},
        {"word": "Frog", "clue": "Jumps high and says ribbit"},
        {"word": "Pajamas", "clue": "Sleepy-time clothes"},
        {"word": "Drone", "clue": "Flies in the sky remotely"},
        {"word": "Spacesuit", "clue": "Protects astronauts in space"},
        {"word": "Taco", "clue": "Mexican food with fillings"},
        {"word": "Laptop", "clue": "Your portable work/play computer"},
        {"word": "Robot", "clue": "Automated machine buddy"},
        {"word": "Sloth", "clue": "Slow and sleepy animal"},
        {"word": "Hologram", "clue": "3D image in space"},
        {"word": "Rainbow", "clue": "Colors after the rain"},
        {"word": "Cheese", "clue": "Yummy dairy slice or block"},
        {"word": "Pogo", "clue": "Bounces up and down"},
        {"word": "Joystick", "clue": "Game controller lever"},
        {"word": "Laptop", "clue": "Portable device for tech fun"},
        {"word": "Cat", "clue": "Purrs and chases mice"},
        {"word": "Dog", "clue": "Barks and wags tail"},
        {"word": "Cookie", "clue": "Sweet baked snack"},
        {"word": "Cupcake", "clue": "Mini cake in a paper liner"},
        {"word": "Parrot", "clue": "Colorful bird that talks"},
        {"word": "Mouse", "clue": "Clicks on your computer screen"},
        {"word": "Headset", "clue": "Wear to hear music and talk"},
        {"word": "Tablet", "clue": "Screen device for drawing or reading"},
        {"word": "Moon", "clue": "Shines at night in the sky"},
        {"word": "Star", "clue": "Twinkles at night"},
        {"word": "Planet", "clue": "Orbits a star in space"},
        {"word": "Alien", "clue": "Comes from outer space"},
        {"word": "Spaceship", "clue": "Fly among planets and stars"},
        {"word": "Camera", "clue": "Captures photos"},
        {"word": "Microphone", "clue": "Lets you talk to everyone"},
        {"word": "Rocket", "clue": "Launches into the sky"},
        {"word": "Volcano", "clue": "Erupts hot lava"},
        {"word": "Treasure", "clue": "Hidden riches"},
        {"word": "Map", "clue": "Shows you directions"},
        {"word": "Compass", "clue": "Points you North"},
        {"word": "Potion", "clue": "Magic drink"},
        {"word": "Crown", "clue": "Royal headgear"},
        {"word": "Knight", "clue": "Brave fighter in armor"},
        {"word": "Castle", "clue": "Where kings and queens live"},
        {"word": "Wizard", "clue": "Casts spells"},
        {"word": "Fairy", "clue": "Tiny magical being"},
        {"word": "Mermaid", "clue": "Lives in the sea"},
        {"word": "Pirate", "clue": "Searches for treasure on the sea"},
        {"word": "Robot", "clue": "Mechanical helper"},
        {"word": "Alien", "clue": "From another planet"},
        {"word": "Spacesuit", "clue": "Protects you in space"},
        {"word": "Laptop", "clue": "Portable computer"},
        {"word": "Tablet", "clue": "Touchscreen gadget"},
        {"word": "Drone", "clue": "Flies by remote control"},
        {"word": "Joystick", "clue": "Game controller"},
        {"word": "Emoji", "clue": "Funny chat faces"},
        {"word": "Meme", "clue": "Funny internet picture"},
        {"word": "GIF", "clue": "Animated internet image"},
        {"word": "Streamer", "clue": "Person who broadcasts live video"},
        {"word": "Hashtag", "clue": "Used to tag posts online"},
        {"word": "Laptop", "clue": "Portable tech device"},
        {"word": "VR", "clue": "Virtual Reality headset fun"},
        {"word": "Robot", "clue": "Tech buddy that moves"}
    ])


@app.route("/show-moodspace")
def show_moodspace_page():
    return render_template("moodspace.html")





#CONTACT FORM

@app.route("/insert-contactform")
def insertcontactform():

    return render_template("settings.html")

@app.route("/submit-contactform", methods=['POST'])
def submit_contactform():
      if request.method == 'POST':    

          message = request.form.get('message')



          cursor.execute('''
    INSERT INTO `contactform` (submissionId, message)
    VALUES (%s, %s)
    ''', ('NULL', message))

          conn.commit()


          data = {
            "message": message,
          
          }

          return render_template("success.html", **data)