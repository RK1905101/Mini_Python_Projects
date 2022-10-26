# Question : 9) Write a Python function to implement Binary Search without using recursion.

def bs(l, elem):
   low = 0
   high = len(l) - 1
   mid = 0
   while low <= high:
      mid = (high + low) // 2
      if l[mid] < elem:
         low = mid + 1
      elif l[mid] > elem:
         high = mid - 1
      else:
         return mid
   return -1

l = [ 1, 9, 11, 21, 5, 15, 25, 50, 34, 54, 67, 90 ]
e = int(input("Enter number:"))
res = bs(l, e)

if res != -1:
   print("found at index ", str(res))
else:
   print("Not found!")
