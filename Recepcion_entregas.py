import base64
from email.mime.text import MIMEText
from email import errors
import os
import csv

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
ARCHIVO_SECRET_CLIENT = 'client_secret.json'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]
def leer_asunto() -> None:
    credencial = create_credencial()
    serv= build('gmail', 'v1', credentials=credencial)
    resultados = serv.users().messages().list(userId='me').execute()
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
                return asunto

def create_credencial():
    if os.path.exists('token.json'):
        with open('token.json', 'r'):
            credencial = Credentials.from_authorized_user_file('token.json', SCOPES)
    return credencial

def lista_alumnos(alumnos, padrones, mail_alumnos) -> list:
    with open("alumnos.csv", mode= 'r',newline= '', encoding= "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv,delimiter=',')
        for linea in csv_reader:
            alumnos.append(linea[0])
            padrones.append(linea[1])
            mail_alumnos.append(linea[2])
    
def mail_docentes(profesores):
    with open("docentes.csv", mode= 'r',newline= '', encoding= "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv,delimiter=',')
        for linea in csv_reader:
            profesores[linea[0]]=linea[1]

def correctores(docente_alumno):
    with open("docente-alumno.csv", mode= 'r',newline= '', encoding= "UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv,delimiter=',')
        for linea in csv_reader:
            if linea[0] in docente_alumno:
                docente_alumno[linea[0]]+=(", "+ linea[1])
            else :
                docente_alumno[linea[0]]=linea[1]

def enviar_mensaje(alumnos, padrones, mail_alumnos, mail_profesores, docente_alumno)-> None:
    credencial = create_credencial()
    serv= build('gmail', 'v1', credentials=credencial)
    
    for i in alumnos:
        for n in docente_alumno:
            if alumnos[i] in docente_alumno[n]:
                gmail_de = mail_profesores[n]
        gmail_para = mail_alumnos[i]
        if leer_asunto()[1] == padrones[i]:
            mensaje ="La entrega fue exitosa"
        elif leer_asunto() not in padrones:
            mensaje ="padron incorrecto"
    
    asunto ="La entrega fue..."

    message = MIMEText(mensaje)
    message['to'] = gmail_para
    message['from'] = gmail_de
    message['subject'] = asunto
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body= {'raw': raw}
    try:
        message = (serv.users().messages().send(userId='me', body=body).execute())
        print ("Mensaje enviado")
    except errors.MessageError as error:
        print ('An error occurred: %s' % error)



def main():
    alumnos = []
    padrones=[]
    mail_alumnos=[]
    profesores={}
    docente_alumno={}
    lista_alumnos(alumnos, padrones, mail_alumnos)
    mail_docentes(profesores)
    correctores(docente_alumno)
    print (leer_asunto())

main()
