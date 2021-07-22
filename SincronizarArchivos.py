import os
import pathlib
import time


def sincronizar() -> None:
    carpetas = pathlib.Path('/Users/aldai/PycharmProjects/pythonProject')
    for archivo in carpetas.iterdir():
        print(f"Ultima modificacion de {archivo.name} fue {time.ctime(os.path.getmtime(archivo))} ")
