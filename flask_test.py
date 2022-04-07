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
    suggestion = []
    top10 = []
    suggestion.append({'name':'Samsung','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6452/6452997_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/samsung.png'})
    suggestion.append({'name':'Sony','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6453/6453619_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/sony.png'})
    suggestion.append({'name':'Lg','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6458/6458623_sd.jpg;maxHeight=640;maxWidth=550','profile':'/static/item_folder/lg.png'})
    top10.append({'name':'TCL','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6470/6470251_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/tcl.png'})
    top10.append({'name':'Insignia','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6456/6456970_sd.jpg;maxHeight=640;maxWidth=550','img':'/static/item_folder/insignia.png'})
    top10.append({'name':'VIZIO','img_address':'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6459/6459559_sd.jpg;maxHeight=640;maxWidth=550','profile':'/static/item_folder/vizio.png'})
    return render_template('main.html',suggestion = suggestion, top10=top10)
    

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