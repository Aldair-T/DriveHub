import os
import io
import pathlib
import time
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from service_drive import obtener_servicio


def definir_tipo_archivo(nombre_archivo: str) -> tuple:

    tipo_archivo = ""

    if nombre_archivo.endswith(".pdf") == 1:
        tipo_archivo = 'application/pdf'
        nombre_archivo = nombre_archivo.removesuffix(".pdf")
    elif nombre_archivo.endswith(".txt") == 3:
        tipo_archivo = 'text/plain'
        nombre_archivo = nombre_archivo.removesuffix(".txt")
    elif nombre_archivo.endswith(".csv") == 4:
        tipo_archivo = 'text/csv'
        nombre_archivo = nombre_archivo.removesuffix(".csv")
    elif nombre_archivo.endswith(".jpg") == 5:
        tipo_archivo = 'image/jpeg'
        nombre_archivo = nombre_archivo.removesuffix(".jpg")
    elif nombre_archivo.endswith(".docx") == 6:
        tipo_archivo = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        nombre_archivo = nombre_archivo.removesuffix(".docx")
    elif nombre_archivo.endswith(".pptx") == 7:
        tipo_archivo = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        nombre_archivo = nombre_archivo.removesuffix(".pptx")
    elif nombre_archivo.endswith(".xlsx") == 8:
        tipo_archivo = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        nombre_archivo = nombre_archivo.removesuffix(".xlsx")
    
    return tipo_archivo,nombre_archivo



def obtener_tiempo(archivo) -> str:
    tiempo = os.path.getmtime(archivo) # obtengo la ultima modificacion del archivo
    anio, mes, dia, hora, minuto, segundo = time.localtime(tiempo)[: -3] # le doy un formato para poder compararlo
    lista_fecha = [anio, mes, dia, hora, minuto, segundo]
    tiempo_formateado = dar_formato_tiempo(lista_fecha)

    return tiempo_formateado


def obtener_extension_archivo(nombre_archivo:str, ID_archivo: str) -> str:

    servicio_archivo = obtener_servicio().files()
    informacion_archivo = servicio_archivo.get(fileId=ID_archivo,fields= 'fileExtension').execute()
    if len(informacion_archivo) == 0:
        informacion_archivo = servicio_archivo.get(fileId=ID_archivo,fields= 'mimeType').execute()
        if informacion_archivo['mimeType'] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extension_archivo = ".docx"
            nombre_archivo += extension_archivo
        elif informacion_archivo['mimeType'] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            extension_archivo = ".xlsx"
            nombre_archivo += extension_archivo
    return nombre_archivo



def dar_formato_tiempo(lista_fechas: list) -> str:
    cadena_fecha = ''
    for i in lista_fechas:
        i = str(i) # aca paso todos a cadena
        cadena_fecha += i # lo sumo asi obtengo el mismo formato q antes 2020712123557
    return cadena_fecha


def archivos_local() -> dict:
    directorio_usuario = os.getcwd()
    carpetas = pathlib.Path(directorio_usuario)
    archivos_locales = {}
    for archivo in carpetas.iterdir():
        tiempo = obtener_tiempo(archivo) # aca obtengo la ultima modificacion
        archivos_locales[archivo.name] = tiempo
        # {'nombre archivo': ultima modificacion}
    return archivos_locales


def retornar_formato_tiempo(lista: list) -> str:

    lista_formato = []
    for i in lista[0:14]:
            lista_formato.append(i)
    cadena = "".join(lista_formato)
    return cadena 


def modificar_estructura(tiempo: str) -> str:
    lista_tiempo = []
    # aca el formato viene dado como: 2020-07-12T12:34:56.945Z
    for i in tiempo:
        lista_tiempo.append(i) # cada letra o numero es un elemento de la lista
    if "-" and "T" and "." and ":" in lista_tiempo:
        lista_tiempo.remove("-")
        lista_tiempo.remove("-")
        lista_tiempo.remove("T")
        lista_tiempo.remove(".")# elimino las cosas q no me interesan
        lista_tiempo.remove(":")
        lista_tiempo.remove(":")
    return retornar_formato_tiempo(lista_tiempo) # me retorna esto: 2020712123456945Z en una lista


