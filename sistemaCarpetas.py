from service_drive import obtener_servicio as SERVICE_DRIVE
from service_gmail import obtener_servicio as SERVICE_GMAIL
import csv


def creacion_carpeta_alumnos(carpeta_docente_ID: str,docente: str) -> None:
    lista_alumnos = []

    with open("docente-alumno.csv", mode= 'r',newline= '', encoding= "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv,delimiter=',')
        for linea in csv_reader:
            if linea[0] == docente:
                lista_alumnos.append(linea[1])


    for alumno in lista_alumnos:
        carpeta_alumnos_metadata = {        
            'name': alumno,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [carpeta_docente_ID]      
        }
        
        SERVICE_DRIVE().files().create(body=carpeta_alumnos_metadata).execute()

def creacion_carpeta_docentes(carpeta_examenes_ID: str) -> None:

    lista_docentes = []


    with open("docentes.csv", mode= 'r',newline= '', encoding= "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv,delimiter=',')
        for linea in csv_reader:
            lista_docentes.append(linea[0])

 

    for docente in lista_docentes:    
        carpeta_docentes_metadata = {
            'name': docente,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [carpeta_examenes_ID]
        }
        carpeta_docentes = SERVICE_DRIVE().files().create(body=carpeta_docentes_metadata).execute()

        carpeta_docente_ID = carpeta_docentes.get('id')

        creacion_carpeta_alumnos(carpeta_docente_ID,docente)


def creacion_carpeta(nombre: str)-> None:

    file_metadata = {
        'name': nombre,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    carpeta_examenes = SERVICE_DRIVE().files().create(body=file_metadata).execute()

    carpeta_examenes_ID = carpeta_examenes.get('id')

    creacion_carpeta_docentes(carpeta_examenes_ID)


def leer_mail(carpetas_en_drive: list) -> None:

    resultados = SERVICE_GMAIL().users().messages().list(userId='me').execute()


    id_mails = []
    contador = 0
    
    for mail in resultados['messages']:
        mail_ID = (resultados['messages'][contador]['id'])
        id_mails.append(mail_ID)
        contador += 1

    for id_mail in id_mails:

        mail = SERVICE_GMAIL().users().messages().get(userId='me', id=id_mail, format='full').execute()

        for valor in mail['payload']['headers']:
            if valor['name'] == 'Subject':
                asunto = (valor['value']).split()
                if asunto[0] == "nombre_examen":
                    if asunto[1] not in carpetas_en_drive:
                        nombre_examen = asunto[1]
                        creacion_carpeta(nombre_examen)


def carpetas_encontradas() -> None:

    carpetas_en_drive = list()

    carpetas = SERVICE_DRIVE().files().list(q = "mimeType = 'application/vnd.google-apps.folder'").execute()

    for carpeta in carpetas['files']:
        carpetas_en_drive.append(carpeta['name'])
    
    leer_mail(carpetas_en_drive)


carpetas_encontradas()





