import os
import pathlib


def opciones() -> None:
    # opciones de repositorios
    print("1) Archivos locales\n"
          "2) Archivos remotos")


def repo_local() -> None:
    # Lista los archivos del repositorio local
    # Tenemos que cambiar el contenido del direc. actual por la carpeta principal
    # Averiguar como navegar entre las carpetas del repo
    directorio_actual = os.getcwd()
    carpetas = pathlib.Path(directorio_actual)
    for archivo in carpetas.iterdir():
        print("-", archivo.name)


def listar_archivos() -> None:
    # Elegir si navegar entre repositorio local o remoto
    opciones()
    opcion = input("Elija una opcion: ")
    while not opcion.isnumeric() or int(opcion) < 1 or int(opcion) > 2:
        opcion = input("Ingrese una opcion correcta: ")
    if int(opcion) == 1:
        repo_local()
    elif int(opcion) == 2:
        print("Falta crear la funcion de repo_remoto")
