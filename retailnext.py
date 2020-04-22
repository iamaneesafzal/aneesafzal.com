from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length
import paramiko, pandas as pd


class Covid19HoursForm(FlaskForm):
    cloudurl = StringField("Cloud Sub-domain",
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    sftpusername = StringField(
        "sFTP Username", validators=[DataRequired(),
                                     Length(min=2, max=20)])
    sftppassword = PasswordField("sFTP Password", validators=[DataRequired()])
    csvfile = FileField('CSV File', validators=[FileRequired()])


def covid19hours(custurl, sftpuser, sftppass, csvfile):
    output_list = []
    try:
        with open(csvfile, "r", encoding="utf-8-sig") as rfile:
            inputfile = pd.read_csv(rfile)
            inputfile.columns = ["StoreID", "StartDate", "EndDate"]
        for a, b in inputfile.iterrows():
            datelist = pd.date_range(b["StartDate"], b["EndDate"]).tolist()
            for date in datelist:
                output_list.append(
                    [b["StoreID"],
                     str(date)[:10], "00:00:00", "00:00:00"])
        df = pd.DataFrame(output_list,
                          columns=["StoreID", "Date", "Opening", "Closing"])
        df.to_csv(f"/tmp/new_store_exception_hours_{csvfile[8:]}", index=False)
    except:
        return "Couldn't fix the file! Please check the File Format", "danger"
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            custurl + ".store-hours.retailops.io",
            username=sftpuser,
            password=sftppass,
            port=2022,
        )
        sftp = ssh.open_sftp()
        sftp.chdir("/storehours_uploads/" + custurl)
        sftp.put(
            f"/tmp/new_store_exception_hours_{csvfile[8:]}",
            f"new_store_exception_hours_{csvfile[8:]}",
            confirm=False,
        )
        sftp.close()
        ssh.close()
        return "File uploaded to the cloud", "success"
    except:
        return "Error occured! Please check sFTP details", "danger"
