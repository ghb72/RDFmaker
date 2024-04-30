import random as ran
import numpy as np

def cambiar_elementos_prob(atpos:list, dict_elementos:dict):
    print(f'Cambia elementos prob a atpos')
    new_atpos = []
    new_eleList = []
    for atom in atpos:
        nuevo_elemento = ran.choices(list(dict_elementos.keys()), weights=list(dict_elementos.values()), k=1)[0]
        if ran.random() < 100*dict_elementos[nuevo_elemento]:
            new_atpos.append([nuevo_elemento, atom[1], atom[2], atom[3]])
            if nuevo_elemento not in new_eleList:
                new_eleList.append(nuevo_elemento)
        else:
            new_atpos.append(atom)
            if atom[0] not in new_eleList:
                new_eleList.append(atom[0])
    return new_atpos, new_eleList, 'rand'

def eliminar_at(atpos,percent):
    print(f'Elimina aleatoriament el {percent}% de atpos')
    new_atpos = []
    for atom in atpos:
        if ran.random() < percent:
            new_atpos.append(atom)
    return new_atpos

def pow_rad_ch(atpos:list,eleList:list,percentes:dict,Diam:float, new_element:str, inverse):
    maxrad = Diam/2
    print(f'Cambia en potencia el porcentaje radial de átomos en {percentes}')
    new_atpos=[]
    if inverse == False:
        per = percentes[new_element]
        p = (1/per)-1
        print(f'per es {per}, p es {p}')
        for atom in atpos:
            r = np.sqrt(atom[1]**2+atom[2]**2+atom[3]**2)
            x = pow(r/maxrad,3)
            y = pow(x,p)
            if ran.random() <= y:
                new_atpos.append([new_element,atom[1],atom[2],atom[3]])
                if new_element not in eleList:
                    eleList.append(new_element)
            else:
                   new_atpos.append(atom)
    elif inverse == True:
        per = 1-percentes[new_element]
        p = (1/per)-1
        print(f'per es {per}, p es {p}')
        for atom in atpos:
            r = np.sqrt(atom[1]**2+atom[2]**2+atom[3]**2)
            x = pow(r/maxrad,3)
            y = pow(x,p)
            if ran.random() >= y:
                new_atpos.append([new_element,atom[1],atom[2],atom[3]])
                if new_element not in eleList:
                    eleList.append(new_element)
            else:
                new_atpos.append(atom)
    return new_atpos,eleList,'pow'

def pol_ab_rad_ch(atpos:list,eleList:list,percentes:dict,Diam:float, new_element:str, a:float, b:float):
    maxrad = Diam/2
    print(f'Cambia en potencia el porcentaje radial de átomos en {percentes}')
    new_atpos=[]
    per = percentes[new_element]
    p = a/(per-b)-1
    print(f'per es {per}, p es {p}')
    for atom in atpos:
        r = np.sqrt(atom[1]**2+atom[2]**2+atom[3]**2)
        x = pow(r/maxrad,3)
        y = a*pow(x,p)+b
        if ran.random() <= y:
            new_atpos.append([new_element,atom[1],atom[2],atom[3]])
            if new_element not in eleList:
                eleList.append(new_element)
        else:
            new_atpos.append(atom)
    print(a*pow(0.25,p)+b,a*pow(0.5,p)+b,a*pow(0.75,p)+b,a*pow(1,p)+b)
    return new_atpos,eleList,'pow'


def help():
    print('dict_elementos or percentes = {"Pt":0.25,"Ni":0.75} ')