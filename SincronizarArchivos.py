import os
import pathlib
from datetime import datetime
from service_drive import obtener_servicio
from SubirArchivo import subir_a_unidad
from DescargarArchivos import descargar_archivo_media, archivos_drive
def archivos_local() -> dict:
    directorio_usuario = os.getcwd()
    carpetas = pathlib.Path(directorio_usuario)
    archivos_locales = {}
    for archivo in carpetas.iterdir():
        ruta_archivo = os.getcwd() + "\\" + archivo.name
        modificacion_local = datetime.utcfromtimestamp(os.path.getmtime(archivo))
        archivos_locales[archivo.name] = [modificacion_local, ruta_archivo]
        # {'nombre archivo': ultima modificacion}
    return archivos_locales





def sincronizar() -> None:
    dict_local = archivos_local()
    dict_drive = archivos_drive()
    for nombres_local, modificacion_local in dict_local.items():
        for nombres_drive, modificacion_drive in dict_drive.items():
            if nombres_local == nombres_drive:
                if modificacion_local[0] > modificacion_drive[0]:
                    subir_a_unidad(nombres_local, modificacion_local[1], modificacion_drive[2])
                    obtener_servicio().files().delete(fileId = modificacion_drive[1])
                elif modificacion_drive[0] > modificacion_local[0]:
                    descargar_archivo_media(modificacion_drive[1], nombres_drive, os.getcwd())
                    os.remove(modificacion_local[1])
                else:
                    print("No hay archivos para modificar")
