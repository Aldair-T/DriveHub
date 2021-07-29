from service_drive import obtener_servicio as SERVICE_DRIVE
from service_gmail import obtener_servicio as SERVICE_GMAIL
import csv

def importar_archivos(alumnos):
    resultados = SERVICE_GMAIL().users().messages().list(userId='me').execute()
    id_mails = []
    contador = 0
    for mail in resultados['messages']:
        mail_ID = (resultados['messages'][contador]['id'])
        contador += 1
        
        for padron in mail['payload']['headers']:
            nombre = alumnos[padron]

            archivo = SERVICE_GMAIL().users().attachments().get(userId='me', messageId=mail_ID, x__xgafv=None).execute()

            buscar_carpeta(nombre,archivo)

            service.files().update(fileId = archivo.get("id"),
            addParents = target_folder_id,
            removeParents = source_folder_id
            ).execute()


            

def buscar_carpeta(nombre_alumno: str, archivo) ->  None:
    id_ = input("Ingrese el nombre de la carpeta: ")
    carpetas_en_drive = {}
    carpetas_profesores = {}
    carpetas_alumnos = {}
    carpetas = SERVICE_DRIVE().files().list(q = "mimeType = 'application/vnd.google-apps.folder'",
    fields = 'files(id, name)').execute()
    for carpeta in carpetas['files']:
        nombre = carpeta.get('name')
        id_carpeta = carpeta.get('id')
        carpetas_en_drive[nombre] = id_carpeta
    for clave, valor in carpetas_en_drive.items():
        if id_ == clave:
            query = f"parents = '{valor}' and mimeType = 'application/vnd.google-apps.folder'"
            respuesta = SERVICE_DRIVE().files().list(q = query,
            fields = 'files(id, name)').execute()
            for archivos in respuesta.get('files', []):
                nombre_carpeta = archivos.get('name')
                carpeta_evaluacion = archivos.get('id')
                carpetas_profesores[nombre_carpeta] = carpeta_evaluacion
    for clave, valor in carpetas_profesores.items():
        query2 = f"parents = '{valor}' and mimeType = 'application/vnd.google-apps.folder'"
        respuesta2 = SERVICE_DRIVE().files().list(q = query2,
                                                  fields = 'files(id, name)').execute()
        for carpeta_alum in respuesta2.get('files', []):
            nombre_carpeta_alum = carpeta_alum.get('name')
            carpeta_id_alum = carpeta_alum.get('id')
            carpetas_alumnos[nombre_carpeta_alum] = carpeta_id_alum
    for clave, valor in carpetas_alumnos.items():
        if clave == nombre_alumno:
            print("El archivo tiene que pasar de gmail a drive")

def padron_con_nombre(alumnos):
    with open("alumnos.csv", mode= 'r',newline= '', encoding= "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv,delimiter=',')
        for linea in csv_reader:
            alumnos[linea[1]] = linea[0]
    
def main():
    alumnos = {}
    padron_con_nombre(alumnos)
    importar_archivos(alumnos)

main()