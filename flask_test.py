from flask import Flask, render_template,send_from_directory
# import os

# member_folder = os.path.join('static','member_folder')

app = Flask(__name__)
# app.config['mbr_folder'] = member_folder


@app.route("/")
def basic():
    return render_template("main.html")
    

@app.route("/about")
def following():
    member_list = []
    member_list.append({'name':'Muhuan Lyu','role':'CEO','linkedin':'https://www.linkedin.com/in/yunhe-j-380651172/','profile':'/static/member_folder/david.png'})
    member_list.append({'name':'You Wu','role':'CTO','linkedin':'https://www.linkedin.com/in/you-yoli-wu/','profile':'/static/member_folder/yoli.png'})
    member_list.append({'name':'Young','role':'COO','linkedin':'https://www.linkedin.com/in/yunhe-j-380651172/','profile':'/static/member_folder/david.png'})
    member_list.append({'name':'Chandan Nayak','role':'Product Manager','linkedin':'https://www.linkedin.com/in/yunhe-j-380651172/','profile':'/static/member_folder/david.png'})
    member_list.append({'name':'Yunhe Jia','role':'Software Engineer','linkedin':'https://www.linkedin.com/in/yunhe-j-380651172/','profile':'/static/member_folder/yunhe.png'})
    member_list.append({'name':'Meilin Li','role':'Data Scientist','linkedin':'https://www.linkedin.com/in/li-meilin','profile':'/static/member_folder/david.png'})
    member_list.append({'name':'Jaysen Shi','role':'Data Engineer','linkedin':'https://www.linkedin.com/in/jaysenshi/','profile':'/static/member_folder/david.png'})
    return render_template('about_page.html',member_list = member_list)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)