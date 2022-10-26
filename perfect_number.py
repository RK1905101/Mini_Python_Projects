# Question : 13)Write a function to check if a given number is perfect or not. The first perfect number is 6, because 1, 2,and 3 are its proper positive divisors, and 1 + 2 + 3 = 6*/

def perfect(n):
    sum = 0
    for x in range(1, n):
        if n % x == 0:
            sum += x
    return sum == n

num=int(input("Enter Number : "))
if perfect(num):
    print("perfect")
else:
    print("Not Perfect")
