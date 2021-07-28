from datetime import datetime
from pathlib import Path
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from service_drive import obtener_servicio as SERVICE_DRIVE
from service_gmail import obtener_servicio as SERVICE_GMAIL
import os
import io
import pathlib
import csv


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


def opciones() -> None:
    # opciones de repositorios
    print("1) Archivos locales\n"
          "2) Archivos remotos\n"
          "3) Salir")


def tipos_archivos_creacion() -> None:
    # Tipos de archivos que se pueden crear (Pueden faltar algunos)
    print("1) Crear un archivo .pdf\n"
          "2) Crear un archivo .zip\n"
          "3) Crear un archivo .txt\n"
          "4) Crear un archivo .csv\n"
          "5) Crear un archivo .jpg\n"
          "6) Crear un archivo PowerPoint\n"
          "7) Crear un archivo Word\n"
          "8) Crear un archivo Excel\n"
          "9) Crear una carpeta"
          "10) Menu principal")


def tipos_() -> None:
    print("1)Pdf\n"
          "2)Comprimido\n"
          "3)Text\n"
          "4)Csv\n"
          "5)Imagen\n"
          "6)PowerPoint\n"
          "7)Word\n"
          "8)Excel\n")


def ruta_a_archivo(carpetas_anidadas: list, carpeta: str) -> str:
    # Lista los archivos del parámetro pasado
    carpetas_anidadas.append(carpeta)
    anidacion = '/'.join(carpetas_anidadas)
    existe = os.path.exists(anidacion)
    if not existe:
        print("!No existe esa carpeta¡")
        carpetas_anidadas.remove(carpeta)
        return 'No existe'
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
        anidacion = ruta_a_archivo(carpetas_anidadas, carpeta)
        if os.path.isdir(anidacion):
            seguir = True
        elif os.path.isfile(anidacion):
            return anidacion
        else:
            seguir = False


def listar_carpeta_drive(ids_carpetas: list) -> None:
    id_ = input("Ingrese el id de su carpeta: ")
    if id_ in ids_carpetas:
        query = f"parents = '{id_}'"
        respuesta = SERVICE_DRIVE().files().list(q = query).execute()
        for archivos in respuesta.get('files', []):
            print(f"- {archivos.get('name')} su id es: {archivos.get('id')}")
    else:
        print("No existe esa carpeta")


def verificar_carpetas_drive() -> None:
    id_carpetas = []
    respuesta = SERVICE_DRIVE().files().list(q = "mimeType = 'application/vnd.google-apps.folder'").execute()
    for file in respuesta.get('files', []):
        ids = file.get('id')
        id_carpetas.append(ids)
    if len(id_carpetas) > 0:
        listar_carpeta_drive(id_carpetas)
    else:
        print("No hay carpetas en tu drive")


def repo_remoto() -> None:
    acceso = True
    # Lista todos los archivos del Drive con su id correspondiente
    respuesta = SERVICE_DRIVE().files().list().execute()
    for archivo in respuesta.get('files', []):
        print(f"- {archivo.get('name')} su id es: {archivo.get('id')}")
    while acceso:
        seguir = input("Queres buscar alguna carpeta? s/n: ")
        if seguir == "s":
            verificar_carpetas_drive()
        elif seguir == "n":
            acceso = False
        else:
            print("Ingrese una respuesta correcta")


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
        else:  # Hay un error aca, no vuelve al menu principal
            main()


