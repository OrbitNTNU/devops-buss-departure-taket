import random

def chooseRandomPicture(base):
    maxChanse=0
    for i in base:
        if type(i)!=type(1):
            maxChanse+=i[-1]

    nr=random.randint(0,maxChanse)

    chosen=""
    goneByNr=0
    at=0
    while chosen=="":
        if base[at][-1]+goneByNr>=nr:
            chosen=base[at]
        goneByNr+=base[at][-1]
        at+=1
    
    if type(base[0][0])==type(""):
        return chosen[0]
    else:
        return chooseRandomPicture(chosen)