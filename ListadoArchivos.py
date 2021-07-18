import os
import pathlib


def opciones() -> None:
    # opciones de repositorios
    print("1) Archivos locales\n"
          "2) Archivos remotos\n"
          "3) Salir")


def listado(carpetas_anidadas: list, carpeta: str) -> None:
    # Lista los archivos del parámetro pasado
    carpetas_anidadas.append(carpeta)
    anidacion = '/'.join(carpetas_anidadas)
    existe = os.path.exists(anidacion)
    if existe == False:
        print("!No existe esa carpeta¡")
        carpetas_anidadas.remove(carpeta)
    else:
        carpetas = pathlib.Path(anidacion)
        for archivo in carpetas.iterdir():
            print(f"- {archivo.name}")


def repo_local() -> None:
    # Es el menu del repo local, para luego listarlo en otra funcion
    seguir = True
    repo_inicial = pathlib.Path('/Users')
    for carpetas in repo_inicial.iterdir():
        print(f"- {carpetas.name}")
    carpetas_anidadas = ['/Users']
    while seguir == True:
        carpeta = input("Ingrese una carpeta o exit para salir: ")
        if carpeta == "exit":
            seguir = False
        else:
            listado(carpetas_anidadas, carpeta)


def listar_archivos() -> None:
    # Elegir si navegar entre repositorio local o remoto
    acceso = True
    while acceso == True:
        opciones()
        opcion = input("Elija una opcion: ")
        while not opcion.isnumeric() or int(opcion) < 1 or int(opcion) > 3:
            opcion = input("Ingrese una opcion correcta: ")
        if int(opcion) == 1:
            repo_local()
        elif int(opcion) == 2:
            print("Falta crear la funcion de repo_remoto")
        elif int(opcion) == 3:  # Hay un error aca, no vuelve al menu principal
            acceso = False
