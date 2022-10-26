# Question : 20). WAP to convert a decimal number into its equivalent number with base b. Decimal number and b are the user input.

def reVal(num):
    if (num >= 0 and num <= 9):
        return chr(num + 48)
    else:
        return chr(num - 10 + 65)

def fromDeci(base, inputNum):
    res = ""
    while (inputNum > 0):
        res += reVal(inputNum % base)
        inputNum //= base
    res = res[::-1]
     
    return res

def convertBase(s, b):
    num=s
    ans = fromDeci(b, num)
    print(ans)
 
n = int(input("enter the number : "))
b = int(input("enter the base in which you want to change the number : "))
convertBase(n, b)
