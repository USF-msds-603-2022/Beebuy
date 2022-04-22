from flask import Flask,  render_template,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields import *
from werkzeug.security import check_password_hash
from flask_login import LoginManager, UserMixin
from flask_wtf import FlaskForm, CSRFProtect
from flask_bootstrap import Bootstrap4, SwitchField
from flask import Flask, render_template, request, flash, Markup, redirect, url_for
from wtforms.validators import DataRequired, Length, Regexp,EqualTo
from wtforms.fields import *
from werkzeug.security import generate_password_hash
import os
from flask_login import current_user, login_user, login_required, logout_user
import time
# from django.contrib.auth.decorators import login_required
# member_folder = os.path.join('static','member_folder')

app = Flask(__name__)
app.secret_key = 'dev'# app.config['mbr_folder'] = member_folder
bootstrap = Bootstrap4(app)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

# database input
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
# items.append({'name':'Toshiba','code':'B0924SX7P1','score':7.5,'img_address':'https://www.amazon.com/Toshiba-65-inch-4K-UHD-Smart-Fire-TV/dp/B0924SX7P1/ref=sr_1_5_sspa?gclid=EAIaIQobChMIjr_RrdyD9wIVxDizAB3DWA3WEAAYASAAEgIKBPD_BwE&hvadid=557209947814&hvdev=c&hvlocphy=1014221&hvnetw=g&hvqmt=b&hvrand=1267777265010267032&hvtargid=kwd-297505614716&hydadcr=20142_13296026&keywords=tv+at+amazon&qid=1649395315&sr=8-5-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFEWk9MSzROQ1VKOUImZW5jcnlwdGVkSWQ9QTA1MDU0NTEyVERPRzBMNVdLNjlZJmVuY3J5cHRlZEFkSWQ9QTAxMTYwNjVWSTkxVkVaTTdTNTYmd2lkZ2V0TmFtZT1zcF9tdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl','img':'https://m.media-amazon.com/images/I/81QvlthwGRS._AC_SL1500_.jpg'})

class SearchBar(FlaskForm):
    search = SearchField()



class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = EmailField('Email')
    password = PasswordField('Password', validators=[DataRequired(), Length(8,150)])
    confirmpassword = PasswordField('Confirm Password',validators=[DataRequired(), Length(8, 150),\
        EqualTo('password', message='Passwords must match')])
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice', [DataRequired()])
    submit = SubmitField('Register')

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = EmailField('Email')
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 150)])
    submit = SubmitField('login')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegisterTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    register_time = db.Column(db.Integer) ## Epoch Time
    username = db.Column(db.String(80), db.ForeignKey(User.username)) ## User who registered

    def __init__(self, username):
        self.username = username
        self.register_time = time.time()

class LoginTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_time = db.Column(db.Integer) ## Epoch Time
    username = db.Column(db.String(80), db.ForeignKey(User.username)) ## User who registered

    def __init__(self, username):
        self.username = username
        self.login_time = time.time()

db.create_all()
db.session.commit()

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LogInForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')



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


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/register',  methods=('GET', 'POST'))
def register():
    # https://flask.palletsprojects.com/en/2.1.x/patterns/wtforms/
    registration_form = Register()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = User.query.filter_by(username=username).count() \
                     + User.query.filter_by(email=email).count()

        if(user_count > 0):
            flash('Error - Existing user : ' + username + ' OR ' + email)            
        else:
            user = User(username, email, password)
            rt = RegisterTime(username)
            db.session.add(user)
            db.session.add(rt)
            db.session.commit()
            # flash('Thanks for registering!')
            return redirect(url_for('login'))
    return render_template('user.html',form=registration_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = Login()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = User.query.filter_by(username=username).first()
        # Login and validate the user.
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('basic'))
        else:
            print (user,password)
            flash('Invalid username and password combination!')
    return render_template('user.html', form=login_form)


@app.route('/logout')
# @login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('basic'))
    else:
        return render_template('error_page.html')

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
############


@app.route("/product/dp/B08WFV7L3N")
def evaluate():
    original_url = 'https://www.amazon.com/' + 'dp/B08WFV7L3N'

    critic_rating = 85
    user_rating = 4.2
    price_score = 'Great'
    product_name = "LG OLED C1 Series"
    product_img_url = "/static/item_folder/lg_c1.jpeg"
    price_history = '/static/item_folder/price_history.png'
    radar_chart = "https://miro.medium.com/max/1400/1*YFroPGj9dpPx7nqf045AUQ.png"

    tempfile1 = 'product.html'
    tempfile2 = 'product_page_templates/product.html'

    return render_template(tempfile1,
                           critic_rating = critic_rating, user_rating = user_rating, price_score = price_score,
                           review_list = review_list, pros_list = pros_list, cons_list = cons_list,
                           product_name = product_name, original_url = original_url, product_img_url = product_img_url,
                           price_history= price_history, radar_chart = radar_chart)

@app.route("/product/<website_special>/<product_code>")
def product(website_special = 'dp', product_code = 'B085WTYQ4X'):
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

    tempfile1 = 'product.html'
    tempfile2 = 'product_page_templates/product.html'

    return render_template(tempfile1,
                           critic_rating = critic_rating, user_rating = user_rating, price_score = price_score,
                           review_list = review_list, pros_list = pros_list, cons_list = cons_list,
                           product_name = product_name, original_url = original_url, product_img_url = product_img_url,
                           price_history= price_history, radar_chart = radar_chart)

@app.route('/myAccount')
# @login_required
def myAccount():
    if current_user.is_authenticated:
        return render_template('myaccount.html',items = items)
    else:
        # flash("Please login first")
        return render_template('error_page.html')
        # return redirect(url_for('login'))
    

if __name__=='__main__':
    app.run(host='0.0.0.0',debug = True)