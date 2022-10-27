# Question : WAP to convert a number with base b into its equivalent decimal number. Numbers with base b &amp; b are the user input.

def val(c):
    if (c >= '0' and c <= '9'):
        return ord(c) - 48
    else:
        return ord(c) - 65  + 10

def toDeci(strr, base):
    lenn = len(strr)
    power = 1
    num = 0
    for i in range(lenn - 1, -1, -1):
        if (val(strr[i]) >= base):
            print("Invalid Number")
            return -1
             
        num += val(strr[i]) * power
        power = power * base
    print(num)
 
s = input("enter the number : ")
b = int(input("enter the base in which you enterd the number : "))
toDeci(s, b)
