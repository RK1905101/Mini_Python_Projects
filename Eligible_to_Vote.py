# Question : 3) WAP in python has a class Person storing name and date of birth of a person. The program should subtract the date of birth from today’s date to find out if the personis eligible to vote or not.
import datetime

class person():
    def __init__(self, name, dob):
        self.name=name
        self.dob=dob
    def check(self):
        today=datetime.date.today()
        age=today.year-self.dob.year
        if today< datetime.date(today.year, self.dob.month, self.dob.day):
            age-=1
        if age>=18:
            print(self.name, " , Congratulation! You are eligible to vote.")
        else:
            print(self.name, " , Sorry! You should be at least 18 years of age.")

name = input("Enter your name : ") 
date_of_birth_year = int(input("Enter year : "))
date_of_birth_month = int(input("Enter month : ")) 
date_of_birth_day = int(input("Enter day : ")) 

p=person(name, datetime.date(date_of_birth_year, date_of_birth_month, date_of_birth_day))

p.check()
