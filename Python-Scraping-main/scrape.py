import requests
from bs4 import BeautifulSoup

branch = 'ee'
rStart = 1
rEnd = 127

rollno = "21b"+branch
url = 'http://14.139.56.19/scheme21/studentresult/result.asp'


def find_cgpa(roll):

    student = []

    data = {
        'RollNumber': roll
    }
    p = requests.post(url, data)
    soup = BeautifulSoup(p.content, 'html.parser')

    cgpa = soup.find_all(class_="formSetting")
    # print(cgpa)
    for i in cgpa:
        student.append(i.string)
    x, cgpa = student[9].split('=')
    print('{"roll":'+f'"{student[1].strip()}"'+',')
    print('"name":'+f'"{student[3].strip()}"'+',')
    print('"cgpa":'+f'"{cgpa}"'+'},\n')


for i in range(rStart, rEnd+1):
    try:
        if i <= 9:
            find_cgpa(rollno + "00"+str(i))
        elif i <= 99:
            find_cgpa(rollno + "0"+str(i))
        else:
            find_cgpa(rollno + str(i))
    except:
        continue
