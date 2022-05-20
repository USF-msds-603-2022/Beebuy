import os
import sys
import click
from flask import Flask, flash, redirect, render_template, send_from_directory, url_for
from flask_bootstrap import Bootstrap4
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

"""
    ____             __ _                            _   _             
   / ___|___  _ __  / _(_) __ _ _   _ _ __ ___  __ _| |_(_) ___  _ __  
  | |   / _ \| '_ \| |_| |/ _` | | | | '__/ _ \/ _` | __| |/ _ \| '_ \ 
  | |__| (_) | | | |  _| | (_| | |_| | | |  __/ (_| | |_| | (_) | | | |
   \____\___/|_| |_|_| |_|\__, |\__,_|_|  \___|\__,_|\__|_|\___/|_| |_|
                          |___/                                        
"""
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Shouldwebuy168@group6-db.ciuiqprwm79f.us-east-1.rds.amazonaws.com/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)
bootstrap = Bootstrap4(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

"""
    ____ __  __ ____  
   / ___|  \/  |  _ \ 
  | |   | |\/| | | | |
  | |___| |  | | |_| |
   \____|_|  |_|____/ 
"""
@app.cli.command
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

"""
   __  __           _      _ 
  |  \/  | ___   __| | ___| |
  | |\/| |/ _ \ / _` |/ _ \ |
  | |  | | (_) | (_| |  __/ |
  |_|  |_|\___/ \__,_|\___|_|
"""
class User(db.Model, UserMixin):
    id =            db.Column(db.Integer, primary_key=True)
    username =      db.Column(db.String(80), unique=True, nullable=False)
    email =         db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    # Need to use different name for WTF check.
    submit1 = SubmitField('Submit')

class LogInForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    # Need to use different name for WTF check.
    submit2 = SubmitField('Login')


items = []
items.append({'name':'Samsung','code':'B08V37JHSQ','score':9, 'critic_rating':95, 'user_rating':4.4, 'price_score': 'Good',
              'img_address':'https://www.amazon.com/SAMSUNG-85-Inch-Class-QN85A-Built/dp/B08V37JHSQ/ref=sr_1_1_sspa?crid=3ADPK2WZ7TB3L&keywords=Samsung+tv&qid=1649383624&sprefix=samsung+tv%2Caps%2C282&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExV0tJSFJGSFpBVk9NJmVuY3J5cHRlZElkPUEwMDM4NjE2MVJPVUNNV1cyWDZTOSZlbmNyeXB0ZWRBZElkPUExMDA4MTc5WjRPTTRVRTlNRUJJJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==',
              'img':'https://m.media-amazon.com/images/I/816z9yHvl4L._AC_SL1500_.jpg'})
items.append({'name':'Sony','code':'B08WJMQ5TG','score':8.6, 'critic_rating':88, 'user_rating':4.1, 'price_score': 'Great',
              'img_address':'https://www.amazon.com/Sony-X85J-Inch-Compatibility-KD50X85J/dp/B08WJMQ5TG/ref=sr_1_3?crid=FIRWCM4EUP5H&keywords=Sony%2Btv&qid=1649383693&sprefix=sony%2Btv%2Caps%2C189&sr=8-3&th=1',
              'img':'https://m.media-amazon.com/images/I/81gvQXs0CML._AC_SL1500_.jpg'})
items.append({'name':'Lg','code':'B098KMQFLR','score':9.6, 'critic_rating':92, 'user_rating':4.5, 'price_score': 'Great',
              'img_address':'https://www.amazon.com/LG-43UP8000PUR-Alexa-Built-Smart/dp/B098KMQFLR/ref=sr_1_3_mod_primary_new?crid=OEVWA5JY2SKA&keywords=lg%2Btv&qid=1649383736&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=lg%2Btv%2Caps%2C297&sr=8-3&th=1',
              'img':'https://m.media-amazon.com/images/I/A1x+r1Swa+S._AC_SL1500_.jpg'})
items.append({'name':'TCL','code':'B0885N17CC','score':5.5, 'critic_rating':65, 'user_rating':4.1, 'price_score': 'Okay',
              'img_address':'https://www.amazon.com/dp/B0885N17CC/ref=redir_mobile_desktop?_encoding=UTF8&aaxitk=587b1f6935a5002f9dbc01c05b389cb1&hsa_cr_id=3832062660101&pd_rd_plhdr=t&pd_rd_r=be5bc822-fd56-40c2-a582-3080c52a2485&pd_rd_w=mCWpa&pd_rd_wg=WA2Su&ref_=sbx_be_s_sparkle_mcd_asin_0_img',
              'img':'https://m.media-amazon.com/images/I/91CXxVtVkAL._AC_SL1500_.jpg'})
items.append({'name':'Insignia','code':'B08Z265BJH','score':4.6, 'critic_rating':91, 'user_rating':3.9, 'price_score': 'Good',
              'img_address':'https://www.amazon.com/Insignia-50-inch-Class-Smart-Fire/dp/B08Z265BJH/ref=sr_1_2_sspa?crid=28YZLD7TWZ02U&keywords=tv&qid=1649382165&sprefix=t+v%2Caps%2C294&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzMkczNldSSzg5M01MJmVuY3J5cHRlZElkPUEwMTQyMjYwQjdWQTdMSDRZRENFJmVuY3J5cHRlZEFkSWQ9QTA2NDc5NTIxWUZFS1E5NkIyTFA0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==',
              'img':'https://m.media-amazon.com/images/I/81kRxFTpd1L._AC_SL1500_.jpg'})
items.append({'name':'VIZIO','code':'B092Q8L5DV','score':6.0, 'critic_rating':67, 'user_rating':3.1, 'price_score': 'Poor',
              'img_address':'https://www.amazon.com/VIZIO-65-Inch-AirPlay-Chromecast-V655-J09/dp/B092Q8L5DV/ref=sr_1_2?crid=1P4G301WOXA19&keywords=VIZIO+tv&qid=1649382210&sprefix=vizio+t+v%2Caps%2C282&sr=8-2',
              'img':'https://m.media-amazon.com/images/I/81ii3VScCbL._AC_SL1500_.jpg'})

"""
    ____ _____ ____  _              
   / ___|_   _|  _ \| |    ___ _ __ 
  | |     | | | |_) | |   / _ \ '__|
  | |___  | | |  _ <| |__|  __/ |   
   \____| |_| |_| \_\_____\___|_|   
"""
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 
                            'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def basic():
    good_items = []
    bad_items = []
    for item in items:
        url = '/product/' + 'dp/' + item['img_address'].split('/dp/')[1].split('/ref=')[0]

        if item['score'] > 6:
            good_items.append((item, url))
        if item['score'] <= 6:
            bad_items.append((item, url))
    return render_template('index.html',good_items=good_items, bad_items=bad_items)

@app.route("/suggestion")
def suggest():
    return render_template('suggestion.html', items=items)
    
@app.route("/dontbuy")
def dontbuy():
    return render_template('dontbuy.html', items=items)

@app.route("/about")
def following():
    member_list = []
    member_list.append({'name':'David Lyu','role':'CEO','linkedin':'https://www.linkedin.com/in/david-muhuan-lyu/','profile':'/static/member_folder/david.png'})
    member_list.append({'name':'Yoli Wu','role':'CTO','linkedin':'https://www.linkedin.com/in/you-yoli-wu/','profile':'/static/member_folder/yoli.png'})
    member_list.append({'name':'Young Zeng','role':'COO','linkedin':'https://www.linkedin.com/in/yixuan-young-zeng-574359105/','profile':'/static/member_folder/young.png'})
    member_list.append({'name':'Chandan Nayak','role':'Product Manager','linkedin':'https://www.linkedin.com/in/nayakchandan/','profile':'/static/member_folder/chandan.png'})
    member_list.append({'name':'Yunhe Jia','role':'Software Engineer','linkedin':'https://www.linkedin.com/in/yunhe-j-380651172/','profile':'/static/member_folder/yunhe.png'})
    member_list.append({'name':'Meilin Li','role':'Data Scientist','linkedin':'https://www.linkedin.com/in/li-meilin','profile':'/static/member_folder/meilin.png'})
    member_list.append({'name':'Jaysen Shi','role':'Data Engineer','linkedin':'https://www.linkedin.com/in/jaysenshi/','profile':'/static/member_folder/jaysen.png'})
    return render_template('about_page.html',member_list = member_list)

########## User Related ##########
@app.route('/login', methods=['GET', 'POST'])
def login():
    registration_form = RegistrationForm()
    login_form = LogInForm()
    # Registration
    if registration_form.submit1.data and registration_form.validate_on_submit():
        username = registration_form.username.data
        # Hash the password and store
        password = generate_password_hash(registration_form.password.data)
        email = registration_form.email.data
        user_count = User.query.filter_by(username = username).count() + + User.query.filter_by(email=email).count()
        if user_count > 0:
            flash('error - Existing user : ' + username + ' OR ' + email)
        else:
            user = User(username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()
            flash('Welcome, ' + username)
            return redirect(url_for('login'))
    # Login
    if login_form.submit2.data and login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('basic'))
        else:
            flash('Invalid username or password combination!')
    return render_template('user.html', form1=registration_form, form2=login_form)

@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('basic'))
    else:
        return render_template('error_page.html')

