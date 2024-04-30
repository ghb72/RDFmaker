import pandas as pd
from myfuncions.tools_f import leer_xyz
import numpy as np

class diffractin_powers:
    def __init__(self,element,Z_number) -> None:
        self.element = element
        self.Z_number = Z_number
    
    def show_diff_powers(self):
        print()

atpos, eleList = leer_xyz(name)

dif_powers = {'Ni':28, 'Pt':78, 'Co':28, 'Pd':46}



def hist(atpos:list, nhis:int, dr:float):
    n_atom = len(atpos) # number of atoms
    B = 0
    for i in range(n_atom):
        B = B + dif_powers[atpos[i][0]]
    
    m = n_atom*(n_atom-1)/2
    B = B/m

    rmin = 10.0
    rmed = 0.0
    rmax = 0.0
    hint = 0.0
    box = dr*nhis

    hist = np.zeros(nhis)

    for i in range(0,n_atom-1):
        for j in range(i+1, n_atom):
            bij = dif_powers[atpos[i][0]]*dif_powers[atpos[i][0]]/(B*B)
            dx = atpos[i][1]-atpos[j][1]
            dy = atpos[i][2]-atpos[j][2]
            dz = atpos[i][3]-atpos[j][3]
            d = np.sqrt(dx*dx + dy*dy + dz*dz)
            if d<box: print(i,j, atpos[i], atpos[j])
            elif d<box:
                ig = int(d/dr - 0.5)
                hist[ig] = hist[ig] + 2*bij/(d*dr)
                hint = hint + 1/d
                rmed = rmed + d
                if d < rmin: rmin = d
                elif d > rmax: rmax = d
            else: print('El tamaño del sistema supera los parámetros', d, '>', box)
    
    rmed = rmed/m
    hist = hist/hint

    print(n_atom,' atomos ',m,' pares ')
    print('Rango de distancias ',rmin,'-',rmax)
    print('Distancias promedio ',rmed)
    print('Factor de normalizacion ',hint)
    return hist


if __name__ == __main__:
    name = str(input('Name of .xyz file: '))