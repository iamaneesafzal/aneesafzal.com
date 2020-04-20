from flask import Flask, render_template, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, regexp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'eoakzGTaCx6Xblz1Sfxb71M5hmIqL9jt'


class Covid19HoursForm(FlaskForm):
    cloudurl = StringField("Cloud Sub-domain",
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    sftpusername = StringField(
        "sFTP Username", validators=[DataRequired(),
                                     Length(min=2, max=20)])
    sftppassword = PasswordField("sFTP Password", validators=[DataRequired()])
    csvfile = FileField('CSV File')
    submit = SubmitField("Upload File")


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
        return 'File uploaded to the cloud!'
    return render_template("retailnext.html", form=form)


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)