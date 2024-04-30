import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from sys import argv
from myfuncions.tools_f import leer_xyz

def atomos_por_radio(atpos:list, elemento_interes:str):
    radios = defaultdict(int)
    rad_tot = defaultdict(int)
    for atomo in atpos:
        r = np.sqrt(atomo[1]**2 + atomo[2]**2 + atomo[3]**2)
        rad_tot[r] += 1
        if atomo[0] == elemento_interes:
            radios[r] += 1
        else: radios[r] += 0
    rad_tot_o = sorted(rad_tot.items())
    radios_ordenados = sorted(radios.items())
    rad_tot, conteo_tot = zip(*rad_tot_o)
    radios, conteo = zip(*radios_ordenados)
    return rad_tot, conteo_tot, radios, conteo

def fracc_atomos_por_radio(atpos:list, elemento_interes:str):
    conteo_atomos = defaultdict(int)
    conteo_total = defaultdict(int)
    radios = []
    for atomo in atpos:
        conteo_total[np.sqrt(atomo[1]**2+atomo[2]**2+atomo[3]**2)] += 1
        if atomo[0] == elemento_interes:
            conteo_atomos[np.sqrt(atomo[1]**2+atomo[2]**2+atomo[3]**2)] += 1
    radios_ordenados = sorted(conteo_total.items())
    radios, conteo_total = zip(*radios_ordenados)
    proporciones = [conteo_atomos[radio] / total for radio, total in zip(radios, conteo_total)]
    return radios, proporciones

def graficar_at_p_rad(atpos:list, elemento_interes:str):
    rad_tot, conteo_tot, radios, conteo = atomos_por_radio(atpos,elemento_interes)
    fig, ax =plt.subplots(figsize=(5,5), layout='constrained')
    ax.plot(rad_tot, conteo_tot, label=('Total'), color = 'black')
    ax.plot(radios, conteo, label=('Átomos de ' + elemento_interes), color='red')
    ax.set_xlabel('Radio [$\\AA$]')
    ax.set_xlim([0,16])
    ax.set_ylabel('Átomos por capa')
    ax.set_title('Cantidad de Átomos de ' + elemento_interes + ' por Radio')
    ax.legend()
    plt.show()

def graficar_fracc_at_p_rad(atpos:list,elemento_interes:str):
    rads, proporciones = fracc_atomos_por_radio(atpos,elemento_interes)
    fig, ax =plt.subplots(figsize=(5,5), layout='constrained')
    ax.plot(rads, proporciones, color='black')
    ax.set_xlabel('Radio[$\\AA$]')
    ax.set_ylabel('Fracción de Átomos de '+ elemento_interes)
    ax.set_title('Fracción de Átomos de ' + elemento_interes + ' por Radio')
    ax.legend()
    plt.show()

def plot_fracc_y_at_p_rad(atpos:list,elemento_interes:str):
    rad_tot, conteo_tot, radios, conteo = atomos_por_radio(atpos,elemento_interes)
    rads, proporciones = fracc_atomos_por_radio(atpos, elemento_interes)

    fig, ax =plt.subplots(2,1,figsize=(10,5), layout='constrained')
    ax[0].plot(rad_tot, conteo_tot, label=('Total'), color = 'black')
    ax[0].plot(radios, conteo, label=('Átomos de ' + elemento_interes), color='red')
    ax[0].set_xlabel('Radio [$\\AA$]')
    ax[0].set_xlim([0,16])
    ax[0].set_ylabel('Átomos por capa')
    #ax[0].set_title('Cantidad de Átomos de ' + elemento_interes + ' por Radio')
    ax[0].legend()

    ax[1].plot(rads, proporciones, color='black')
    ax[1].set_xlabel('Radio[$\\AA$]')
    ax[1].set_ylabel('Fracción de Átomos de '+ elemento_interes)

    fig.suptitle('Fracción y Átomos por radio')
    plt.show()

