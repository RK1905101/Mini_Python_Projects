import pandas as pd
import datetime
import smtplib
import os 

os.chdir(r"D:\Automatic Birthday Wisher")
# os.mkdir("testing")

def sendEmail(to, sub, msg):
    # Enter your authentication details
    GMAIL_ID = 'test@gmail.com'
    GMAIL_PSWD = 'password@123'
    print(f"Email to {to} sent with subject: {sub} and message {msg}")
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls()
    s.login(GMAIL_ID, GMAIL_PSWD)

    s.sendmail(GMAIL_ID, to, f"Subject: {sub}\n\n{msg}")
    s.quit()
if __name__ == "__main__":
    df = pd.read_excel("data.xlsx")
    # print(df)
    today = datetime.datetime.now().strftime("%d-%m")
    yearNow = datetime.datetime.now().strftime("%Y")
    # print(today)
    writeInd = []  # Prevent the code to send birthday wish to the person if he has already been wished in that year
    for index, item in df.iterrows():
        # print(index, item['Birthday'])
        bday = item['Birthday'].strftime("%d-%m")
        # print(bday) 
        if(today == bday) and yearNow not in str(item['Year']):
            sendEmail(item['Email'], "Happy Birthday!", item['Dialogue'])
            writeInd.append(index)
    # print(writeInd)
    for i in writeInd:
        if len(writeInd)==0:
            break
        yr =df.loc[i, 'Year']
        df.loc[i, 'Year'] = str(yr) + ',' + str(yearNow)
        # print(df.loc[i, 'Year'])
    
    # print(df) 
    df.to_excel('data.xlsx', index = False)   # pip install openpyxl
         
