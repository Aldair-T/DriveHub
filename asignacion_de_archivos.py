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

            #utilizar nombre para guardar archivo en carpeta
        

def padron_con_nombre(alumnos):
    with open("alumnos.csv", mode= 'r',newline= '', encoding= "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv,delimiter=',')
        for linea in csv_reader:
            alumnos[linea[1]] = linea[0]
    

def main():
    alumnos = {}
    padron_con_nombre(alumnos)
    importar_archivos(alumnos)


    
            