def dump_fracc_atpr(atpos:list, elemento_interes:str, dr:float):
    atpos1 = []
    for atom in atpos:
        atpos1.append([atom[0], np.sqrt(atom[1]**2+atom[2]**2+atom[3]**2)]) # append el elemento y su radio
    radios = []
    r = 0
    atpos_ordenados = sorted(atpos1,key=lambda at:at[1])
    conteo_total =[]
    conteo_interes = []
    fracc = []
    while r<=atpos_ordenados[-1][1]+dr:
        radios.append(r)
        c = 0
        porcent = 0
        for atom in atpos_ordenados:
            if r <= atom[1] and atom[1] <= r+dr:
                c = c + 1
                if atom[0] == elemento_interes:
                    porcent = porcent + 1
        conteo_interes.append(porcent)
        porcent = (porcent/c if c>0 else 0)
        fracc.append(porcent)
        conteo_total.append(c)

        r = r + dr
    return radios, fracc, conteo_total, conteo_interes

def dump_graficar_fracc_atpr(atpos:list, elemento_interes:str, dr:float):
    radios, fracc, conteo_total, conteo_interes = dump_fracc_atpr(atpos, elemento_interes, dr)
    fig, ax =plt.subplots(figsize=(5,5), layout='constrained')
    ax.plot(radios, fracc, color='black')
    ax.set_xlabel('Radio[$\\AA$]')
    ax.set_ylabel('Fracción de Átomos de '+ elemento_interes)
    ax.set_title('Fracción de Átomos de ' + elemento_interes + ' por entre $r$ y $r+\Delta r$')
    ax.text(1,0.5,f'$\Delta r = {dr} \AA$', va='bottom')
    ax.legend()
    plt.show()

def dump_graficar_atpr(atpos:list, elemento_interes:str, dr:float):
    radios, fracc, conteo_total, conteo_interes = dump_fracc_atpr(atpos, elemento_interes, dr)
    fig, ax =plt.subplots(figsize=(5,5), layout='constrained')
    ax.plot(radios, conteo_total, label=('Total'), color = 'black')
    ax.plot(radios, conteo_interes, label=('Átomos de ' + elemento_interes), color='red')
    ax.set_xlabel('Radio [$\\AA$]')
    #ax.set_xlim([0,16])
    ax.set_ylabel('Átomos por r')
    ax.set_title('Cantidad de Átomos de ' + elemento_interes + ' entre $r$ y $r+\Delta r$')
    ypos_text = max(conteo_total)/2
    ax.text(1,ypos_text,f'$\Delta r = {dr} \AA$', va='bottom')
    ax.legend()
    plt.show()

def plot_dump_f_y_atpr(atpos:list, elemento_interes:str, dr:float):
    radios, fracc, conteo_total, conteo_interes = dump_fracc_atpr(atpos, elemento_interes, dr)
    fig, ax =plt.subplots(2,1,figsize=(10,5), layout='constrained')
    ax[0].plot(radios, conteo_total, label=('Total'), color = 'black')
    ax[0].plot(radios, conteo_interes, label=('Átomos de ' + elemento_interes), color='red')
    ax[0].set_xlabel('Radio [$\\AA$]')
    #ax[0].set_xlim([0,16])
    ax[0].set_ylabel('Átomos por radio')
    #ax[0].set_title('Cantidad de Átomos de ' + elemento_interes + ' por Radio')
    ax[0].legend()

    ax[1].plot(radios, fracc, color='black')
    ax[1].set_xlabel('Radio[$\\AA$]')
    ax[1].set_ylabel('Fracción de Átomos de '+ elemento_interes)

    fig.suptitle(f'Fracción y Átomos de interés entre $r$ y $r+\Delta r$, $\Delta r = {dr} \AA$')
    plt.show()

if __name__ == '__main__':
    name = argv[1]
    elemento= argv[2]
    atpos, eleList = leer_xyz(name)
    plot_fracc_y_at_p_rad(atpos,elemento)