import paramiko, pandas as pd

customer = "xxx"  ### url of the cloud

### CSV Upload FTP details

ftpdetails = {"user": "retailnext", "pass": "tKbxwz"}

output_list = []

with open("storehours/storesclosures_magrabi.csv", "r",
          encoding="utf-8-sig") as rfile:
    inputfile = pd.read_csv(rfile)
    for a, b in inputfile.iterrows():
        datelist = pd.date_range(b["StartDate"], b["EndDate"]).tolist()
        for date in datelist:
            output_list.append(
                [b["StoreID"],
                 str(date)[:10], "00:00:00", "00:00:00"])
df = pd.DataFrame(output_list,
                  columns=["StoreID", "Date", "Opening", "Closing"])
df.to_csv("storehours/new_store_exception_hours_covid19.csv", index=False)


def file_upload():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        customer + ".store-hours.retailops.io",
        username=ftpdetails["user"],
        password=ftpdetails["pass"],
        port=2022,
    )
    sftp = ssh.open_sftp()
    sftp.chdir("/storehours_uploads/" + customer)
    sftp.put(
        "storehours/new_store_exception_hours_covid19.csv",
        "new_store_exception_hours_covid19.csv",
        confirm=False,
    )
    sftp.close()
    ssh.close()
    print("Success")


file_upload()


def testfunction(a, b, c, d):
    return a, b, c, d
