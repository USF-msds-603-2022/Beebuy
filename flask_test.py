from flask import Flask,  render_template
from wtforms.fields import *
from flask_wtf import FlaskForm, CSRFProtect
from flask_bootstrap import Bootstrap4, SwitchField

# import os

# member_folder = os.path.join('static','member_folder')

app = Flask(__name__)
app.secret_key = 'dev'
# app.config['mbr_folder'] = member_folder
bootstrap = Bootstrap4(app)
csrf = CSRFProtect(app)

class SearchBar(FlaskForm):
    search = SearchField()

@app.route("/")
def basic():
    return render_template("main.html")
    

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



if __name__=='__main__':
    app.run(host='0.0.0.0',debug = True)