import base64
from email.mime.text import MIMEText
from email import errors
import os
import csv

from AsignacionArchivos import importar_archivos

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

ARCHIVO_SECRET_CLIENT = 'client_secret.json'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def leer_asunto(alumnos: list, padrones: list, mail_alumnos: list, profesores: dict, docente_alumno: dict) -> None:
    credencial = create_credencial()
    serv= build('gmail', 'v1', credentials=credencial)
    resultados = serv.users().messages().list(userId='me', q="is:unread").execute()
    id_mails = []
    contador = 0
    for mail in resultados['messages']:
        mail_ID = (resultados['messages'][contador]['id'])
        id_mails.append(mail_ID)
        contador += 1
    for id_mail in id_mails:
        mail = serv.users().messages().get(userId='me', id=id_mail, format='metadata').execute()
        for valor in mail['payload']['headers']:
            if valor['name'] == 'Subject':
                asunto = (valor['value']).split()
            if valor['name'] == 'From':
                de = (valor['value']).split()
            if valor['name'] == 'To':
                para = (valor['value']).split()
                for i in range (len (alumnos)):
                    if asunto[1] == padrones[i] and asunto[2]== "-" and asunto[4]== alumnos[i] and para[2] == profesores[docente_alumno[alumnos[i]]] and de[2] in mail_alumnos:
                        return ("La entrega fue exitosa")
                    elif asunto[1] != padrones[i] and asunto[2]== "-" or asunto[4]!= alumnos[i]:
                        return ("nombre no coincide con padron")
                    elif asunto[1] not in padrones:
                        return ("padron incorrecto")
                    elif de[2] not in mail_alumnos:
                        return ("enviado con mail que no corresponde")
                    else:
                        return  ("entrega fallida")

def create_credencial() -> Credentials:
    if os.path.exists('token.json'):
        with open('token.json', 'r'):
            credencial = Credentials.from_authorized_user_file('token.json', SCOPES)
    return credencial

def lista_alumnos(alumnos: list, padrones: list, mail_alumnos: list) -> None:
    with open("alumnos.csv", mode= 'r',newline= '', encoding= "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv,delimiter=',')
        for linea in csv_reader:
            alumnos.append(linea[0])
            padrones.append(linea[1])
            mail_alumnos.append("<"+linea[2]+">")
    
def mail_docentes(profesores: dict)-> None:
    with open("docentes.csv", mode= 'r',newline= '', encoding= "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv,delimiter=',')
        for linea in csv_reader:
            profesores[linea[0]]="<"+linea[1]+">"

def correctores(docente_alumno: dict)-> None:
    with open("docente-alumno.csv", mode= 'r',newline= '', encoding= "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv,delimiter=',')
        for linea in csv_reader:
            docente_alumno[linea[1]]=linea[0]

def enviar_mensaje()-> None:
    alumnos = []
    padrones=[]
    mail_alumnos=[]
    profesores={}
    docente_alumno={}
    lista_alumnos(alumnos, padrones, mail_alumnos)
    mail_docentes(profesores)
    correctores(docente_alumno)
    credencial = create_credencial()
    serv= build('gmail', 'v1', credentials=credencial)
    
    for i in range(len(alumnos)):
        if alumnos[i] in docente_alumno:
            gmail_de = profesores[docente_alumno[alumnos[i]]]
        gmail_para = mail_alumnos[i]
        mensaje = leer_asunto(alumnos, padrones, mail_alumnos, profesores, docente_alumno)
        if mensaje == "La entrega fue exitosa":
            importar_archivos()
    
    message = MIMEText(mensaje)
    message['to'] = gmail_para
    message['from'] = gmail_de
    message['subject'] = "Entrega"
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body= {'raw': raw}
    try:
        message = (serv.users().messages().send(userId='me', body=body).execute())
        print ("Mensaje enviado")
    except errors.MessageError as error:
        print ('An error occurred: %s' % error)


def main()-> None:
    enviar_mensaje()

main()
