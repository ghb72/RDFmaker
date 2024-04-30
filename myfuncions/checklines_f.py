from os import scandir, getcwd
from sys import argv

def file_list(path=getcwd()):
    return [arch.name for arch in scandir(path) if arch.is_file()]

def check_repeated_lines(name):
    with open(name) as infile:
        data = infile.readlines()
    n = int(data[0])
    #print(data[1], data[2])
    unique_lines = set()
    for i in range(n):
        ele, sx, sy, sz = data[i + 2].split()
        line = f"{ele} {sx} {sy} {sz}"
        if line in unique_lines:
            print(f"Línea repetida encontrada: {line} en {name}")
        else:
            unique_lines.add(line)
    print(f"Verificación completa. No se encontraron líneas repetidas en {name}")

def proccess_all_files_in_folder(folder):
    f_list = file_list(folder)
    for file in f_list:
        check_repeated_lines(folder+'\\'+file)

if __name__ == '__main__':
    path = argv[1]
    proccess_all_files_in_folder(path)