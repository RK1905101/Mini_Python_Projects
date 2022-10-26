a=int(input("Enter 1st number :"))
b=int(input("Enter 2nd number :"))
c=input("Enter operator :")
if c=='+':
    res=a+b 
elif c=='-':
    res = a-b
elif c=='*':
    res = a*b
elif c=='/':
    res = a/b
else:
    res = "try again with correct input"

print(a,c,b ,":",res)
