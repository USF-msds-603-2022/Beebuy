from flask import Flask,  render_template
from wtforms.fields import *
from flask_wtf import FlaskForm, CSRFProtect
from flask_bootstrap import Bootstrap4, SwitchField
from flask import Flask, render_template, request, flash, Markup, redirect, url_for
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import *
# import os

# member_folder = os.path.join('static','member_folder')

app = Flask(__name__)
app.secret_key = 'dev'
# app.config['mbr_folder'] = member_folder
bootstrap = Bootstrap4(app)
csrf = CSRFProtect(app)

# database input
items = []
items.append({'name':'Samsung','score':9,'img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6452/6452997_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/samsung.png'})
items.append({'name':'Sony','score':8.6,'img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6453/6453619_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/sony.png'})
items.append({'name':'Lg','score':9.6,'img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6458/6458623_sd.jpg;maxHeight=640;maxWidth=550','profile':'/static/item_folder/lg.png'})
items.append({'name':'TCL','score':5.5,'img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6470/6470251_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/tcl.png'})
items.append({'name':'Insignia','score':4.6,'img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6456/6456970_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/insignia.png'})
items.append({'name':'VIZIO','score':6.0,'img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6459/6459559_sd.jpg;maxHeight=640;maxWidth=550','profile':'/static/item_folder/vizio.png'})

class SearchBar(FlaskForm):
    search = SearchField()


class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = EmailField('Email')
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 150)])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), Length(8, 150)])
    submit = SubmitField('Register')

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = EmailField('Email')
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 150)])
    submit = SubmitField('submit')


@app.route("/")
def basic():
    return render_template('main.html', items=items)
    
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

@app.route('/register',methods=['GET', 'POST'])
def register():
    form = Register()

    if form.validate_on_submit():
        # if form.password()==form.confirmpassword():
        # flash('Form validated!')
        return redirect(url_for('basic'))
    return render_template(
        'user.html',
        form=form
    ) 

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        # flash('Form validated!')
        return redirect(url_for('basic'))
    return render_template(
        'user.html',
        form=form
    ) 


if __name__=='__main__':
    app.run(host='0.0.0.0',debug = True)