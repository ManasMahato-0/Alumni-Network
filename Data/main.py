from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float,func
from sqlalchemy.exc import IntegrityError
from flask import jsonify
import base64
from My_Package import email
app=Flask(__name__)
class Base(DeclarativeBase):
    pass
mail=email.Mail()
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///user_data.db"
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png"]
app.config["UPLOAD_PATH"] = "image_uploads"
app.jinja_env.filters['decode'] = base64.b64decode
db = SQLAlchemy(model_class=Base)
db.init_app(app)
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    First_Name: Mapped[str] = mapped_column(String(250), nullable=False)
    Last_Name: Mapped[str] = mapped_column(String(250), nullable=False)
    Email: Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    Password:Mapped[str]=mapped_column(String(250),nullable=False)
    Confirm_Password:Mapped[str]=mapped_column(String(250),nullable=False)
    Branch:Mapped[str] = mapped_column(String(250),nullable=False)
    Status:Mapped[str] = mapped_column(String(250),nullable=False)
    Current_Company:Mapped[str] = mapped_column(String(250),nullable=False)
    Current_Working_Position:Mapped[str] = mapped_column(String(250),unique=False,nullable=False)
    Image:Mapped[str] = mapped_column(String(100000),nullable=False)
    def to_dict(self):
        #Method 1. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
        
        #Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()
@app.route('/')
def home():
    return render_template('index.html',var=False) 
@app.route('/login')
def logs():
    return render_template('index4.html')
@app.route('/loginform')
def login():
    return render_template('login.html')
@app.route('/signup',methods=['GET','POST'])
def done():
    global fname
    global lname
    fname=request.form["firstname"].title()
    lname=request.form["lastname"].title()
    email=request.form["email"]
    password=request.form["password"]
    conpassword=request.form["conpassword"]
    status=request.form["status"]
    branch=request.form["branch"]
    company=request.form["company"]
    position=request.form["position"]
    file=request.files["pic"]
    if password==conpassword:
        image_content = file.read()
            # Encode the bytes-like object as a base64 string
        image_64_encode = base64.b64encode(image_content).decode()
        try:
            with app.app_context():
                new_user = User(First_Name=f"{fname}",Last_Name=f"{lname}",Status=f"{status}",Email=f"{email}",Password=f"{password}",Confirm_Password=f"{conpassword}",Branch=f"{branch}",Current_Company=f"{company}",Current_Working_Position=f"{position}",Image=f"{image_64_encode}")
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            return f"<h1 style='color:red'>Email Unique Consraint failed</h1>"
        return render_template('login.html')
    else:
        return f"<h1 style='color:red'>Password Fields dont match</h1>"
@app.route('/login/successful',methods=['GET','POST'])
def loggedin():
    email=request.form["email"]
    password=request.form["password"]
    var=False
    result = db.session.execute(db.select(User).order_by(User.First_Name))
    all_users=result.scalars()
    global firstnames
    for user in all_users:
        Demail=user.Email
        Dpassword=user.Password
        # firstnames=firstnames+user.First_Name
        if Demail==email and Dpassword==password:
            var=True
            name=user.First_Name
            status=user.Status
    if var==True and status=="Student":
        return render_template('indexuser.html',var=True,name=name)
    elif var==True and status=="Admin":
        return render_template('index.html',var=True,name=name)
    elif var==True and status=="Alumni":
        return render_template('indexalumni.html',var=True,name=name)
    
    else:
        return render_template('login.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/searchuser',methods=['GET','POST'])
def searchuser():
    user_id = request.form['searchuser'].lower().strip()

    # Retrieve users with matching first name (case-insensitive)
    global matching_users
    matching_users=[]
    if request.form["filter"]=='Name':
        users = User.query.filter(func.lower(User.First_Name) == user_id).all()
    elif request.form["filter"]=='Company':
        users = User.query.filter(func.lower(User.Current_Company) == user_id).all()
    for user in users:
        matching_users.append(user.to_dict())

    if matching_users:
        return render_template('namecard.html',users=matching_users,var=True,name=user_id)
    else:
        return render_template('namecard.html',var=False,name=user_id)
@app.route('/searchuserbrother',methods=['GET','POST'])
def search():
    user_id = request.form['searchuser'].lower().strip()

    # Retrieve users with matching first name (case-insensitive)
    global matching_users
    matching_users=[]
    users = User.query.filter(func.lower(User.First_Name) == user_id).all()
    for user in users:
        matching_users.append(user.to_dict())

    if matching_users:
        return render_template('namecard.html',users=matching_users,var=True,name=user_id)
    else:
        return render_template('namecard.html',var=False,name=user_id)
@app.route('/connectbrodcast')
def brodcast():
    return render_template('brodcast.html')
@app.route('/sendmail',methods=['GET','POST'])
def send_mail():
    email=request.form["email"]
    message=request.form["message"]
    picture=request.form['pic']
    mail.send_to_mail(email=email,message=message,image_path=r"C:\Users\hgp99\OneDrive\Desktop\HAckathon\8.png")
    return f"<h1>Send email successfully</h1>"
@app.route('/connect')
def connect():
    return render_template('connect.html')
@app.route('/send/all',methods=['GET','POST'])
def send_all_mail():
    result = db.session.execute(db.select(User).order_by(User.First_Name))
    message=request.form["message"]
    users=result.scalars()
    mail.send_to_all(message=message,data=users)
    return f"<h1>Send email successfully to all</h1>"
def get_user_by_id(user_id):
    for user in matching_users:
        if user['id'] == user_id:
            return user
    return None  # Return None if no user with the specified ID is found
@app.route('/viewprofile',methods=['GET','POST'])
def viewprofile():
    return render_template('profile.html',data=matching_users)
@app.route('/mentor')
def mentor():
    return render_template('Mentorship.html')
@app.route('/request/mentorship')
def requestmentor():
    return render_template('indexRequestMentorship.html')
if __name__=="__main__":
    app.run(debug=True)