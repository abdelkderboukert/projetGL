from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, json, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from waitress import serve
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, DateField, SelectField, TimeField
from wtforms.validators import DataRequired, equal_to, Length
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from flask_bcrypt import Bcrypt  # Import Bcrypt
from flask_login import UserMixin, login_user, login_manager, logout_user, login_required, current_user, login_remembered,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import datetime
from wtforms.widgets import TextArea
from flask_apscheduler import APScheduler
from flask_migrate import Migrate
from jinja2_time import TimeExtension
from validate_email import validate_email


app = Flask(__name__)
#csrf = CSRFProtect(app)
REMEMBER_COOKIE_DURATION = timedelta(days=0)
app.config['SECRET_KEY'] = '5511467d654732b6d9875da2691f78fd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///use.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Initialize Bcrypt
# flask_login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
scheduler = APScheduler()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.jinja_env.filters['datetime'] = datetime.datetime.strptime
#the module
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    infod = db.relationship('infod', backref='infod')
    info = db.relationship('info', backref='info')
    bro = db.Column(db.String(1), nullable=False, default=1)
    spi = db.Column(db.String(12), nullable=False, default='userr')
    wil = db.Column(db.String(2), nullable=False, default='userr') 
     

    @property
    def password(self):
        raise AttributeError('password is not a readable')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<name %r>' % self.name

class info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prename = db.Column(db.String(30), nullable=False, default='userr')
    datn = db.Column(db.String(30), nullable=False, default='userr')
    adresse = db.Column(db.String(30), nullable=False, default='userr')
    Ntph = db.Column(db.String(12), nullable=False, default='userr')
    text = db.Column(db.Text)

    def __repr__(self):
        return '<name %r>' % self.name

class infod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prename = db.Column(db.String(30), nullable=False, default='userr')
    datn = db.Column(db.String(30), nullable=False, default='userr')
    adresse = db.Column(db.String(30), nullable=False, default='userr')
    Ntph = db.Column(db.String(12), nullable=False, default='userr')
    text = db.Column(db.Text)


    def __repr__(self):
        return '<name %r>' % self.name

class rdv(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   date_to_do = db.Column(db.DateTime, nullable=False)
   text = db.Column(db.Text)
   drname = db.Column(db.String(50), nullable=False)
   drid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   ptid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   name = db.Column(db.String(50), nullable=False)
   prename = db.Column(db.String(50), nullable=False)
   ntph = db.Column(db.String(13), nullable=False)

#the forms
class userForm(FlaskForm):

    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password_hash = PasswordField("password", validators=[DataRequired(), equal_to('password_hash2', message='password must match!')])
    password_hash2 = PasswordField("password", validators=[DataRequired()]) 
    bro = SelectField(u'register as', choices=[
        (0, 'doctor'),
        (1, 'patient'),
    ], render_kw={"placeholder": "register as"}, validators=[DataRequired()])
    submit = SubmitField('creat a new account') 

class edit_userForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()], render_kw={"autocomplete": "name"})
    prename = StringField("prename", validators=[DataRequired()], render_kw={"autocomplete": "prename"})
    datn = StringField("date nisons", validators=[DataRequired()], render_kw={"autocomplete": "date nisons"})
    adresse = StringField("adresse", validators=[DataRequired()], render_kw={"autocomplete": "adresse"})
    Ntph = StringField("N° telephone", validators=[DataRequired()], render_kw={"autocomplete": "N° telephone"})
    email = StringField("email", validators=[DataRequired()], render_kw={"autocomplete": "email"})
    spi = SelectField(u'Choose a programming language', choices=[
        (1, ''),
        (2, 'Highest'),
        (3, 'Medium'),
        (4, 'Normal'),
        (5, ''),
        (6, 'Highest'),
        (7, 'Medium'),
        (8, 'Normal'),
    ], render_kw={"placeholder": "Choose a priority"}, validators=[DataRequired()])
    wil = SelectField(u'Choose a programming language', choices=[
        (1, ''),
        (2, 'Highest'),
        (3, 'Medium'),
        (4, 'Normal'),
        (5, ''),
        (6, 'Highest'),
        (7, 'Medium'),
        (8, 'Normal'),
        (9, ''),
        (10, 'Highest'),
        (11, 'Medium'),
        (12, 'Normal'),
        (13, ''),
        (14, 'Highest'),
        (15, 'Medium'),
        (16, 'Normal'),
        (17, ''),
        (18, 'Highest'),
        (19, 'Medium'),
        (20, 'Normal'),
        (21, ''),
        (22, 'Highest'),
        (23, 'Medium'),
        (24, 'Normal'),
        (25, ''),
        (26, 'Highest'),
        (27, 'Medium'),
        (28, 'Normal'),
        (29, ''),
        (30, 'Highest'),
        (31, 'Medium'),
        (32, 'Normal'),
        (33, ''),
        (34, 'Highest'),
        (35, 'Medium'),
        (36, 'Normal'),
        (37, ''),
        (38, 'Highest'),
        (39, 'Medium'),
        (40, 'Normal'),
        (41, ''),
        (42, 'Highest'),
        (43, 'Medium'),
        (44, 'Normal'),
        (45, ''),
        (46, 'Highest'),
        (47, 'Medium'),
        (48, 'Highest'),
        (59, 'Medium'),
        (50, 'Normal'),
        (51, ''),
        (52, 'Highest'),
        (53, 'Medium'),
        (54, 'Normal'),
        (55, ''),
        (56, 'Highest'),
        (57, 'Medium'),
        (58, 'Normal'),

    ], render_kw={"placeholder": "Choose a priority"}, validators=[DataRequired()])
    text = StringField("text", widget=TextArea())
    submit = SubmitField('update')

class loginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()]) 
    remember = BooleanField('Remember me')
    submit = SubmitField('login')     
    
class addForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    text = StringField("text", widget=TextArea())
    date_to_do = DateField('date_to_do', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.date.today())
    hour_to_do = StringField("hour_to_do", validators=[DataRequired()], default=8)
    min_to_do = StringField("min_to_do", validators=[DataRequired()], default=0)
    rep = StringField("rep", validators=[DataRequired()])
    dro = SelectField(u'Choose a programming language', choices=[
        (0, ''),
        (1, 'Highest'),
        (2, 'Medium'),
        (3, 'Normal'),
    ], render_kw={"placeholder": "Choose a priority"}, validators=[DataRequired()])
    submit = SubmitField('create')

class searchForm(FlaskForm):
    spi = SelectField(u'Choose a programming language', choices=[
        (1, ''),
        (2, 'Highest'),
        (3, 'Medium'),
        (4, 'Normal'),
        (5, ''),
        (6, 'Highest'),
        (7, 'Medium'),
        (8, 'Normal'),
    ], render_kw={"placeholder": "Choose a priority"}, validators=[DataRequired()])
    wil = SelectField(u'Choose a programming language', choices=[
        (1, ''),
        (2, 'Highest'),
        (3, 'Medium'),
        (4, 'Normal'),
        (5, ''),
        (6, 'Highest'),
        (7, 'Medium'),
        (8, 'Normal'),
        (9, ''),
        (10, 'Highest'),
        (11, 'Medium'),
        (12, 'Normal'),
        (13, ''),
        (14, 'Highest'),
        (15, 'Medium'),
        (16, 'Normal'),
        (17, ''),
        (18, 'Highest'),
        (19, 'Medium'),
        (20, 'Normal'),
        (21, ''),
        (22, 'Highest'),
        (23, 'Medium'),
        (24, 'Normal'),
        (25, ''),
        (26, 'Highest'),
        (27, 'Medium'),
        (28, 'Normal'),
        (29, ''),
        (30, 'Highest'),
        (31, 'Medium'),
        (32, 'Normal'),
        (33, ''),
        (34, 'Highest'),
        (35, 'Medium'),
        (36, 'Normal'),
        (37, ''),
        (38, 'Highest'),
        (39, 'Medium'),
        (40, 'Normal'),
        (41, ''),
        (42, 'Highest'),
        (43, 'Medium'),
        (44, 'Normal'),
        (45, ''),
        (46, 'Highest'),
        (47, 'Medium'),
        (48, 'Highest'),
        (59, 'Medium'),
        (50, 'Normal'),
        (51, ''),
        (52, 'Highest'),
        (53, 'Medium'),
        (54, 'Normal'),
        (55, ''),
        (56, 'Highest'),
        (57, 'Medium'),
        (58, 'Normal'),

    ], render_kw={"placeholder": "Choose a priority"}, validators=[DataRequired()])
    submit = SubmitField('search')

class searchrdvForm(FlaskForm):
   date_to_do = DateField('date_to_do', format='%Y-%m-%d', validators=[DataRequired()])
   time_to_do = TimeField('time_to_do', format='%H:%M', validators=[DataRequired()])
   submit = SubmitField('search')