def archivos_drive() -> dict:
    # aca creo el diccionario de los archivos remotos para despues compararlo
    archivos_remotos = {}
    respuesta = obtener_servicio().files().list(q = "mimeType != 'application/vnd.google-apps.folder'",fields = 'files(id, name, modifiedTime)').execute()

    for file in respuesta.get('files', []):
        tiempo = file.get('modifiedTime') # obtengo la ultima modificacion
        tiempo = modificar_estructura(tiempo) # le doy estructura pero creo q hay q hacerlo de otra manera
        nombre = file.get('name')
        id_archivo = file.get('id')
        nombre = obtener_extension_archivo(nombre,id_archivo)
        archivos_remotos[nombre] = [tiempo, id_archivo] # aca guardo todos los archivos
        # {'nombre archivo': [ultima modific, id archivo]}
    return archivos_remotos

def descargar_media_drive(nombre_archivo: str,id_archivos: str,ruta_archivo: str) -> None:

    respuesta = obtener_servicio().files().get_media(fileId = id_archivos)
    fh = io.BytesIO()
    descarga = MediaIoBaseDownload(fd = fh, request = respuesta)
    salir = False
    while not salir:
        status, salir = descarga.next_chunk()
        print("Se descargo su archivo con exito")
    fh.seek(0)
    with open(os.path.join(ruta_archivo, nombre_archivo), 'wb') as f:
        f.write(fh.read())
        f.close()


def descargar_workspace_drive(nombre_archivo: str,id_archivos: str,ruta_archivo: str) -> None:

    tipo_archivo = definir_tipo_archivo(nombre_archivo)

    byteData = obtener_servicio().files().export_media(
        fileId = id_archivos,
        mimeType = tipo_archivo).execute()
    with open(os.path.join(ruta_archivo, nombre_archivo), 'wb', encoding = "utf-8") as f:
        f.write(byteData)
        f.close()


def subir_modific_drive(nombre_archivo: str, id_archivo: str) -> None:
    
    tipo_archivo,nombre = definir_tipo_archivo(nombre_archivo)

    ruta_archivo = os.getcwd + "\\" + nombre_archivo

    obtener_servicio().files().delete(fileId = id_archivo)

    file_metadata = {'name': nombre, 'mimeType': tipo_archivo}
    media = MediaFileUpload(ruta_archivo, mimetype = tipo_archivo)
    obtener_servicio().files().create(body = file_metadata,
                                      media_body = media,
                                      fields = 'id').execute()

    print("Su archivo se subió con éxito")



def subir_modific_local(nombre_archivo: str, id_archivo: str) -> None:

    lista_extensiones = [".docx",".xlsx",".pptx"]

    ruta_archivo = os.getcwd()

    workspace = False

    for extension in lista_extensiones:
        if nombre_archivo.endswith(extension):
            workspace = True

    if workspace:
        descargar_workspace_drive(nombre_archivo,id_archivo,ruta_archivo)
    else:
        descargar_media_drive(nombre_archivo,id_archivo,ruta_archivo)



def sincronizacion() -> None:
    dict_local = archivos_local() 
    dict_drive = archivos_drive()  

    for nombres_local, modificacion_local in dict_local.items():
        for nombres_drive, modificacion_drive in dict_drive.items():
            if nombres_local == nombres_drive:  
                if int(modificacion_drive[0]) < int(modificacion_local): 
                    subir_modific_drive(nombres_local, modificacion_drive[1])
                elif int(modificacion_drive[0]) > int(modificacion_local): 
                    subir_modific_local(nombres_local, modificacion_drive[1])

sincronizacion()