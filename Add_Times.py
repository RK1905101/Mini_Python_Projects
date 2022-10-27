print("Enter 1st time :")
h1=int(input("hour : "))
m1=int(input("minute : "))
s1=int(input("second : "))
print("Enter 2nd time :")
h2=int(input("hour : "))
m2=int(input("minute : "))
s2=int(input("second : "))
h3=h1+h2+(m1+m2+(s1+s2)//60)//60
m3=(m1+m2+(s1+s2)//60)%60
s3=(s1+s2)%60
print("Total Time  :",h3," Hour &",m3," Minute and ",s3,"Second")
