from flask import Flask, render_template, url_for, flash, request, redirect
from retailnext import Covid19HoursForm, covid19hours
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'eoakzGTaCx6Xblz1Sfxb71M5hmIqL9jt'


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/experiments')
def experiments():
    return render_template("experiments.html")


@app.route('/retailnext', methods=['GET', 'POST'])
def retailnext():
    form = Covid19HoursForm()
    if form.validate_on_submit():
        custurl = form.cloudurl.data
        sftpuser = form.sftpusername.data
        sftppass = form.sftppassword.data
        csvfile = form.csvfile.data
        filename = secure_filename(csvfile.filename)
        filepath = os.path.join('uploads', filename)
        csvfile.save(filepath)
        result = covid19hours(custurl, sftpuser, sftppass, filepath)
        flash(result[0], result[1])
    return render_template("retailnext.html", form=form)


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)