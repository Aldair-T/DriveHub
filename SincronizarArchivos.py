import os
import io
import pathlib
import time
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from service_drive import obtener_servicio


def obtener_tiempo(archivo) -> str:
    tiempo = os.path.getmtime(archivo)
    anio, mes, dia, hora, minuto, segundo = time.localtime(tiempo)[: -3]
    lista_fecha = [anio, mes, dia, hora, minuto, segundo]
    return dar_formato_tiempo(lista_fecha)


def dar_formato_tiempo(lista_fechas: list) -> str:
    cadena_fecha = ''
    for i in lista_fechas:
        i = str(i)
        cadena_fecha += i
    return cadena_fecha


def archivos_local() -> dict:
    carpetas = pathlib.Path('/Users/aldai/PycharmProjects/pythonProject')
    archivos_locales = {}
    for archivo in carpetas.iterdir():
        tiempo = obtener_tiempo(archivo)
        archivos_locales[archivo.name] = tiempo
    return archivos_locales


def retornar_formato_tiempo(lista: list) -> str:
    lista_formato = []
    if len(lista) == 17:
        for i in lista[0:13]:
            lista_formato.append(i)
    if len(lista) == 18:
        for i in lista[0:14]:
            lista_formato.append(i)
    cadena = "".join(lista_formato)
    return cadena


def modificar_estructura(tiempo: str) -> str:
    lista_tiempo = []
    for i in tiempo:
        lista_tiempo.append(i)
    if "-" and "T" and "." and ":" in lista_tiempo:
        lista_tiempo.remove("-")
        lista_tiempo.remove("-")
        lista_tiempo.remove("T")
        lista_tiempo.remove(".")
        lista_tiempo.remove(":")
        lista_tiempo.remove(":")
        if "0" in lista_tiempo[4]:
            lista_tiempo.pop(4)
    return retornar_formato_tiempo(lista_tiempo)


def archivos_drive() -> dict:
    archivos_remotos = {}
    respuesta = obtener_servicio().files().list(fields = 'files(id, name, modifiedTime)').execute()
    for file in respuesta.get('files', []):
        tiempo = file.get('modifiedTime')
        tiempo = modificar_estructura(tiempo)
        nombre = file.get('name')
        id_archivo = file.get('id')
        archivos_remotos[nombre] = [tiempo, id_archivo]
    return archivos_remotos


def subir_modific_drive(nombre_archivo: str, id_archivo: str) -> None:
    obtener_servicio().files().delete(fileId = id_archivo)
    archivos_metadata = {'name': nombre_archivo}
    media = MediaFileUpload(nombre_archivo)
    obtener_servicio().files().create(body = archivos_metadata,
                                      media_body = media,
                                      fields = 'id').execute()
    print("Se modificaron los archivos")


def subir_modific_local(nombre_archivo: str, ids_archivo: str) -> None:
    nombre_archivos = nombre_archivo.split(" ")
    ids_archivos = ids_archivo.split(" ")
    for ids, nombre in zip(ids_archivos, nombre_archivos):
        respuesta = obtener_servicio().files().get_media(fileId = ids_archivos)
        fh = io.BytesIO()
        descarga = MediaIoBaseDownload(fd = fh, request = respuesta)
        salir = False
        while salir is False:
            estado, salir = descarga.next_chunk()
            estado = 0
            salir = True
        fh.seek(0)
        with open(os.path.join("./Descargas_Drive", nombre_archivo), "wb") as archivos:
            archivos.write(fh.read())
            print("Se modifico los archivos")
            archivos.close()
        os.remove(nombre_archivo)


def sincronizacion() -> None:
    dict_local = archivos_local()
    print(dict_local)
    dict_drive = archivos_drive()
    print(dict_drive)

    for nombres_local, modificacion_local in dict_local.items():
        for nombres_drive, modificacion_drive in dict_drive.items():
            if nombres_local == nombres_drive:
                print(modificacion_drive[0])
                if modificacion_local > modificacion_drive[0]:
                    print("badyb")
                    subir_modific_drive(nombres_local, modificacion_drive[1])
                elif modificacion_local < modificacion_drive[0]:
                    print("uadb")
                    subir_modific_local(nombres_local, modificacion_drive[1])
