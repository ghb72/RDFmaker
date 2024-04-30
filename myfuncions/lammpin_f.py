import sys, os
import random as ran
import numpy as np
from operator import itemgetter

def getStr(name):
	with open(name) as infile:
		data = infile.readlines()
	n = int(data[0])
	print(data[1], data[2])
	f = 1.0
	w = []
	atpos = []
	eleList = []
	for i in range(n):
		ele, sx, sy, sz = data[i+2].split()
		x = f*float(sx)
		y = f*float(sy)
		z = f*float(sz)
		r = np.sqrt(x*x +y*y +z*z)
		atpos.append([ele, x, y, z])
		if ele not in eleList:
			eleList.append(ele)

	return atpos, eleList


def centerStr(atpos):

	n = len(atpos)
	cx = cy = cz = 0.0
	w = []
	for i in range(n):
		ele, x, y, z = atpos[i]
		cx += x/n
		cy += y/n
		cz += z/n
	for i in range(n):
		atpos[i][1] -= cx
		atpos[i][2] -= cy
		atpos[i][3] -= cz
#	atpos.sort(key=itemgetter(3))
	for i in range(n):
		ele, x, y, z = atpos[i]
		r = np.sqrt(x*x +y*y +z*z)
		w.append([r, ele, x, y, z])
	w.sort()
	atpos = []
	for atom in w:
		atpos.append(atom[1:])
	return atpos


def rotate(atpos,angle,axis='z'):

	a = np.sin(angle)
	b = np.cos(angle)
	rm = []
	if axis == 'x':
		rm.append([1.0,0.0,0.0])
		rm.append([0.0, b ,-a])
		rm.append([0.0, a , b])
	elif axis == 'y':
		rm.append([ b ,0.0, a])
		rm.append([0.0,1.0,0.0])
		rm.append([-a ,0.0, b])
	elif axis == 'z':
		rm.append([ b ,-a ,0.0])
		rm.append([ a , b ,0.0])
		rm.append([0.0,0.0,1.0])
	for i in range(len(atpos)):
		ele,x,y,z = atpos[i]
		rotx = x*rm[0][0] + y*rm[0][1] + z*rm[0][2]
		roty = x*rm[1][0] + y*rm[1][1] + z*rm[1][2]
		rotz = x*rm[2][0] + y*rm[2][1] + z*rm[2][2]
		atpos[i] = [ele,rotx,roty,rotz]
	return atpos


def wlammpin(atpos,eleList,name):

	lin = open(name[:-4]+'.ini','w')
	print(name[:-4]+'.ini')
	n = len(atpos)
	m = len(eleList)

	w = []
	for atom in atpos:
		ele, x, y, z = atom
		w += [x,y,z]
	low = min(w) - 10.0
	high = max(w) + 10.0 

	lin.write('LAMMPS DATA FOR MEAM SIMULATION\n\n')
	lin.write('{0:7d}   atoms\n'.format(n))
	lin.write('{0:7d}   atom types\n\n'.format(m))
	lin.write('{0:8.2f}{1:8.2f}   xlo xhi\n'.format(low,high))
	lin.write('{0:8.2f}{1:8.2f}   ylo yhi\n'.format(low,high))
	lin.write('{0:8.2f}{1:8.2f}   zlo zhi\n\n'.format(low,high))
	lin.write(' Atoms\n\n')
	for i in range(n):
		ele, x, y, z = atpos[i]
		if ele == 'Ni':
			j = 1
		if (ele=='Pt'):
			j = 2 #j=1 #REAL
			#j = 1
		elif ele == 'Pd':
			#j=1
			j = 2
		elif ele == 'Co':
			j = 3
#		j = eleList.index(ele) + 1
		lin.write('{0:6d}{1:4d}{2:12.5f}{3:12.5f}{4:12.5f}\n'.format(i+1, j, x, y, z))
	lin.close()


def wXYZ(atpos):

        xyzfile = open('model.xyz','w')
        n = len(atpos)
        xyzfile.write(str(n) +'\n\n')
        for ele,x,y,z in atpos:
                xyzfile.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(ele, x, y, z))
        xyzfile.close()



def spherical_cut(atpos, radius, file_out):
    # Crear una nueva lista de posiciones atómicas que estén dentro del radio dado
    new_atpos = [atom for atom in atpos if np.sqrt(atom[1]**2 + atom[2]**2 + atom[3]**2) <= radius]

    # Escribir las nuevas posiciones atómicas en un archivo .xyz
    with open(file_out , 'w') as f:
        f.write(str(len(new_atpos)) + '\n\n')
        for atom in new_atpos:
            f.write('{0:2s}{1:12.5f}{2:12.5f}{3:12.5f}\n'.format(atom[0], atom[1], atom[2], atom[3]))

# Uso de la función
# atpos, eleList = getStr(name)  # Obtener las posiciones atómicas del archivo de entrada
# spherical_cut(atpos, radius)  # Realizar el corte esférico y escribir el nuevo archivo .xyz

def leer_xyz(nombre_archivo):
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

def calcular_rdf(atomos, nhis=6000, delr=0.01):
    npart = len(atomos)
    box = nhis * delr
    g = np.zeros(nhis)
    h = np.zeros(nhis)

    m = npart * (npart - 1) // 2
    rmin = 10.0
    rmax = 0.0
    rmed = 0.0
    hint = 0.0

    for i in range(npart - 1):
        for j in range(i + 1, npart):
            dx = atomos[i][1] - atomos[j][1]
            dy = atomos[i][2] - atomos[j][2]
            dz = atomos[i][3] - atomos[j][3]
            r = np.sqrt(dx**2 + dy**2 + dz**2)

            if r < box:
                ig = int(r / delr - 0.5)
                g[ig] += 2
                h[ig] += 2.0 / (r * delr)
                hint += 1 / r
                rmed += r
                rmin = min(rmin, r)
                rmax = max(rmax, r)

    rmed /= m
    h /= hint

    return rmin, rmax, rmed, hint, h

def suavizar(h, nh):
    k = nh // 2
    nhis = len(h)
    f = np.zeros(nhis)

    for i in range(nhis):
        x = 0.0
        for j in range(i - k, i + k + 1):
            if j >= 0 and j < nhis:
                x += h[j]
        f[i] = x / (2 * k + 1)

    return f

def run_lammpin(name):
	atpos, eleList = leer_xyz(name)
	wlammpin(atpos,eleList,name)