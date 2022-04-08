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
    suggestion = []
    top10 = []
    suggestion.append({'name':'Samsung','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6452/6452997_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/samsung.png'})
    suggestion.append({'name':'Sony','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6453/6453619_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/sony.png'})
    suggestion.append({'name':'Lg','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6458/6458623_sd.jpg;maxHeight=640;maxWidth=550','profile':'/static/item_folder/lg.png'})
    top10.append({'name':'TCL','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6470/6470251_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/tcl.png'})
    top10.append({'name':'Insignia','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6456/6456970_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/insignia.png'})
    top10.append({'name':'VIZIO','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6459/6459559_sd.jpg;maxHeight=640;maxWidth=550','profile':'/static/item_folder/vizio.png'})
    return render_template('main.html',suggestion = suggestion, top10=top10)
    
@app.route("/suggestion")
def suggest():
    return render_template('suggestion.html')
    
@app.route("/dontbuy")
def dontbuy():
    return render_template('dontbuy.html')

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

@app.route("/product")
def product():
    product_img_url = "https://ca-times.brightspotcdn.com/dims4/default/9b1c273/2147483647/strip/true/crop/3000x2000+0+0/resize/840x560!/format/webp/quality/90/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2Fe3%2Fef%2F1473571143efbd8cd764a95352d8%2F927753-me-0308-gas-2-rcg.jpg"
    price_history = "https://cdn.forumcomm.com/dims4/default/a314711/2147483647/strip/true/crop/670x325+0+0/resize/1680x814!/format/webp/quality/90/?url=https%3A%2F%2Fforum-communications-production-web.s3.amazonaws.com%2Fbrightspot%2F51%2F8c%2F9bab38594800892f770e8350a078%2Fgas-prices-chart.gif"
    radar_chart = "https://miro.medium.com/max/1400/1*YFroPGj9dpPx7nqf045AUQ.png"

    return render_template('product.html', product_img_url = product_img_url, price_history= price_history,
                           radar_chart = radar_chart)

if __name__=='__main__':
    app.run(host='0.0.0.0',debug = True)