def crear_carpeta_drive(nombre_carpeta: str):
    archivo_metadata = {
        'name': nombre_carpeta,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    SERVICE_DRIVE().files().create(body = archivo_metadata, fields = 'id').execute()
    print("Se creo su carpeta")


def crear_carpeta() -> None:
    # Crea carpetas, falta que naveguen en el escritorio
    nombre_carpeta = input("Ingrese el nombre de la carpeta: ")
    if os.path.isdir(nombre_carpeta):
        print("la carpeta existe")
    else:
        crear_carpeta_drive(nombre_carpeta)
        os.mkdir(nombre_carpeta)


def crear_archivo_drive(tipo_archivo: str, nombre_archivo) -> None:
    archivo_metadata = {
        'name': nombre_archivo,
        'mimeType': tipo_archivo
    }
    SERVICE_DRIVE().files().create(body = archivo_metadata, fields = 'id').execute()


def crear_archivo_local(tipo_archivo: str, extension: str) -> None:
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    nombre_archivo += extension
    archivo = Path(nombre_archivo)
    if archivo.is_file():
        print("Ese archivo ya existe")
    else:
        crear_archivo_drive(tipo_archivo, nombre_archivo)
        nuevo_archivo = open(nombre_archivo, "w", encoding = "utf-8")
        nuevo_archivo.close()
        print("Se creo con éxito")


def creacion_archivos() -> None:
    # Es el menu para ver que archivo va a crear
    tipos_archivos_creacion()
    opcion = input("Que quieres crear: ")
    while not opcion.isnumeric() or int(opcion) < 1 or int(opcion) > 10:
        opcion = input("Ingrese una opcion correcta: ")
    extension = elegir_extension(opcion)
    if 1 <= int(opcion) <= 8:
        crear_archivo_local(extension[0], extension[1])
    elif int(opcion) == 9:
        crear_carpeta()
    elif int(opcion) == 10:
        main()


def subir_a_unidad(nombre: str, ruta_archivo: str, tipo_archivo: str) -> None:
    file_metadata = {'name': nombre, 'mimeType': tipo_archivo}
    media = MediaFileUpload(ruta_archivo, mimetype = tipo_archivo)
    SERVICE_DRIVE().files().create(body = file_metadata,
                                   media_body = media,
                                   fields = 'id').execute()
    print("Su archivo se subió con éxito")


def subir_a_carpeta_especifica(nombre: str, id_carpeta: str, ruta_archivo: str, tipo_archivo: str) -> None:
    file_metadata = {'name': nombre, 'mimeType': tipo_archivo, 'parents': [id_carpeta]}
    media = MediaFileUpload(ruta_archivo, mimetype = tipo_archivo)
    SERVICE_DRIVE().files().create(body = file_metadata,
                                   media_body = media,
                                   fields = 'id').execute()
    print("Su archivo se subió con exito")


def verificar_carpetas_drive(nombre: str, id_carpet: str, ruta_archivo: str, tipo_archivo: str) -> None:
    id_carpetas = []
    response = SERVICE_DRIVE().files().list(q = "mimeType = 'application/vnd.google-apps.folder'").execute()
    for file in response.get('files', []):
        ids = file.get('id')
        id_carpetas.append(ids)
    if id_carpet in id_carpetas:
        subir_a_carpeta_especifica(nombre, id_carpet, ruta_archivo, tipo_archivo)
    else:
        print("Esa carpeta no existe")


def elegir_datos(ruta_archivo: str, tipo_archivo: str) -> None:
    nombre = input("Ingrese el nombre para el nuevo archivo: ")
    respuesta = input("Deseas guardar en una carpeta especifica? s/n: ")
    if respuesta == "s":
        carpeta = input("Ingrese el id de su carpeta: ")
        verificar_carpetas_drive(nombre, carpeta, ruta_archivo, tipo_archivo)
        main()
    elif respuesta == "n":
        subir_a_unidad(nombre, ruta_archivo, tipo_archivo)
        main()
    else:
        print("Ingrese una opcion correcta")


def subir_archivos() -> None:
    print("Ingrese la ruta de su archivo")
    ruta_archivo = repo_local()
    tipos_()
    if os.path.isfile(ruta_archivo):
        tipo_archivo = input("Ingrese el tipo de archivo: ")
        while not tipo_archivo.isnumeric() or int(tipo_archivo) < 1 or int(tipo_archivo) > 8:
            tipo_archivo = input("Ingrese una opcion correcta: ")
        propiedades_archivo = elegir_extension(tipo_archivo)
        elegir_datos(ruta_archivo, propiedades_archivo[0])
    else:
        print("Ese archivo no existe")


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


def archivos_drive() -> dict:
    archivos_remotos = {}
    respuesta = SERVICE_DRIVE().files().list(q = "mimeType != 'application/vnd.google-apps.folder'",
                                             fields = 'files(id, name, modifiedTime, mimeType)').execute()
    for archivo in respuesta.get('files', []):
        tiempo = archivo.get('modifiedTime')  # obtengo la ultima modificacion
        modificacion_drive = datetime.strptime(tiempo, "%Y-%m-%dT%H:%M:%S.%fZ")
        nombre = archivo.get('name')
        id_archivo = archivo.get('id')
        mimeType = archivo.get('mimeType')
        archivos_remotos[nombre] = [modificacion_drive, id_archivo, mimeType]  # aca guardo todos los archivos
        # {'nombre archivo': [ultima modific, id archivo]}
    return archivos_remotos


def descargar_archivo_media(id_archivo: str, nombre_archivo: str, anidacion: str) -> None:
    respuesta = SERVICE_DRIVE().files().get_media(fileId = id_archivo)
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


def ruta_carpeta(carpetas_anidadas: list, carpeta: str) -> list:
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
        carpeta = input("Ingrese una carpeta o un . para descargar aca: ")
        if carpeta == ".":
            anidacion = '/'.join(carpetas_anidadas)
            verificar_id(anidacion)
            main()
        else:
            carpetas_anidadas = ruta_carpeta(carpetas_anidadas, carpeta)


def sincronizar() -> None:
    dict_local = archivos_local()
    dict_drive = archivos_drive()
    for nombres_local, modificacion_local in dict_local.items():
        for nombres_drive, modificacion_drive in dict_drive.items():
            if nombres_local == nombres_drive:
                print(modificacion_local[0])
                print(modificacion_drive[0])
                if modificacion_local[0] > modificacion_drive[0]:
                    print("hl")
                    SERVICE_DRIVE().files().delete(fileId = modificacion_drive[1])
                    print(nombres_local)
                    subir_a_unidad(nombres_local, modificacion_local[1], modificacion_drive[2])
                elif modificacion_drive[0] > modificacion_local[0]:
                    print("as")
                    os.remove(modificacion_local[1])
                    print(nombres_drive)
                    descargar_archivo_media(modificacion_drive[1], nombres_drive, os.getcwd())
                else:
                    print("No hay archivos para modificar")


def creacion_carpeta_alumnos(carpeta_docente_ID: str, docente: str) -> None:
    print("asdhae")
    lista_alumnos = []

    with open("docente-alumnos.csv", mode = 'r', newline = '', encoding = "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter = ',')
        for linea in csv_reader:
            if linea[0] == docente:
                lista_alumnos.append(linea[1])

    for alumno in lista_alumnos:
        carpeta_alumnos_metadata = {
            'name': alumno,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [carpeta_docente_ID]
        }

        SERVICE_DRIVE().files().create(body = carpeta_alumnos_metadata).execute()


def creacion_carpeta_docentes(carpeta_examenes_ID: str) -> None:
    print("PLOA")
    lista_docentes = []

    with open("docentes.csv", mode = 'r', newline = '', encoding = "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter = ',')
        for linea in csv_reader:
            lista_docentes.append(linea[0])

    for docente in lista_docentes:
        carpeta_docentes_metadata = {
            'name': docente,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [carpeta_examenes_ID]
        }
        carpeta_docentes = SERVICE_DRIVE().files().create(body = carpeta_docentes_metadata).execute()

        carpeta_docente_ID = carpeta_docentes.get('id')

        creacion_carpeta_alumnos(carpeta_docente_ID, docente)


def creacion_carpeta_examen(nombre: str) -> None:
    print("Oas")
    file_metadata = {
        'name': nombre,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    carpeta_examenes = SERVICE_DRIVE().files().create(body = file_metadata).execute()

    carpeta_examenes_ID = carpeta_examenes.get('id')

    creacion_carpeta_docentes(carpeta_examenes_ID)


def leer_mail(carpetas_en_drive: list) -> None:
    print("Nasda")
    resultados = SERVICE_GMAIL().users().messages().list(userId = 'me').execute()

    id_mails = []
    contador = 0

    for mail in resultados['messages']:
        mail_ID = (resultados['messages'][contador]['id'])
        id_mails.append(mail_ID)
        contador += 1

    for id_mail in id_mails:

        mail = SERVICE_GMAIL().users().messages().get(userId = 'me', id = id_mail, format = 'full').execute()

        for valor in mail['payload']['headers']:
            if valor['name'] == 'Subject':
                asunto = (valor['value']).split()
                if asunto[0] == "nombre_examen":
                    if asunto[1] not in carpetas_en_drive:
                        nombre_examen = asunto[1]
                        creacion_carpeta_examen(nombre_examen)


def carpetas_encontradas() -> None:
    print("NOasas")
    carpetas_en_drive = list()

    carpetas = SERVICE_DRIVE().files().list(q = "mimeType = 'application/vnd.google-apps.folder'").execute()

    for carpeta in carpetas['files']:
        carpetas_en_drive.append(carpeta['name'])

    leer_mail(carpetas_en_drive)


def menu() -> None:
    print("1) Listar archivos\n"
          "2) Crear un archivo\n"
          "3) Subir un archivo\n"
          "4) Descargar un archivo\n"
          "5) Sincronizar\n"
          "6) Genera carpeta de una evaluacion\n"
          "7) Actualizar entregas de alumnos via mail\n"
          "8) Salir")


def opcion_valida(opcion: str) -> int:
    while not opcion.isnumeric() or int(opcion) < 1 or int(opcion) > 8:
        opcion = input("Ingrese una opcion correcta: ")
    opcion = int(opcion)
    return opcion


def main() -> None:
    menu()
    acceso = True
    opcion = input("Ingrese una opcion: ")
    opcion = opcion_valida(opcion)
    while acceso == True:
        if opcion == 1:
            listar_archivos()
        if opcion == 2:
            creacion_archivos()
        if opcion == 3:
            subir_archivos()
        if opcion == 4:
            ingresar_carpeta_descarga()
        if opcion == 5:
            sincronizar()
        if opcion == 6:
            carpetas_encontradas()
        if opcion == 7:
            pass
        if opcion == 8:
            acceso = False


main()
