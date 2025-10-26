import itertools
def split_cs(x,y):
    if x[0]=='l':
        y[0]=y[0]-int(x[2])
        y[1]=y[1]+int(x[2])
    elif x[0]=='r':
        y[1]=y[1]-int(x[1])
        y[0]=y[0]+int(x[1])
    else:
        pass
    return(y)
        
    
    
    