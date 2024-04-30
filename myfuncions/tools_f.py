import sys, os
import random as ran
import numpy as np

def leer_xyz(nombre_archivo:str):
    with open(nombre_archivo) as f:
        lineas = f.readlines()
    num_atomos = int(lineas[0])
    atpos = []
    eleList = []
    for linea in lineas[2:2 + num_atomos]:
        partes = linea.split()
        elemento = partes[0]
        x, y, z = map(float, partes[1:])
        atpos.append([elemento, x, y, z])
        if elemento not in eleList:
            eleList.append(elemento)
    return atpos, eleList

def wXYZ(atpos:list,name_out:str):

        xyzfile = open(name_out,'w')
        n = len(atpos)
        xyzfile.write(str(n) +'\n\n')
        for ele,x,y,z in atpos:
                xyzfile.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(ele, x, y, z))
        xyzfile.close()

def cambiar_etiquetas_xyz(atpos:list, eleList:list, dict_etiquetas:dict):
    new_atpos=[]
    print(f'Cambia etiquetas a "atpos"')
    for atom in atpos:
        try:
            el = int(atom[0])
        except:
            el = atom[0]
        if el in dict_etiquetas:
            elemento = dict_etiquetas[el]
        else:
            print(f"Advertencia: No se encontró la etiqueta {el} en el diccionario de etiquetas. Se usará la etiqueta original.")
            elemento = str(el)
        new_atpos.append([elemento, atom[1], atom[2], atom[3]])

    new_eleList =[]
    for ele in eleList:
        try:
            el = int(ele)
        except: el = ele
        if el in dict_etiquetas:
            elemento = dict_etiquetas[el]
        else:
            print(f"Advertencia: No se encontró la etiqueta {el} en el diccionario de etiquetas. Se usará la etiqueta original.")
            elemento = str(el)
        new_eleList.append(el)

    print('jala')
    return new_atpos, new_eleList

def show_percent(atpos:list, eleList:list):
    tot = len(atpos)
    print(f'atomos totales : {tot}')
    for element in eleList:
        empty = []
        for atom in atpos:
            if atom[0] == element:
                empty.append(atom[0])
        percentes=len(empty)
        print(f'{element} : {100*percentes/tot} %, {percentes}')

def spherical_cut(atpos:list, eleList:list, radius:float):
    print(f'Corta esfericamente al atpos')
    new_atpos = [atom for atom in atpos if np.sqrt(atom[1]**2 + atom[2]**2 + atom[3]**2) <= radius]
    return new_atpos, eleList