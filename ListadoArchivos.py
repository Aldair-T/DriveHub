from service_drive import obtener_servicio
import os
import pathlib
import pandas as pd


def opciones() -> None:
    # opciones de repositorios
    print("1) Archivos locales\n"
          "2) Archivos remotos\n"
          "3) Salir")


def listado_repo_local(carpetas_anidadas: list, carpeta: str) -> None:
    # Lista los archivos del parámetro pasado
    carpetas_anidadas.append(carpeta)
    anidacion = '/'.join(carpetas_anidadas)
    existe = os.path.exists(anidacion)
    if not existe:
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
    while seguir:
        carpeta = input("Ingrese una carpeta o exit para salir: ")
        if carpeta == "exit":
            seguir = False
        else:
            listado_repo_local(carpetas_anidadas, carpeta)


def listar_todo_drive() -> None:
    # Lista todos los archivos del Drive con su id correspondiente
    acceso = True
    while acceso:
        response = obtener_servicio().files().list().execute()
        for file in response.get('files', []):
            print(f"- {file.get('name')}, su id es: {file.get('id')}")
        if acceso:
            acceso = False


def busqueda_especifica() -> None:
    Id = input("Ingrese el archivo a buscar: ")
    response = obtener_servicio().files().list().execute()
    archivos_exactos = response.get(Id)
    siguiente_pagina = response.get('nextPageToken')

    while siguiente_pagina:
        response = obtener_servicio().files().list().execute()
        archivos_exactos.extend(response.get(Id))
        siguiente_pagina = response.get('nextPageToken')

    archivos = pd.DataFrame(archivos_exactos)
    print(archivos)


def repo_remoto() -> None:
    # Elegir en como buscar sus archivos
    print("1) Listar todos los archivos\n"
          "2) Busqueda especifica\n")
    respuesta = input("Ingrese una opcion: ")
    while not respuesta.isnumeric() or int(respuesta) < 1 or int(respuesta) > 2:
        respuesta = input("Ingrese una opcion correcta: ")
    if int(respuesta) == 1:
        listar_todo_drive()
    if int(respuesta) == 2:
        busqueda_especifica()


def listar_archivos() -> None:
    # Elegir si navegar entre repositorio local o remoto
    acceso = True
    while acceso:
        opciones()
        opcion = input("Elija una opcion: ")
        while not opcion.isnumeric() or int(opcion) < 1 or int(opcion) > 3:
            opcion = input("Ingrese una opcion correcta: ")
        if int(opcion) == 1:
            repo_local()
        elif int(opcion) == 2:
            listar_todo_drive()
        elif int(opcion) == 3:  # Hay un error aca, no vuelve al menu principal
            acceso = False