@app.route('/account')
@login_required
def myAccount():
    if current_user.is_authenticated:
        return render_template('myaccount.html',items = items)
    else:
        flash("Please login first")
        return redirect(url_for('login'))

############ This are hard-coded variables
review_list = []
review_list.append({'publisher':'CNET','abstract':'With a world-beating picture, oodles of features and slim styling, the LG C1 remains the TV to beat. ',
                    'url':'https://www.cnet.com/reviews/lg-oled55c1pub-review/'})
review_list.append({'publisher':'RTINGS','abstract':"As expected, it's an amazing TV, but aside from a few minor tweaks and upgrades—like the new 'Game Optimizer' settings, a redesigned Magic Remote, and a new version of webOS—it performs about the same as its predecessor. ",
                    'url':'https://www.rtings.com/tv/reviews/lg/c1-oled'})
review_list.append({'publisher':'TECHRADAR','abstract':'The C1 OLED is one of the best TVs we’ve seen in 2021, and a very good option for a cheaper OLED in 2022.',
                    'url':'https://www.techradar.com/reviews/lg-c1-oled-tv-oled65c1'})
review_list.append({'publisher':'IGN','abstract':"A gorgeous OLED, a great 4K smart TV, and the best gaming TV we've ever seen.",
                    'url':'https://www.tomsguide.com/reviews/lg-c1-oled-tv'})
