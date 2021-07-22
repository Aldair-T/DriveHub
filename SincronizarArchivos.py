import os
import pathlib
import time
from service_drive import obtener_servicio


def modificacion_tiempo(archivo) -> str:
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
        tiempo = modificacion_tiempo(archivo)
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
        archivos_remotos[nombre] = tiempo
    return archivos_remotos




"""
archivos_locales = {aldair.txt: 39399393, alda.jpg: 832746}
archivos_remotos = {alda.txt: 923847y2, hola: 4338, aldair.txt: 8376473}
for x, y in archivos_locales.items():
    for z, k in archivos_remotos.items():
        if x == z:
            
"""
