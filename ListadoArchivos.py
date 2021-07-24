from service_drive import obtener_servicio
import os
import pathlib


def opciones() -> None:
    # opciones de repositorios
    print("1) Archivos locales\n"
          "2) Archivos remotos\n"
          "3) Salir")


def listado_repo_local(carpetas_anidadas: list, carpeta: str) -> str:
    # Lista los archivos del parámetro pasado
    carpetas_anidadas.append(carpeta)
    anidacion = '/'.join(carpetas_anidadas)
    existe = os.path.exists(anidacion)
    if not existe:
        print("!No existe esa carpeta¡")
        carpetas_anidadas.remove(carpeta)
    else:
        carpetas = pathlib.Path(anidacion)
        if os.path.isfile(anidacion):
            print("Esto es un archivo")
            return anidacion
        else:
            for archivo in carpetas.iterdir():
                print(f"- {archivo.name}")
            return anidacion


def repo_local() -> str:
    # Es el menu del repo local, para luego listarlo en otra funcion
    seguir = True
    repo_inicial = pathlib.Path('/Users')
    for carpetas in repo_inicial.iterdir():
        print(f"- {carpetas.name}")
    carpetas_anidadas = ['/Users']
    while seguir:
        carpeta = input("Ingrese una carpeta o un archivo: ")
        respuesta = listado_repo_local(carpetas_anidadas, carpeta)
        if os.path.isdir(respuesta):
            seguir = True
        else:
            return respuesta



def listar_carpetas_remoto() -> None:
    id_carpeta = input("Ingrese el id de su carpeta: ")
    query = f"parents = '{id_carpeta}'"
    respuesta = obtener_servicio().files().list(q = query).execute()
    print(respuesta)
    nextPageToken = respuesta.get('nextPageToken')
    while nextPageToken:
        respuesta = obtener_servicio().files().list(q = query, pageToken = nextPageToken).execute()
        nextPageToken = respuesta.get('nextPageToken')
    for archivos in respuesta.get('files', []):
        print(f"- {archivos.get('name')} su id es: {archivos.get('id')}")


def repo_remoto() -> None:
    acceso = True
    # Lista todos los archivos del Drive con su id correspondiente
    response = obtener_servicio().files().list().execute()
    for file in response.get('files', []):
        print(f"- {file.get('name')} su id es: {file.get('id')}")
    while acceso:
        seguir = input("Queres buscar alguna carpeta? s/n: ")
        if seguir == "s":
            listar_carpetas_remoto()
        elif seguir == "n":
            acceso = False
        else:
            seguir = input("Ingrese una repsuesta corercta (s/n): ")


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
            repo_remoto()
        elif int(opcion) == 3:  # Hay un error aca, no vuelve al menu principal
            acceso = False
