from xml.dom.pulldom import IGNORABLE_WHITESPACE
from flask import Flask, render_template, request, flash, Markup, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields import *
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager
from flask_wtf import FlaskForm, CSRFProtect
from flask_bootstrap import Bootstrap4, SwitchField
from wtforms.validators import DataRequired, Length, Regexp,EqualTo
from wtforms.fields import *
import os
from flask_login import current_user, login_user, login_required, logout_user
import time
# member_folder = os.path.join('static','member_folder')

app = Flask(__name__)
app.secret_key = 'dev'
# app.config['mbr_folder'] = member_folder
bootstrap = Bootstrap4(app)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

# database input
items = []
items.append({'name':'Samsung','code':'B08V37JHSQ','score':9,'img_address':'https://www.amazon.com/SAMSUNG-85-Inch-Class-QN85A-Built/dp/B08V37JHSQ/ref=sr_1_1_sspa?crid=3ADPK2WZ7TB3L&keywords=Samsung+tv&qid=1649383624&sprefix=samsung+tv%2Caps%2C282&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExV0tJSFJGSFpBVk9NJmVuY3J5cHRlZElkPUEwMDM4NjE2MVJPVUNNV1cyWDZTOSZlbmNyeXB0ZWRBZElkPUExMDA4MTc5WjRPTTRVRTlNRUJJJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==','img':'https://m.media-amazon.com/images/I/816z9yHvl4L._AC_SL1500_.jpg'})
items.append({'name':'Sony','code':'B08WJMQ5TG','score':8.6,'img_address':'https://www.amazon.com/Sony-X85J-Inch-Compatibility-KD50X85J/dp/B08WJMQ5TG/ref=sr_1_3?crid=FIRWCM4EUP5H&keywords=Sony%2Btv&qid=1649383693&sprefix=sony%2Btv%2Caps%2C189&sr=8-3&th=1','img':'https://m.media-amazon.com/images/I/81gvQXs0CML._AC_SL1500_.jpg'})
items.append({'name':'Lg','code':'B098KMQFLR','score':9.6,'img_address':'https://www.amazon.com/LG-43UP8000PUR-Alexa-Built-Smart/dp/B098KMQFLR/ref=sr_1_3_mod_primary_new?crid=OEVWA5JY2SKA&keywords=lg%2Btv&qid=1649383736&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=lg%2Btv%2Caps%2C297&sr=8-3&th=1','img':'https://m.media-amazon.com/images/I/A1x+r1Swa+S._AC_SL1500_.jpg'})
items.append({'name':'TCL','code':'B0885N17CC','score':5.5,'img_address':'https://www.amazon.com/dp/B0885N17CC/ref=redir_mobile_desktop?_encoding=UTF8&aaxitk=587b1f6935a5002f9dbc01c05b389cb1&hsa_cr_id=3832062660101&pd_rd_plhdr=t&pd_rd_r=be5bc822-fd56-40c2-a582-3080c52a2485&pd_rd_w=mCWpa&pd_rd_wg=WA2Su&ref_=sbx_be_s_sparkle_mcd_asin_0_img','img':'https://m.media-amazon.com/images/I/91CXxVtVkAL._AC_SL1500_.jpg'})
items.append({'name':'Insignia','code':'B08Z265BJH','score':4.6,'img_address':'https://www.amazon.com/Insignia-50-inch-Class-Smart-Fire/dp/B08Z265BJH/ref=sr_1_2_sspa?crid=28YZLD7TWZ02U&keywords=tv&qid=1649382165&sprefix=t+v%2Caps%2C294&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzMkczNldSSzg5M01MJmVuY3J5cHRlZElkPUEwMTQyMjYwQjdWQTdMSDRZRENFJmVuY3J5cHRlZEFkSWQ9QTA2NDc5NTIxWUZFS1E5NkIyTFA0JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==','img':'https://m.media-amazon.com/images/I/81kRxFTpd1L._AC_SL1500_.jpg'})
items.append({'name':'VIZIO','code':'B092Q8L5DV','score':6.0,'img_address':'https://www.amazon.com/VIZIO-65-Inch-AirPlay-Chromecast-V655-J09/dp/B092Q8L5DV/ref=sr_1_2?crid=1P4G301WOXA19&keywords=VIZIO+tv&qid=1649382210&sprefix=vizio+t+v%2Caps%2C282&sr=8-2','img':'https://m.media-amazon.com/images/I/81ii3VScCbL._AC_SL1500_.jpg'})
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
    submit = SubmitField('submit')

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
    return render_template('main.html', good_items=good_items, bad_items=bad_items)
    
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

