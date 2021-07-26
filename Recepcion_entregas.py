import base64
from email.mime.text import MIMEText
from email import errors
import os

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
ARCHIVO_SECRET_CLIENT = 'client_secret.json'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def enviar_mensaje():
    credencial = None

    if os.path.exists('token.json'):
        with open('token.json', 'r'):
            credencial = Credentials.from_authorized_user_file('token.json', SCOPES)

    gmail_de = "ljun@fi.uba.ar"
    gmail_para = "ljun@fi.uba.ar"
    asunto ="La entrega fue..."
    mensaje ="La entrega fue exitosa"

    message = MIMEText(mensaje)
    message['to'] = gmail_para
    message['from'] = gmail_de
    message['subject'] = asunto
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body= {'raw': raw}
    serv= build('gmail', 'v1', credentials=credencial)
    try:
        message = (serv.users().messages().send(userId='me', body=body).execute())
        print ("Mensaje enviado")
    except errors.MessageError as error:
        print ('An error occurred: %s' % error)

def main():
    enviar_mensaje()

main()
