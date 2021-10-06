#!/usr/bin/env python
# coding: utf-8

# In[1]:


import split
import attack
a=[1,1]
b=[1,1]
print("player 1:",a,"\nplayer 2:",b)
def calculate(x,y):
    p1=input("enter the move of player : Attack or Split:")
    if p1=='A' or p1=='a':
            l=list(input("enter the move combination to attack:").split())
            m=attack.attack_cs(l,x,y)
            x=m[0]
            y=m[1]
            for i in range(len(y)):
                if y[i]>=5:
                    y[i]=0
    elif p1=='S' or p1=='s':
            l=list(input("enter the move combination to split:").split())
            m=split.split_cs(l,x)
            x=m
    else:
        print('invalid move')
        
def rollover():
    global a,b
    p=int(input("enter the player number:"))
    if p==1:
        calculate(a,b)
        print("player 1:",a,"\nplayer 2:",b)
    else:
        calculate(b,a)
        print("player 1:",a,"\nplayer 2:",b)
    
def status(a,b):
    rollover()
    if sum(a)==0:
        print("player 2 wins")
    elif sum(b)==0:
        print("player 1 wins")
    else:
        status(a,b)
status(a,b)       
        


# In[ ]:




