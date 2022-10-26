# Question : WAP in python with class Bill. The users have the option to pay the bill by card or by cash. Use the inheritance to model this situation.

class ClassBill:
    def __init__(self, bill):
        self.bill = bill

    def card(self):
      print("amount payed by card")

    def cash(self):
      print("amount payed by cash")


class Card(ClassBill):
    def __init__(self, bill):
        ClassBill.__init__(self, bill)
        
    def message(self):
        ClassBill.card(self)


class Cash(ClassBill):
    def __init__(self, bill):
        ClassBill.__init__(self, bill)
        
    def message(self):
        ClassBill.cash(self)

payment = int(input("Enter your payment amount : "))
choice = input("Enter your payment choice : ")
if(choice == "cash"):
  ca = Cash(payment)
  ca.message()
else:
  ca = Card(payment)
  ca.message()
