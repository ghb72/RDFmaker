import numpy as np


def janus(atpos, z1, newel):
    new_atpos = []
    for atom in atpos:
        if atom[1]<z1:
            new_atpos.append([newel, atom[1], atom[2], atom[3]])
        else:
            new_atpos.append(atom)
    return new_atpos

def sandwich(atpos,z1,z2, newel):
    if z2 < z1 or z1 == z2:
        print('wrong values, is necessary z1 < z2')
        exit()
    new_atpos = []
    for atom in atpos:
        if float(atom[3]) < z1 and float(atom[3]) > z2:
            new_atpos.append([newel, atom[1], atom[2], atom[3]])
        else:
            new_atpos.append(atom)
    return new_atpos

def capas(atpos, r1, r2, newel):
    if r1 > r2 or r1 == r2:
        print('wrong values, is necessary r1 > r2')
        exit()
    new_atpos=[]
    for atom in atpos:
        r = np.sqrt(atom[1]**2 +atom[2]**2+atom[3]**2)
        if (r>r1 and r<=r2):
            new_atpos.append([newel, atom[1], atom[2], atom[3]])
        else:
            new_atpos.append(atom)
    return new_atpos

def radcut(atpos, r1, r2):
    if r1>r2 or r1==r2:
        print('wrong values, is necessary r1 > r2')
        exit()
    new_atpos=[]
    for atom in atpos:
        r = np.sqrt(atom[1]**2 +atom[2]**2+atom[3]**2)
        #print(r)
        if (r>r1 and r<=r2):
            #print('b')
            new_atpos.append(atom)
    return new_atpos

def makesmall(atpos,r1):
    if r1 <= 0: 
        print('wrong value of radius: it needs r>0')
        exit()
    new_atpos = []
    for atom in atpos:
        r = np.sqrt(atom[1]**2 +atom[2]**2+atom[3]**2)
        #print(r)
        if (r<=r1):
            new_atpos.append(atom)
    return new_atpos