class rdvForm(FlaskForm):
   name = StringField("title", validators=[DataRequired()])
   prename = StringField("title", validators=[DataRequired()])
   date_to_do = DateField('date_to_do', format='%Y-%m-%d', validators=[DataRequired()])
   time_to_do = TimeField('time_to_do', format='%H:%M', validators=[DataRequired()])
   drname = StringField("title", validators=[DataRequired()])
   text = StringField("text", widget=TextArea())
   ntph = StringField("tiliphon", validators=[DataRequired()])
   submit = SubmitField('create')
   
   def date_time_to_do(self):
        return datetime.datetime.combine(self.date_to_do.data, self.time_to_do.data)

class AddTextForm(FlaskForm):
    new_text = StringField('Enter the text you want to add:', validators=[DataRequired()])
    submit = SubmitField('Add Text')

@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
 form = searchForm()
 if request.method == 'POST':
  print(form.spi.data)
  print(form.wil.data)
  return redirect(url_for('search', w=form.wil.data, s=form.spi.data))
 else:
  return render_template('home.html',form=form)
 
@app.route('/home_doctor', methods=['POST', 'GET'])
@login_required
def home_doctor():
 form = searchrdvForm()
 if request.method == 'POST':
  return redirect(url_for('searchrdv', w=form.date_to_do.data, s=form.time_to_do.data))
 else:
  return render_template('home_doctor.html',form=form)

