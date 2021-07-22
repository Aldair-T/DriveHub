import os
import io
from googleapiclient.http import MediaIoBaseDownload
from service_drive import obtener_servicio


def descargar_archivos(ids_archivo: list, nombre_archivos: list) -> None:
    for id_archivo, nombre_archivo in zip(ids_archivo, nombre_archivos):
        respuesta = obtener_servicio().files().get_media(fileId = id_archivo)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd = fh, request = respuesta)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
            done = True
        fh.seek(0)
        with open(os.path.join("./Descargas_Drive", nombre_archivo), "wb") as archivos:
            archivos.write(fh.read())
            archivos.close()


def crear_nombre_archivo() -> None:
    ids_archivo = input("Ingrese el id de su archivo: ")
    ids_archivo = ids_archivo.split(" ")
    nombre = input("Ingrese el nombre para el archivo: ")
    tipo_archivo = input("Ingrese el tipo de archivo (ejem : .txt) : ")
    nombre_archivos = nombre + tipo_archivo
    nombre_archivos = nombre_archivos.split(" ")
    descargar_archivos(ids_archivo, nombre_archivos)


def crear_carpeta_descargas() -> None:
    carpeta = 'Descargas_Drive'
    if os.path.isdir(carpeta):
        crear_nombre_archivo()
    else:
        os.mkdir(carpeta)
        crear_nombre_archivo()