# @app.route('/register',methods=['GET', 'POST'])
# def register():
#     form = Register()
#     if form.validate_on_submit():
#         return redirect(url_for('basic'))
#     return render_template(
#         'user.html',
#         form=form
#     ) 

# @app.route('/login',methods=['GET', 'POST'])
# def login():
#     form = Login()
#     if form.validate_on_submit():
#         # flash('Form validated!')
#         return redirect(url_for('myAccount'))
#     return render_template(
#         'user.html',
#         form = form
#     ) 


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# @app.route('/index')
# @app.route('/')
# def index():
#     return render_template('index.html', authenticated_user=current_user.is_authenticated)

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
            flash('Thanks for registering!')
            return redirect(url_for('login'))
    return render_template('user.html',form=registration_form)

@app.route('/exam', methods=['GET', 'POST'])
@login_required
def examples():
    return render_template('examples.html', authenticated_user=current_user.is_authenticated,)


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
            flash('Invalid username and password combination!')
    return render_template('user.html', form=login_form)

@app.route('/logout')
@login_required
def logout():

    before_logout = '<h1> Before logout - is_autheticated : ' \
                    + str(current_user.is_authenticated) + '</h1>'

    logout_user()

    after_logout = '<h1> After logout - is_autheticated : ' \
                + str(current_user.is_authenticated) + '</h1>'
    return before_logout + after_logout


@app.route("/product/dp/B007M0I850")
def evaluate():
    original_url = 'https://www.amazon.com/' + 'dp/B007M0I850'

    product_img_url = "https://ca-times.brightspotcdn.com/dims4/default/9b1c273/2147483647/strip/true/crop/3000x2000+0+0/resize/840x560!/format/webp/quality/90/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2Fe3%2Fef%2F1473571143efbd8cd764a95352d8%2F927753-me-0308-gas-2-rcg.jpg"
    price_history = "https://cdn.forumcomm.com/dims4/default/a314711/2147483647/strip/true/crop/670x325+0+0/resize/1680x814!/format/webp/quality/90/?url=https%3A%2F%2Fforum-communications-production-web.s3.amazonaws.com%2Fbrightspot%2F51%2F8c%2F9bab38594800892f770e8350a078%2Fgas-prices-chart.gif"
    radar_chart = "https://miro.medium.com/max/1400/1*YFroPGj9dpPx7nqf045AUQ.png"

    return render_template('product.html', original_url = original_url, product_img_url = product_img_url, price_history= price_history, radar_chart = radar_chart)

@app.route("/product/<website_special>/<product_code>")
def product(website_special = 'dp', product_code = 'B085WTYQ4X'):
    original_url = 'https://www.amazon.com/' + website_special + '/' + product_code
    for j in items:
        if j['code'] == product_code:
            product_name = j['name']
            product_img_url = j['img']
            price_history = "https://cdn.forumcomm.com/dims4/default/a314711/2147483647/strip/true/crop/670x325+0+0/resize/1680x814!/format/webp/quality/90/?url=https%3A%2F%2Fforum-communications-production-web.s3.amazonaws.com%2Fbrightspot%2F51%2F8c%2F9bab38594800892f770e8350a078%2Fgas-prices-chart.gif"
            radar_chart = "https://miro.medium.com/max/1400/1*YFroPGj9dpPx7nqf045AUQ.png"
    return render_template('product.html', product_name = product_name, original_url = original_url, product_img_url = product_img_url, price_history= price_history, radar_chart = radar_chart)

@app.route('/myAccount')
def myAccount():
    view_history = []
    for item in items:
        url = '/product/' + 'dp/' + item['img_address'].split('/dp/')[1].split('/ref=')[0]
        if item['score'] >= 8.5:
            view_history.append((item, url))
    return render_template('myaccount.html', view_history = view_history)

if __name__=='__main__':
    app.run(host='0.0.0.0',debug = True)