from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, json, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from waitress import serve
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, DateField, SelectField
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
    post = db.relationship('to_do', backref='todos')
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

class to_do(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_to_do = db.Column(db.DateTime, nullable=False)
    hour_to_do = db.Column(db.Integer, nullable=True, default=8)
    min_to_do = db.Column(db.Integer, nullable=True, default=00)
    val = db.Column(db.String(1), default=0)
    pre = db.Column(db.String(1), default=3)
    datenow = db.Column(db.DateTime, default=datetime.datetime.utcnow)

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
    
class todoForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    text = StringField("text", widget=TextArea())
    date_to_do = DateField('date_to_do', format='%Y-%m-%d', validators=[DataRequired()])
    hour_to_do = StringField("hour_to_do", validators=[DataRequired()])
    min_to_do = StringField("min_to_do", validators=[DataRequired()])
    checkbox = BooleanField("check if you do it")
    submit = SubmitField('create')

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

@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
 form = searchForm()
 if form.spi!=None:
   redirect(url_for('test', w=form.wil.data, s=form.spi.data))

 return render_template('home.html',form=form)

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
                return redirect(url_for('home'))
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
              flash("your account has been created please login ")
              print("your account has been created please login ")
              return redirect(url_for('profil_edit'))
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

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = to_do.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('todo'))

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
    print(form.Ntph.data)
    if user.bro=="1":
     inf = info.query.filter(info.id_user==user.id)
    else:
     inf = infod.query.filter(infod.id_user==user.id)

    if form.validate_on_submit():
        print(form.Ntph.data)
        print(form.datn.data)
        if form.email.data == '':
            form.email.data = user.email
        if form.name.data == '':
            form.name.data = user.name

        v = validate_email(form.email.data, verify=True)
        if v:
         
         user.name = form.name.data
         user.email = form.email.data
         user.spi = form.spi.data
         user.wil = form.wil.data
         db.session.commit()
         inf.prename = form.prename.data   
         inf.datn = form.datn.data
         inf.Ntph = form.Ntph.data 
         inf = info(id_user=user.id, prename=form.prename.data, Ntph=form.Ntph.data, adresse=form.prename.data, datn=form.datn.data, text="someone")
         # update the database
         db.session.add(inf)
         db.session.commit()
        else:
            form.email.data = ''
            return render_template('edit.html', form=form)
        # redirect to the profile page
        return redirect(url_for('profil'))
       
    
    form.email.data = current_user.email
    form.name.data = current_user.name
    return render_template('edit.html', form=form)


@app.route('/test', methods = ['POST','GET'])
@app.route('/test/<w>/<s>', methods = ['POST','GET'])
def test(w,s):
    form = searchForm()
    infds = info.query.all()
    if w !=0:
     docts = User.query.filter(User.bro==0 and User.wil==w and User.spi==s).all()
    else:
      docts = User.query.filter(User.bro==0 and User.spi==s).all()
        

    form.wil.data= w
    form.spi.data= s
    return render_template('search.html', form=form, docts=docts,infds=infds, w=w, s=s)

with app.app_context():
        db.create_all()

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)
 