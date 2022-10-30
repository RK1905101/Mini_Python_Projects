# Question : A Python Program using class and object to deposit or withdraw money in a bank account.
        # If the balance is 0 -> Display as ”New Account Created” If the balance is credited with some amount-> Show the New Balance
        # If the balance is debited with some amount-> Show the New Balance
class Account:
	def __init__(self):
		self.balance=0
		print("Congratulations !! New Account Created.")

	def credit(self):
		amount=float(input("Enter amount to be credited: "))
		self.balance += amount
		print("\nAmount Credited:",amount)

	def debit(self):
		amount = float(input("Enter amount to be debitted: "))
		if self.balance>=amount:
			self.balance-=amount
			print("\nYou debitted:", amount)
		else:
			print("\nInsufficient balance ")

	def display(self):
		print("\nNet Available Balance=",self.balance)

s = Account()
s.credit()
s.display()
s.debit()
s.display()