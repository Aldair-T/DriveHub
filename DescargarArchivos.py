from datetime import datetime

from googleapiclient.http import MediaIoBaseDownload
from service_drive import obtener_servicio
import os
import io
import pathlib

def tipos_archivos() -> None:
    print("1)Pdf\n"
          "2)Comprimido\n"
          "3)Text\n"
          "4)Csv\n"
          "5)Imagen\n"
          "6)PowerPoint\n"
          "7)Word\n"
          "8)Excel\n")


def elegir_extension(archivo_elegido: str) -> list:
    mimeType = ''
    extension = ''
    if int(archivo_elegido) == 1:
        mimeType = 'application/pdf'
        extension = '.pdf'
    elif int(archivo_elegido) == 2:
        mimeType = 'application/zip'
        extension = '.zip'
    elif int(archivo_elegido) == 3:
        mimeType = 'text/plain'
        extension = '.txt'
    elif int(archivo_elegido) == 4:
        mimeType = 'text/csv'
        extension = '.csv'
    elif int(archivo_elegido) == 5:
        mimeType = 'image/jpeg'
        extension = '.jpeg'
    elif int(archivo_elegido) == 6:
        mimeType = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        extension = '.pptx'
    elif int(archivo_elegido) == 7:
        mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        extension = '.docx'
    elif int(archivo_elegido) == 8:
        mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        extension = '.xlsx'
    return [mimeType, extension]

def archivos_drive() -> dict:
    archivos_remotos = {}
    respuesta = obtener_servicio().files().list(q = "mimeType != 'application/vnd.google-apps.folder'",
                                                fields = 'files(id, name, modifiedTime, mimeType)').execute()
    for file in respuesta.get('files', []):
        tiempo = file.get('modifiedTime')  # obtengo la ultima modificacion
        modificacion_drive = datetime.strptime(tiempo, "%Y-%m-%dT%H:%M:%S.%fZ")
        nombre = file.get('name')
        id_archivo = file.get('id')
        mimeType = file.get('mimeType')
        archivos_remotos[nombre] = [modificacion_drive, id_archivo, mimeType]  # aca guardo todos los archivos
        # {'nombre archivo': [ultima modific, id archivo]}
    return archivos_remotos

def descargar_archivo_media(id_archivo: str, nombre_archivo: str, anidacion: str) -> None:
    respuesta = obtener_servicio().files().get_media(fileId = id_archivo)
    fh = io.BytesIO()
    descarga = MediaIoBaseDownload(fd = fh, request = respuesta)
    salir = False
    while not salir:
        status, salir = descarga.next_chunk()
        print("Se descargo su archivo con exito")
    fh.seek(0)
    with open(os.path.join(anidacion, nombre_archivo), 'wb') as f:
        f.write(fh.read())
        f.close()

def verificar_id(anidacion: str) -> None:
    id_archivo = input("Ingrese el id de su archivo: ")
    lista_id = []
    archivo_drive = archivos_drive()
    for clave, valor in archivo_drive.items():
        lista_id.append(valor[1])
    if id_archivo in lista_id:
        nombre_archivo = input("Ingrese el nuevo nombre: ")
        descargar_archivo_media(id_archivo, nombre_archivo, anidacion)
    else:
        print("No existe ese archivo en drive")

def listado_repo_local(carpetas_anidadas: list, carpeta: str) -> list:
    # Lista los archivos del parámetro pasado
    carpetas_anidadas.append(carpeta)
    anidacion = '/'.join(carpetas_anidadas)
    existe = os.path.exists(anidacion)
    if not existe:
        print("!No existe esa carpeta¡")
        carpetas_anidadas.remove(carpeta)
        return carpetas_anidadas
    else:
        carpetas = pathlib.Path(anidacion)
        if os.path.isfile(anidacion):
            print("Aca no se puede descargar")
        else:
            for archivo in carpetas.iterdir():
                print(f"- {archivo.name}")
            return carpetas_anidadas


def ingresar_carpeta_descarga() -> None:
    seguir = True
    print("Posicionese en la carpeta donde quiere descargar")
    repo_inicial = pathlib.Path('/Users')
    for carpetas in repo_inicial.iterdir():
        print(f"- {carpetas.name}")
    carpetas_anidadas = ['/Users']
    while seguir:
        carpeta = input("Ingrese una carpeta o un NO para descargar aca: ")
        if carpeta == "NO":
            anidacion = '/'.join(carpetas_anidadas)
            verificar_id(anidacion)
            seguir = False
        else:
            carpetas_anidadas = listado_repo_local(carpetas_anidadas, carpeta)
