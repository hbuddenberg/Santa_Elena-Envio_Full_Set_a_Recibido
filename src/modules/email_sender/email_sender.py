import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.http import MediaFileUpload
from email.header import Header  # Importar Header

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/drive.file']
#SCOPES=['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.metadata']
CONFIG_PATH = 'src/configuration'

def autenticar():
    """
    Autentica al usuario con OAuth 2.0 y devuelve las credenciales.
    """
    creds = None
    token_path = os.path.join(CONFIG_PATH, 'token.json')
    credentials_path = os.path.join(CONFIG_PATH, 'credentials.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError as error:
                print(f"Error al refrescar el token: {error}")
                os.remove(token_path)  # Delete the token file to force re-authentication
                return autenticar()  # Retry authentication
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
            print(f"Visita esta URL para autorizar la aplicación: {auth_url}")
            creds = flow.run_local_server(port=8989)

        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    return creds

def subir_archivo_a_drive(service, archivo):
    file = None
    try:
        file_metadata = {'name': os.path.basename(archivo)}
        media = MediaFileUpload(archivo, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    except Exception as e:
        print(f"Error al subir el archivo {archivo} a Drive: {e}")
    return file.get('id')

def obtener_enlace_drive(service, file_id):
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    service.permissions().create(fileId=file_id, body=permission).execute()
    link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
    return link

def enviar_correo_api(configuracion, destinatarios, asunto, cuerpo_html, archivos_adjuntos=None, cc=None, bcc=None):
    """
    Envía un correo utilizando la API de Gmail con OAuth 2.0.

    Args:
        destinatarios (list): Lista de destinatarios del correo.
        asunto (str): Asunto del correo.
        cuerpo_html (str): Contenido HTML del correo.
        archivos_adjuntos (list): Lista de rutas de archivos adjuntos.
        cc (list): Lista de destinatarios en copia.
        bcc (list): Lista de destinatarios en copia oculta.

    Returns:
        dict: Diccionario con el estado y la descripción del resultado.
    """
    creds = autenticar()
    try:
        service = build('gmail', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        message = MIMEMultipart()

        # Validación y asignación de destinatarios
        if destinatarios and isinstance(destinatarios, list):
            message['To'] = ", ".join(destinatarios)
        else:
            raise ValueError("No se especificaron destinatarios o el formato es inválido.")

        # Validación y asignación de CC
        if cc and isinstance(cc, list):
            cc_limpio = [correo.strip() for correo in cc if correo.strip()]
            if cc_limpio:
                message['Cc'] = ", ".join(cc_limpio)

        # Validación y asignación de BCC
        if bcc and isinstance(bcc, list):
            bcc_limpio = [correo.strip() for correo in bcc if correo.strip()]
            if bcc_limpio:
                message['Bcc'] = ", ".join(bcc_limpio)

        # Asignar asunto y contenido del mensaje
        message['Subject'] = asunto
        message.attach(MIMEText(cuerpo_html, 'html'))

        # Adjuntar archivos o subir a Drive si son mayores a 25 MB
        if archivos_adjuntos:
            total_size = sum(os.path.getsize(archivo) for archivo in archivos_adjuntos)
            if total_size <= 25 * 1024 * 1024:  # 25 MB
                for archivo in archivos_adjuntos:
                    archivo_normalizado = str(archivo).replace('\\', '/')
                    if not os.path.isfile(archivo_normalizado):
                        raise ValueError(f"Archivo no encontrado: {archivo_normalizado}")

                    with open(archivo_normalizado, 'rb') as adjunto:
                        mime_base = MIMEBase('application', 'octet-stream')
                        mime_base.set_payload(adjunto.read())
                        encoders.encode_base64(mime_base)
                        nombre_archivo = Header(os.path.basename(archivo_normalizado), 'utf-8').encode()
                        mime_base.add_header('Content-Disposition', f'attachment; filename="{nombre_archivo}"')
                        message.attach(mime_base)
            else:
                enlaces_drive = []
                for archivo in archivos_adjuntos:
                    file_id = subir_archivo_a_drive(drive_service, archivo)
                    enlace = obtener_enlace_drive(drive_service, file_id)
                    enlaces_drive.append(enlace)
                cuerpo_html += "<br><br>Archivos adjuntos:<br>" + "<br>".join(enlaces_drive)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {'raw': raw_message}

        send = service.users().messages().send(userId="me", body=send_message).execute()
        if 'SENT' in send.get('labelIds', []):
            descripcion = "Correo enviado correctamente."
            print(descripcion)
            return {'estado': True, 'descripcion': descripcion}
        else:
            descripcion = "El correo no pudo ser enviado."
            print(descripcion)
            return {'estado': False, 'descripcion': descripcion}

    except HttpError as error:
        descripcion = f"Un error ocurrió: {error}"
        print(descripcion)
        return {'estado': False, 'descripcion': descripcion}
    except Exception as e:
        descripcion = f"Ocurrió un error inesperado: {e}"
        print(descripcion)
        return {'estado': False, 'descripcion': descripcion}

def envio_correo_smtp(config_global, configuracion, destinatarios, asunto, cuerpo_html, archivos_adjuntos=None, cc=None, bcc=None):
    """
    Envía un correo usando Gmail.

    Args:
        destinatarios (list): Lista de correos electrónicos de los destinatarios principales.
        asunto (str): Asunto del correo.
        cuerpo_html (str): Contenido del correo en formato HTML.
        archivos_adjuntos (list): Lista de rutas de archivos a adjuntar (opcional).
        cc (list): Lista de correos electrónicos en copia (opcional).
        bcc (list): Lista de correos electrónicos en copia oculta (opcional).

    Returns:
        dict: Diccionario con el estado y la descripción del resultado.
    """
    GMAIL_USER = configuracion['gmail_user']
    GMAIL_PASSWORD = configuracion['gmail_password']
    SMTP_SERVER = configuracion['smtp_server']
    SMTP_PORT = configuracion['smtp_port']

    try:
        # Configurar el correo
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = ", ".join(destinatarios)
        msg['Cc'] = ", ".join(cc) if cc else ""
        msg['Bcc'] = ", ".join(bcc) if bcc else ""
        msg['Subject'] = asunto

        # Adjuntar contenido HTML
        msg.attach(MIMEText(cuerpo_html, 'html'))

        # Adjuntar archivos
        if archivos_adjuntos:
            for archivo in archivos_adjuntos:
                with open(archivo, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(archivo)}')
                    msg.attach(part)

        # Conectar al servidor y enviar el correo
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, destinatarios + (cc or []) + (bcc or []), msg.as_string())
            descripcion = "Correo enviado correctamente."
            print(descripcion)
            return {'estado': True, 'descripcion': descripcion}

    except Exception as e:
        descripcion = f"Error al enviar el correo: {e}"
        print(descripcion)
        return {'estado': False, 'descripcion': descripcion}
    
def main():
    import sys
    import os

    #sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    #sys.path.append('D:/Dev/Santa_Elena-Envio_Full_Set_a_Recibido')
    sys.path.append('/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido')

    from src.modules.configuracion import Configuracion as Configuracion_Yaml
    from src.modules.extraer_excel import Configuracion as Configuracion_Excel

    CONFIG_GLOBAL = Configuracion_Yaml('src/configuration/configuracion.yaml')
    CONFIG_EXCEL = Configuracion_Excel(CONFIG_GLOBAL.config.path.shared.config)

    
    configuracion = CONFIG_GLOBAL
    destinatarios = ['h.buddenberg@gmail.com']
    asunto = 'FULL SET OF DOCS REF 242500170 - 242500171 -242500172 -CHARLES ISLAND - DIVINE (ETA 21-03-2025)'
    cuerpo_html = '\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <meta http-equiv="X-UA-Compatible" content="ie=edge">\n  <title>Orden de Embarque</title>\n  <style>\n    body {\n      margin: 0;\n      padding: 0;\n      background-color: #f4f4f4;\n      font-family: Arial, sans-serif;\n    }\n\n    table {\n      border-spacing: 0;\n      width: 100%;\n    }\n\n    img {\n      display: block;\n      max-width: 100%;\n      height: auto;\n    }\n\n    .email-container {\n      max-width: 600px;\n      margin: 0 auto;\n      background-color: #ffffff;\n      border: 1px solid #e0e0e0;\n      border-radius: 8px;\n    }\n\n    .email-header {\n      padding: 10px 0;\n      text-align: center;\n      background-color: #ffffff;\n      border-bottom: 1px solid #e0e0e0;\n    }\n\n    .email-header img {\n      margin: 0 auto;\n      display: inline-block;\n      width: 100px;\n      height: auto;\n    }\n\n    .email-content {\n      padding: 20px;\n      color: #333333;\n      line-height: 1.6;\n    }\n\n    .email-footer {\n      text-align: center;\n      padding: 10px;\n      background-color: #f9fafb;\n      border-top: 1px solid #e0e0e0;\n      font-size: 11px;\n      color: #666666;\n    }\n  </style>\n</head>\n\n<body>\n  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4;">\n    <tr>\n      <td align="center">\n        <table class="email-container" cellpadding="0" cellspacing="0">\n          <!-- Header -->\n          <tr>\n            <td class="email-header">\n              <img src="https://smart-bots.cl/logo_santahelena.jpg" alt="Company Logo">\n            </td>\n          </tr>\n\n          <!-- Content -->\n          <tr>\n            <td class="email-content">\n              <p>Dear <br>\nPlease find attached The Following docs : <br>\n<br>\n- Bill of Lading (SWB) <br>\n- Invoice<br>\n - Certificate Of Origin <br>\n- Phytosanitary certificate <br>\n- Packing List <br>\n<br>\n<b>Docs are send only by Email, if you need docs phisically please advise, Thanks!<br>\n In case of questions, send email to comex@santaelena.com, comex2@santaelena.com, comexasistente@santaelena.com  <br>\n<br>\nBest Regards!! </b></p>\n            </td>\n          </tr>\n\n          <!-- Footer -->\n          <tr>\n            <td class="email-footer">\n                <p> &copy; 2025 Exportadora Santa Elena S.A. </p>\n            </td>\n          </tr>\n        </table>\n      </td>\n    </tr>\n  </table>\n</body>\n\n</html>\n'
    archivos_adjuntos = ['/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS REF 242500170 - 242500171 -242500172 -CHARLES ISLAND - DIVINE (ETA 21-03-2025)/30mb.zip', '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS REF 242500170 - 242500171 -242500172 -CHARLES ISLAND - DIVINE (ETA 21-03-2025)/FULL SET OE242500170 - CHARLES ISLAND - DIVINE.pdf', '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS REF 242500170 - 242500171 -242500172 -CHARLES ISLAND - DIVINE (ETA 21-03-2025)/FULL SET OE242500171 - CHARLES ISLAND - DIVINE.pdf', '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS REF 242500170 - 242500171 -242500172 -CHARLES ISLAND - DIVINE (ETA 21-03-2025)/FULL SET OE242500172 - CHARLES ISLAND - DIVINE.pdf', '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS REF 242500170 - 242500171 -242500172 -CHARLES ISLAND - DIVINE (ETA 21-03-2025)/FULL SET OF DOCS REF 242500170 - 242500171 -242500172 -CHARLES ISLAND - DIVINE (ETA 21-03-2025).7z', '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS REF 242500170 - 242500171 -242500172 -CHARLES ISLAND - DIVINE (ETA 21-03-2025)/PACKING LIST OE242500170_CHARLES ISLAND_DIVINE.xls', '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS REF 242500170 - 242500171 -242500172 -CHARLES ISLAND - DIVINE (ETA 21-03-2025)/PACKING LIST OE242500171_CHARLES ISLAND_DIVINE.xls', '/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/En Proceso/FULL SET OF DOCS REF 242500170 - 242500171 -242500172 -CHARLES ISLAND - DIVINE (ETA 21-03-2025)/PACKING LIST OE242500172_CHARLES ISLAND_DIVINE.xls']
    cc=None
    bcc=None
    
    status = enviar_correo_api(configuracion, destinatarios, asunto, cuerpo_html, archivos_adjuntos, cc, bcc)
    print(status)


if __name__ == "__main__":
    main()