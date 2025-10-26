def attack_cs(o,p,q):
    if (o[1]=="l"):
        if o[0]=='r':
            q[0]=q[0]+p[1]
        else:
            q[0]=q[0]+p[0]
    elif (o[1]=='r'):
         if o[0]=='r':
            q[1]=q[1]+p[1]
         else:
             q[1]=q[1]+p[0]
    else:
        pass
     
    return(p,q)
        
    