review_list.append({'publisher':'TOMS GUIDE','abstract':'The LG C1 is what I would buy if I were in the market for a gaming television. It does everything right that matters and is packed to the gills with the hardware and software features.',
                    'url':'https://www.ign.com/articles/lg-c1-review'})
pros_list = []
pros_list.append('Near-infinite contrast ratio')
pros_list.append('Wide viewing angles')
pros_list.append('Upscales content without issue')
cons_list = []
cons_list.append('Risk of permanent burn-in')
cons_list.append('May not be bright enough for very bright or sunny rooms')
cons_list.append('No way to disable ads on the interface')
############

@app.route("/product/dp/B08WFV7L3N")
def evaluate():
  template1 = 'index_product.html'
  template2 = 'product.html'
  
  original_url = 'https://www.amazon.com/' + 'dp/B08WFV7L3N'
  
  critic_rating = 85
  user_rating = 4.2
  price_score = 'Great'
  product_name = "LG OLED C1 Series"
  product_img_url = "/static/item_folder/lg_c1.jpeg"
  price_history = '/static/item_folder/price_history.png'
  radar_chart = "https://miro.medium.com/max/1400/1*YFroPGj9dpPx7nqf045AUQ.png"
  
  return render_template(template1, critic_rating = critic_rating, user_rating = user_rating, price_score = price_score, review_list = review_list, pros_list = pros_list, cons_list = cons_list,
product_name = product_name, original_url = original_url, product_img_url = product_img_url, price_history= price_history, radar_chart = radar_chart)


@app.route("/product/<website_special>/<product_code>")
def product(website_special = 'dp', product_code = 'B085WTYQ4X'):
    template1 = 'index_product.html'
    template2 = 'product.html'
    original_url = 'https://www.amazon.com/' + website_special + '/' + product_code
    for j in items:
        if j['code'] == product_code:
            critic_rating = j['critic_rating']
            user_rating = j['user_rating']
            price_score = j['price_score']
            product_name = j['name']
            product_img_url = j['img']
            price_history = '/static/item_folder/price_history.png'
            radar_chart = "https://miro.medium.com/max/1400/1*YFroPGj9dpPx7nqf045AUQ.png"
    return render_template(template1, critic_rating = critic_rating, user_rating = user_rating, price_score = price_score, review_list = review_list, pros_list = pros_list, cons_list = cons_list, product_name = product_name, original_url = original_url, product_img_url = product_img_url, price_history= price_history, radar_chart = radar_chart)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)