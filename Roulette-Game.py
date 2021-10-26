from random import randint

totalAmount=1000                            #total amount invested 

while totalAmount > 0:
    print("Welcome !!!\nYou have", totalAmount,"€. Good Luck !!\n_________________________________")
    selectedNumber=int(input("\nOn which number do you want to bet ?"))
    
    x=0
    x=selectNumber
    if x < 0 or x > 49:
        print("You have to bet a number between 0 and 49")
    
    bettingAmount=int(input("How much do you want to bet on this number?"))
    numberOutput = randint(0, 49)           # line to use to generate a random number between 0 and 49
    print("\nThe number output is",numberOutput)
    
    if numberOutput == selectedNumber:
        print("You Win!!!\n_________________________________")
    
    else:
        print("Sorry but you lost, try again !")
        totalAmount-=bettingAmount
        print("\nYou now have",totalAmount,"€ left\n_________________________________")
        
if totalAmount==0:
    print("Sorry but you don't have enough money to continue !\nThe game is now ending !")