from service_drive import obtener_servicio as SERVICE_DRIVE
from service_gmail import obtener_servicio as SERVICE_GMAIL
import csv
    
def importar_archivos() -> None:
    #PRE lee los mails #
    #POST si el mail esta en condiciones, envia el archivo a la carpeta que se nombra#
    
    nombres = []
    padrones=[]
    alumnos(nombres, padrones)
    resultados = SERVICE_GMAIL().users().messages().list(userId='me').execute()
    id_mails = []
    contador = 0
    for mail in resultados['messages']:
        mail_ID = (resultados['messages'][contador]['id'])
        id_mails.append(mail_ID)
        contador += 1
    for id_mail in id_mails:
        mail = SERVICE_GMAIL().users().messages().get(userId='me', id=id_mail, format='full').execute()
        for valor in mail['payload']['filename']:
            if valor['body']:
                att_id=valor['attachmentId']
                att=SERVICE_GMAIL().users().messages().attachments().get(userId='me', messageId=id_mail,id=att_id).execute()
        for valor in mail['payload']['headers']:
            if valor['name'] == 'Subject':
                asunto = (valor['value']).split()
                for i in range (len(padrones)):
                    if asunto[1] == padrones[i]:
                        carpeta_id= buscar_carpeta(nombres[i])
                        SERVICE_DRIVE.files().update(fileId = att, addParents = carpeta_id,).execute()
            

def buscar_carpeta(nombre_alumno: str) ->  str:
    #PRE Entra en cada carpeta#
    #POST Dependiendo del nombre selecciona la carpeta#
    
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
            respuesta = SERVICE_DRIVE().files().list(q = query, fields = 'files(id, name)').execute()
            for archivos in respuesta.get('files', []):
                nombre_carpeta = archivos.get('name')
                carpeta_evaluacion = archivos.get('id')
                carpetas_profesores[nombre_carpeta] = carpeta_evaluacion
    for clave, valor in carpetas_profesores.items():
        for carpeta_alum in respuesta.get('files', []):
            nombre_carpeta_alum = carpeta_alum.get('name')
            carpeta_id_alum = carpeta_alum.get('id')
            carpetas_alumnos[nombre_carpeta_alum] = carpeta_id_alum
    for clave, valor in carpetas_alumnos.items():
        if clave == nombre_alumno:
            print("El archivo tiene que pasar de gmail a drive")
            return carpeta_id_alum

def alumnos(nombres: list, padrones: list)-> None:
    #PRE 2 listas vacias#
    #POST llena las listas con los nombres y padrones#
    
    with open("alumnos.csv", mode= 'r',newline= '', encoding= "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv,delimiter=',')
        for linea in csv_reader:
            nombres.append(linea[0])
            padrones.append(linea[1])
    
def main():
    importar_archivos()

main()
