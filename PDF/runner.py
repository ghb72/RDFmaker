#import sys
import os
import subprocess
from os import scandir, getcwd

def file_list(path=getcwd()):
    return [arch.name for arch in scandir(path) if arch.is_file()]

def getpath():
    print(os.getcwd())

def run_pdf(name:str, path:str, nhis:int, dr:float):
    new_filename=path+'\\'+name
    print(os.getcwd())
    with open('..\\..\\PDF\\rdf.f90', 'r') as f: # rdf.f90 for dump and rdf1.f90 for shell (no MD)
        lines = f.readlines()
    with open('temp_rdf.f90', 'w') as f:
        for line in lines:
            if "file='shell.xyz'" in line:
                line = line.replace("file='shell.xyz'", f"file='{new_filename}'")
            if "nhis=2600" in line:
                line = line.replace("nhis=2600", f"nhis={nhis}")
            if "file='rdf.txt'" in line:
                line = line.replace("file='rdf.txt'", f"file='{name[:-4]+'.txt'}'")
            if "delr = 0.02" in line:
                line = line.replace("delr = 0.02",f"delr = {dr}")
            f.write(line)
    resultado = subprocess.run(['gfortran','temp_rdf.f90', '-o', 'rdf'], capture_output=True)
    print(resultado.stdout.decode())
    resultado2 = subprocess.run(['./rdf.exe'], capture_output=True)
    print(resultado2.stdout.decode())
    #os.remove('temp_rdf.f90')
    #os.remove('rdf.exe')

def run_pdf_noMD(name:str, path:str, nhis:int, dr:float, smooth1:float, smooth2:float):
    new_filename=path+'\\'+name
    print(os.getcwd())
    with open('..\\..\\PDF\\rdf_noMD.f90', 'r') as f: # rdf.f90 for dump and rdf1.f90 for shell (no MD)
        lines = f.readlines()
    with open('temp_rdf.f90', 'w') as f:
        for line in lines:
            if "file='shell.xyz'" in line:
                line = line.replace("file='shell.xyz'", f"file='{new_filename}'")
            if "nhis=2600" in line:
                line = line.replace("nhis=2600", f"nhis={nhis}")
            if 'call smooth(hs1,5,hs2)' in line:
                line = line.replace('call smooth(hs1,5,hs2)', f'call smooth(hs1,{smooth1},hs2)')
            if 'call smooth(hs2,5,hs1)' in line:
                line = line.replace('call smooth(hs2,5,hs1)', f'call smooth(hs2,{smooth2},hs1)')
            if "file='rdf.txt'" in line:
                line = line.replace("file='rdf.txt'", f"file='{name[:-4]+'.txt'}'")
            if "delr = 0.02" in line:
                line = line.replace("delr = 0.02",f"delr = {dr}")
            f.write(line)
    resultado = subprocess.run(['gfortran','temp_rdf.f90', '-o', 'rdf'], capture_output=True)
    print(resultado.stdout.decode())
    resultado2 = subprocess.run(['./rdf.exe'], capture_output=True)
    print(resultado2.stdout.decode())
    #os.remove('temp_rdf.f90')
    #os.remove('rdf.exe')


def proccess_all_files_in_folder(folder):
    f_list = file_list(folder)
    for file in f_list:
        print(file)
        run_pdf(file,folder)
        print('\n')

#proccess_all_files_in_folder('shells_out')
#run_pdf('shellPt-FCCv2.xyz','shells_original')
#run_pdf('shellPt-BCC.xyz','shells_original')
#run_pdf('shellPt-ico.xyz','shells_original')
#shutil.move(new_filename[:-4]+'.txt', 'graphics\\'+new_filename[:-4]+'.txt')