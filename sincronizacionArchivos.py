import os
import io
import pathlib
import time
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from service_drive import obtener_servicio


def obtener_tiempo(archivo) -> str:
    tiempo = os.path.getmtime(archivo) # obtengo la ultima modificacion del archivo
    anio, mes, dia, hora, minuto, segundo = time.localtime(tiempo)[: -3] # le doy un formato para poder compararlo
    lista_fecha = [anio, mes, dia, hora, minuto, segundo]
    return dar_formato_tiempo(lista_fecha)


def dar_formato_tiempo(lista_fechas: list) -> str:
    cadena_fecha = ''
    for i in lista_fechas:
        i = str(i) # aca paso todos a cadena
        cadena_fecha += i # lo sumo asi obtengo el mismo formato q antes 2020712123557
    return cadena_fecha


def archivos_local() -> dict:
    # aca meto todos los archivos a un diccionario
    carpetas = pathlib.Path('/Users/aldai/PycharmProjects/pythonProject') # esto despues hayq preguntar si tenemos q
    # ingresaelo por defecto o si el usuario ingresa la carpta comparar
    archivos_locales = {}
    for archivo in carpetas.iterdir():
        tiempo = obtener_tiempo(archivo) # aca obtengo la ultima modificacion
        archivos_locales[archivo.name] = tiempo
        # {'nombre archivo': ultima modificacion}
    return archivos_locales


def retornar_formato_tiempo(lista: list) -> str:
    # aca elimino de 2020712123456945Z los ultimos 4 elementos q son los milisegundo creo
    lista_formato = []
    if len(lista) == 17: # esto depende si el mes tiene o no un 0
        for i in lista[0:13]:
            lista_formato.append(i)
    if len(lista) == 18:
        for i in lista[0:14]:
            lista_formato.append(i)
    cadena = "".join(lista_formato)
    return cadena # me devuelve una cadena asi: 2020712123456


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
#        if "0" in lista_tiempo[4]: # si el mes tiene 0 lo elimino \\\\\\ NUEVO COMENTARIO: Mejor si no le eliminas el 0 asi podes implementar la funcion que puse abajo
#            lista_tiempo.pop(4)
    return retornar_formato_tiempo(lista_tiempo) # me retorna esto: 2020712123456945Z en una lista


def archivos_drive() -> dict:
    # aca creo el diccionario de los archivos remotos para despues compararlo
    archivos_remotos = {}
    respuesta = obtener_servicio().files().list(fields = 'files(id, name, modifiedTime)').execute() # obtengo todos los
    # archivos
    for file in respuesta.get('files', []):
        tiempo = file.get('modifiedTime') # obtengo la ultima modificacion
        tiempo = modificar_estructura(tiempo) # le doy estructura pero creo q hay q hacerlo de otra manera
        nombre = file.get('name')
        id_archivo = file.get('id')
        archivos_remotos[nombre] = [tiempo, id_archivo] # aca guardo todos los archivos
        # {'nombre archivo': [ultima modific, id archivo]}
    return archivos_remotos

def convertir_fecha_modific(fecha_modificacion: str) -> list:

    formato_conversion = [4,2,2,2,2,2]
    fecha_convertida = []
    contador = 0

    for formato in formato_conversion:
        fecha_convertida.append(fecha_modificacion[contador: contador + formato])
        contador += formato

    return fecha_convertida

def comparar_fechas_modific(fecha_modificacion_1,fecha_modificacion_2):
    es_mayor = False

    for i in range(len(fecha_modificacion_1)):

        if int(fecha_modificacion_1[i]) > int(fecha_modificacion_2):
            es_mayor = True
    
    return es_mayor

def subir_modific_drive(nombre_archivo: str, id_archivo: str) -> None:
    # aca borro el archivo del drive y subo el nuevo pero no funciona bien
    obtener_servicio().files().delete(fileId = id_archivo) # el .delete lo borra
    archivos_metadata = {'name': nombre_archivo}
    media = MediaFileUpload(nombre_archivo)
    obtener_servicio().files().create(body = archivos_metadata,
                                      media_body = media,
                                      fields = 'id').execute()
    print("Se modificaron los archivos")


def subir_modific_local(nombre_archivo: str, ids_archivo: str) -> None:
    # aca lo q hacia era eliminar el archivo local y descargar el del drive
    nombre_archivos = nombre_archivo.split(" ")
    ids_archivos = ids_archivo.split(" ")
    for ids, nombre in zip(ids_archivos, nombre_archivos): # aca lo q intente hacer era descargarlo pero no funciona
        # xq no te toma los distintos tipos de archivos
        respuesta = obtener_servicio().files().get_media(fileId = ids_archivos)
        fh = io.BytesIO()
        descarga = MediaIoBaseDownload(fd = fh, request = respuesta)
        salir = False
        while salir is False: # esto funciona todp mal hay q buscar la forma para sincronizar sin usra este metodo
            # si no lo usamos de ultimo recurso pero creo q hacerlo asi es mas dificil
            estado, salir = descarga.next_chunk()
            estado = 0
            salir = True
        fh.seek(0)
        with open(os.path.join("./Descargas_Drive", nombre_archivo), "wb") as archivos: # aca creo el nuevo archivo q se
            # descargo y despues lo guardo
            archivos.write(fh.read())
            print("Se modifico los archivos")
            archivos.close()
        os.remove(nombre_archivo) # aca lo q hago es eliminar archivo del local


def sincronizacion() -> None:
    dict_local = archivos_local()  # {'nombre archivo': fecha de ultima modificacion}
    dict_drive = archivos_drive()  # ambos tiene el mismo formato en las q la key es el nombre y el valor es la fecha
    # de modificacion
    for nombres_local, modificacion_local in dict_local.items():
        for nombres_drive, modificacion_drive in dict_drive.items():
            if nombres_local == nombres_drive:  # busca entre los dos diccionarios nombres iguales
                modificacion_local = convertir_fecha_modific(modificacion_local)
                modificacion_drive = convertir_fecha_modific(modificacion_drive)
                if comparar_fechas_modific(modificacion_local,modificacion_drive): 
                    subir_modific_drive(nombres_local, modificacion_drive[1])
                elif comparar_fechas_modific(modificacion_drive,modificacion_local): # aca lo mismo q lo anterior
                    subir_modific_local(nombres_local, modificacion_drive[1])


# el formato de las fechas era 2020/07/28 16:36:56 (año,mes,dia  hora,minutos,segundos) y terminaba asi: 2020728163656
# pero lo implemente mal y no funciona, despues el metodo de comparacion lo hice a los pedos para ver si llegabamos a la
# primera entrega asi q esta muuuuyy mal hecho, no busque todavia como poder compararlo