from flask import Flask, render_template,send_from_directory
import os

member_folder = os.path.join('static','member_folder')

app = Flask(__name__)
app.config['mbr_folder'] = member_folder


@app.route("/")
def basic():
    return "<p>Do not buy it!</p>"

@app.route("/about")
def following():
    full_filename = os.path.join(app.config['mbr_folder'], 'yunhe.png')
    return render_template('about_page.html',user_image = full_filename)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)