@app.route('/', methods=['POST', 'GET'])
def intro():
    return render_template('intro.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form=loginForm()
    for i in enumerate(form):
        print(i[1].data)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        passed = check_password_hash(user.password_hash, form.password.data )
        if user is None or not passed :
            form.password.data = ''
            form.email.data = ''
            flash(" this account does not exist")
            return render_template('login.html', form = form)
        else :
            if passed is True :
                b = form.remember.data
                flash("login successful")
                login_user(user, remember=b)
                if user.wil!="userr":
                 if user.bro=="0":
                  return redirect(url_for('home_doctor'))
                 else:
                  return redirect(url_for('home'))
                 
                else:
                  return redirect(url_for('profil_edit'))  
            else :
                flash("wrong password try again")
                form.password.data = ''
                return render_template('login.html', form = form)
        
    else :
      return render_template('login.html', form = form)
    
@app.route('/add_user', methods = ['POST' , 'GET'])
def add_user():
    form = userForm()
    if form.validate_on_submit():
        v = validate_email(form.email.data, verify=True)
        if v:
          user = User.query.filter_by(email=form.email.data).first()
          print('''user: {user}''')
          if user is None:
              #hash password!!
              hashed_pw = generate_password_hash(form.password_hash.data)
              user = User(name=form.name.data, email=form.email.data, password_hash=hashed_pw, bro=form.bro.data)
              db.session.add(user)
              db.session.commit()
              if user.bro=="1":
               inf = info(id_user=user.id, prename="pat", Ntph="pat", adresse="pat", datn="pat", text="someone")
              else:
               inf = infod(id_user=user.id, prename="doc", Ntph="doc", adresse="doc", datn="doc", text="someone")

              db.session.add(inf)
              db.session.commit()
              flash("your account has been created please login ")
              print("your account has been created please login ")
              return redirect(url_for('login'))
          else :
              flash("this accont already exist please try to login")
              print("this accont already exist please try to login")
              return redirect(url_for('login'))     
        else:
           form.email.data = ''
           return render_template('add_user.html',
                               form = form,
                               ) 
    else :
        return render_template('add_user.html',
                               form = form,
                               )

@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect(url_for('intro'))

@app.route('/profil', methods = ['GET','POST'])
@login_required
def profil():
    inf = info.query.filter(info.id_user==current_user.id)
    return render_template('profil.html', inf=inf)

@app.route('/profil/edit', methods=['GET','POST'])
@login_required
def profil_edit():
    form = edit_userForm()
    user = current_user
    if user.bro=="1":
     inf = info.query.filter(info.id_user==user.id).first()
    else:
     inf = infod.query.filter(infod.id_user==user.id).first()

    if request.method=="POST":
        print(form.Ntph.data)
        print(form.datn.data)
        if form.email.data == '':
            form.email.data = user.email
        if form.name.data == '':
            form.name.data = user.name


        v = validate_email(form.email.data, verify=True)
        if v:
         user.id= user.id
         user.name = form.name.data
         user.email = form.email.data
         if form.spi.data=="":
          user.spi = "userr"
         user.wil = form.wil.data
         db.session.commit()
         inf.prename = form.prename.data   
         inf.datn = form.datn.data
         inf.Ntph = form.Ntph.data 
         inf.adresse = form.adresse.data
         if form.text.data=='':
          inf.text = "somone"
         else:
          inf.text = form.text.data
         if user.bro=="1":
          inf = info(id_user=user.id, prename=form.prename.data, Ntph=form.Ntph.data, adresse=form.prename.data, datn=form.datn.data, text="someone")
         else:
          inf = infod(id_user=user.id, prename=form.prename.data, Ntph=form.Ntph.data, adresse=form.prename.data, datn=form.datn.data, text="someone")
         db.session.commit()
         return redirect(url_for('profil'))
        else:
            form.email.data = ''
            return render_template('edit.html', form=form)
        # redirect to the profile page
    else:  
     form.email.data = current_user.email
     form.name.data = current_user.name
     return render_template('edit.html', form=form)
    

@app.route('/search', methods = ['POST','GET'])
@app.route('/search/<w>/<s>', methods = ['POST','GET'])
def search(w,s):
    form = searchForm()
    infds = infod.query.all()

    if w =="1":
      docts = User.query.filter(User.bro=="0" and User.spi==s).all()
    else:
      docts = User.query.filter(User.bro=="0" and User.wil==w and User.spi==s).all()
        

    form.wil.data= w
    form.spi.data= s
    if w=="1" and s=="1":
       return render_template('home.html', form=form)
    else:
       return render_template('search.html', form=form, docts=docts,infds=infds, w=w, s=s)

@app.route('/searchrdv', methods = ['POST','GET'])
@app.route('/searchrdv/<w>/<s>', methods = ['POST','GET'])
def searchrdv(w,s):
   form1 = AddTextForm()
   datetime.datetime.combine(w,s)
   rd = rdv.query.filter((rdv.date_to_do==datetime.datetime.combine(w,s)) and (rdv.drid==current_user.id)).first()
   fr = info.query.filter(info.id_user==rd.ptid).first()
   pt = User.query.filter(User.id==rd.ptid)
   rd_time = rd.date_to_do.strftime('%H:%M')
   if form1.validate_on_submit:
      old_text = fr.text
      new_text = form1.new_text.data
      fr.text= old_text + new_text
      db.session.commit()
   return render_template('searchrdv.html', rd=rd, fr=fr, rd_time=rd_time, pt=pt)

#@app.route('/profil_doctor', methods = ['POST','GET'])
@app.route('/profil_doctor/<idu>', methods = ['POST','GET'])
def profil_doctor(idu):
    form = rdvForm()
    idd = int(idu)
    user = User.query.filter(User.id==idd).first()
    inf = infod.query.filter(infod.id_user==idd).first()
    prename = inf.prename
    datn = inf.datn
    adresse = inf.adresse
    Ntph = inf.Ntph
    text = inf.text
    if form.name.data != None:
     if request.method == 'POST':
        print(form.name.data)
        rv = rdv(date_to_do =form.date_time_to_do(), text =form.text.data, drname =form.drname.data, drid =idu, ptid =current_user.id, name =form.name.data , prename =form.name.data, ntph =form.ntph.data)
        db.session.add(rv)
        db.session.commit()
        form.name.data= ''
        form.prename.data= ''
        form.date_to_do.data= ''
        form.time_to_do.data= ''
        form.drname.data= ''
        form.text.data= ''
        form.ntph.data= ''
        form.submit.data= ''


    times = []
    if form.name.data == None:
     if request.method == 'POST':
        date_str = request.form['date']
        date_format = '%Y-%m-%d'

        try:
            date = datetime.datetime.strptime(date_str, date_format)
            start_time = datetime.datetime.combine(date, datetime.datetime.min.time())
            end_time = datetime.datetime.combine(date, datetime.datetime.max.time())
            current_time = start_time.replace(hour=8, minute=0)
            end_time = end_time.replace(hour=16, minute=0)
            pose_time = start_time.replace(hour=12, minute=0)
            print(pose_time)
            while current_time <= end_time:
                if ((not rdv.query.filter(rdv.date_to_do == current_time).first()) and (not current_time==pose_time)):
                    times.append(current_time.strftime('%I:%M %p'))

                current_time += timedelta(minutes=30)

            if len(times) > 0:
                times.pop() 

        except ValueError:
            times = []


    return render_template('profil_doctor.html',form=form ,prename=prename ,datn=datn ,adresse=adresse ,Ntph=Ntph ,text=text, name=user.name, spi=user.spi, wil=user.wil, email=user.email, times=times)

with app.app_context():
        db.create_all()

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)
 