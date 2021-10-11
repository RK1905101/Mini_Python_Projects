import time

print(" Welcome To the Coder's ATM")

username_list = [ "user1" , "user2" , "user3"] 
password_user1 = 3457
password_user2 = 5364
password_user3 = 7574


time.sleep(1)

def task_user1():
	balance_user1 = 1000000
	task = int(input(" Check Balance [1]\nWithdraw [2]\nDeposit [3] \n "))
	if task == 1:
		print("Your Balance : " , balance_user1)
	elif task == 2:
		amount = int(input("Enter the amount you want to Withdraw : "))
		balance_user1 = balance_user1 - amount
		print("You have Successfully withdrawn " , amount)
		print("Your Balance : " , balance_user1)
	elif task == 3:
		depo = int(input("Enter the amount you want to Deposit : "))
		balance_user1 = balance_user1 + depo
		print("You have Successfully Deposited " , depo)
		print("Your Balance : " , balance_user1)


def task_user2():
	balance_user2 = 5600600
	task = int(input(" Check Balance [1]\nWithdraw [2]\nDeposit [3] \n "))
	if task == 1:
		print("Your Balance : " , balance_user2)
	elif task == 2:
		amount = int(input("Enter the amount you want to Withdraw : "))
		balance_user1 = balance_user2 - amount
		print("You have Successfully withdrawn " , amount)
		print("Your Balance : " , balance_user2)
	elif task == 3:
		depo = int(input("Enter the amount you want to Deposit : "))
		balance_user1 = balance_user2 + depo
		print("You have Successfully Deposited " , depo)
		print("Your Balance : " , balance_user2)


def task_user3():
	balance_user3 = 100000000
	task = int(input(" Check Balance [1]\nWithdraw [2]\nDeposit [3] \n "))
	if task == 1:
		print("Your Balance : " , balance_user3)
	elif task == 2:
		amount = int(input("Enter the amount you want to Withdraw : "))
		balance_user1 = balance_user3 - amount
		print("You have Successfully withdrawn " , amount)
		print("Your Balance : " , balance_user3)
	elif task == 3:
		depo = int(input("Enter the amount you want to Deposit : "))
		balance_user1 = balance_user3 + depo
		print("You have Successfully Deposited " , depo)
		print("Your Balance : " , balance_user3)


username = input("Enter Your Username : ")

if username in username_list:
	print("Welcome " , username)
	password = int(input("Enter Your Password : "))
	if username == "user1":
		if password == password_user1:
			print("Welcome User1 , Your Password is Correct ", )
			task_user1()
		else:
			print("Wrong Password")
	elif username == "user2":
		if password == password_user2:
			print("Welcome User1 , Your Password is Correct ", )
			task_user2()
		else:
			print("Wrong Password")
	elif username == "user3":
		if password == password_user3:
			print("Welcome User1 , Your Password is Correct ", )
			task_user3()
		else:
			print("Wrong Password")
    
else:
	print("Wrong Userame Detected")
