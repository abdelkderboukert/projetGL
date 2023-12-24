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
    datn = db.Column(db.DateTime, nullable=False)
    adresse = db.Column(db.String(30), nullable=False, default='userr')
    Ntph = db.Column(db.String(12), nullable=False, default='userr')

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
    search = StringField("search", validators=[DataRequired()])
    submit = SubmitField('search')

@app.route('/', methods=['POST', 'GET'])
@login_required
def home():

 return render_template('home.html')

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
              return redirect(url_for('profil_edit'))
          else :
              flash("this accont already exist please try to login")
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
    return redirect(url_for('login'))

@app.route('/add-daily', methods = ['GET', 'POST'])
@login_required
def add_daily():
    form = addForm()
    if form.validate_on_submit():
        if form.hour_to_do == '':
            form.hour_to_do= '8'
        if form.min_to_do == '':
            form.min_to_do= '00'
        
        k = int(form.rep.data)
        p = int(form.dro.data)
        hour = int(form.hour_to_do.data)
        min = int(form.min_to_do.data)
        while k!=-1:
          if k!=0 : 
           form.date_to_do.data = form.date_to_do.data + timedelta(days=1)
          new_task = to_do(title=form.title.data, date_to_do=form.date_to_do.data, hour_to_do=hour, min_to_do=min, text=form.text.data,id_user= current_user.id , pre=p, val=0)
          db.session.add(new_task)
          db.session.commit()
          k=k-1

        
        flash('Task added successfully!', 'success')
        return redirect(url_for('todo'))

    tasks = to_do.query.all()
    return render_template('add_daily.html', form=form, tasks=tasks)

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

@app.route('/arvhive', methods = ['GET', 'POST'])
@login_required
def archive():
    form1 = todoForm() 
    search_query = request.args.get('query')
    if search_query:
        results = to_do.query.filter(to_do.title.like(f'%{search_query}%')).all()
    else:
        results = []
    dailys=to_do.query.filter(to_do.id_user==current_user.id)
    current_date = datetime.datetime.now().date()
    current_hour = datetime.datetime.now().hour
    return render_template('archive.html', dailys=dailys, form1=form1, date= current_date, hour= current_hour, results=results, search_query=search_query)

@app.route('/todo', methods = ['GET','POST'])
@login_required
def todo():
    form1 = todoForm() 
    search_query = request.args.get('query')
    if search_query:
        results = to_do.query.filter(to_do.title.like(f'%{search_query}%')).all()
    else:
        results = []
    dailys=to_do.query.filter(to_do.id_user==current_user.id).all()
    current_date = datetime.datetime.now().date()
    current_hour = datetime.datetime.now().hour
    if request.method == "POST":
     data = request.get_json()
     daily_id = data['id']
     dail = int(daily_id)
     di = to_do.query.filter(to_do.id==dail).first()
     di.val= '1'
     db.session.add(di)
     db.session.commit()
    return render_template('todo.html', dailys=dailys, form1=form1, date= current_date, hour= current_hour, results=results, search_query=search_query)
    
@app.route('/profil/edit', methods=['GET','POST'])
@login_required
def profil_edit():
    form = edit_userForm()
    user = current_user
    inf = info.query.filter(info.id_user==user.id)

    if form.validate_on_submit():
        if form.email.data == '':
            form.email.data = user.email
        print(form.email.data)
        print(form.email.data)
        if form.name.data == '':
            form.name.data = user.name

        v = validate_email(form.email.data, verify=True)
        if v:
         user.name = form.name.data
         user.email = form.email.data
         inf.prename = form.prename.data   
         inf.addresse = form.prename.data
         inf.datn = form.datn.data
         inf.Ntph = form.Ntph.data      
         # update the database
         db.session.commit()
        else:
            form.email.data = ''
            return render_template('edit.html', form=form)
        # redirect to the profile page
        return redirect(url_for('profil'))
    
    form.email.data = current_user.email
    form.name.data = current_user.name
    return render_template('edit.html')

@app.route('/test', methods = ['POST','GET'])
def test():
    form = edit_userForm()
    user = current_user
    if form.validate_on_submit():
        print(form.name.data)
        if form.email.data == '':
            form.email.data = user.email
        if form.name.data == '':
            form.name.data = user.name
        print(form.name.data)
        v = validate_email(form.email.data, verify=True)
        if v:
         user.name = form.name.data
         user.email = form.email.data
         print(user.name)
         # update the database
         db.session.commit()
         # redirect to the profile page
         return redirect(url_for('profil'))
        else:
            form.email.data = ''
            return render_template('edit.html', form=form)
        
    form.email.data = user.email
    form.name.data = user.name

    return render_template('test.html', form=form)

with app.app_context():
        db.create_all()

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)
 