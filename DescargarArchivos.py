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
          "6)Word\n"
          "7)PowerPoint\n"
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
        extension = '.jpg'
    elif int(archivo_elegido) == 6:
        mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        extension = '.docx'
    elif int(archivo_elegido) == 7:
        mimeType = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        extension = '.pptx'
    elif int(archivo_elegido) == 8:
        mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        extension = '.xlsx'
    return [mimeType, extension]


def descargar_archivos_media(ids_archivos: str, nombre_archivo: str, anidacion: str) -> None:
    respuesta = obtener_servicio().files().get_media(fileId = ids_archivos)
    fh = io.BytesIO()
    descarga = MediaIoBaseDownload(fd = fh, request = respuesta)
    salir = False
    while not salir:
        status, salir = descarga.next_chunk()
        print("Se descargo su archivo con exito")
    fh.seek(0)
    with open(os.path.join(anidacion, nombre_archivo), 'wb', encoding = "utf-8") as f:
        f.write(fh.read())
        f.close()


def descargar_archivos_workspace(ids_archivo: str, tipo_archivo: str, nombre_archivo: str, anidacion: str) -> None:
    byteData = obtener_servicio().files().export_media(
        fileId = ids_archivo,
        mimeType = tipo_archivo).execute()
    with open(os.path.join(anidacion, nombre_archivo), 'wb', encoding = "utf-8") as f:
        f.write(byteData)
        f.close()


def crear_nombre_archivo(id_archivo: str, anidacion: str) -> None:
    nombre_archivo = input("Ingrese el nuevo nombre: ")
    tipos_archivos()
    tipo_a = input("Ingres el tipo de archivo: ")
    while not tipo_a.isnumeric() or int(tipo_a) < 1 or int(tipo_a) > 8:
        tipo_a = input("Ingrese una opcion correcta: ")
    tipo_extension = elegir_extension(tipo_a)
    nombre_archivo += tipo_extension[1]
    if 1 <= int(tipo_a) <= 5:
        descargar_archivos_media(id_archivo, nombre_archivo, anidacion)
    elif int(tipo_a) >= 6:
        descargar_archivos_workspace(id_archivo, tipo_extension[0], nombre_archivo, anidacion)


def verificar_id(anidacion: str) -> None:
    lista_id = []
    id_archivo = input("Ingrese el id de su archivo: ")
    response = obtener_servicio().files().list(q = "mimeType != 'application/vnd.google-apps.folder'").execute()
    for file in response.get('files', []):
        ids = file.get('id')
        lista_id.append(ids)
    if id_archivo in lista_id:
        crear_nombre_archivo(id_archivo, anidacion)
    else:
        print("No existe ese archivo en tu drive")


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
