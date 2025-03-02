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
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
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
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
                print(f"Visita esta URL para autorizar la aplicación: {auth_url}")
                creds = flow.run_local_server(port=8989)

            with open(token_path, 'w') as token_file:
                token_file.write(creds.to_json())

    return creds

def enviar_correo_api(configuracion, destinatarios, asunto, cuerpo_html, archivos_adjuntos=None,  cc=None, bcc=None):
    """
    Envía un correo utilizando la API de Gmail con OAuth 2.0.

    Args:
        destinatarios (list): Lista de destinatarios del correo.
        asunto (str): Asunto del correo.
        cuerpo_html (str): Contenido HTML del correo.
        archivos_adjuntos (list): Lista de rutas de archivos adjuntos.
        cc (list): Lista de destinatarios en copia.

    Returns:
        bool: True si el correo se envió correctamente, False en caso contrario.
    """
    creds = autenticar()
    try:
        service = build('gmail', 'v1', credentials=creds)
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

        # Adjuntar archivos
        if archivos_adjuntos:
            for archivo in archivos_adjuntos:
                # Normalizar la ruta del archivo
                archivo_normalizado = str(archivo).replace('\\','/')

                # Verificar si el archivo existe
                if not os.path.isfile(archivo_normalizado):
                    raise ValueError(f"Archivo no encontrado: {archivo_normalizado}")

                # Abrir y adjuntar el archivo al mensaje
                with open(archivo_normalizado, 'rb') as adjunto:
                    mime_base = MIMEBase('application', 'octet-stream')
                    mime_base.set_payload(adjunto.read())
                    encoders.encode_base64(mime_base)

                    # Codificar el nombre del archivo para evitar problemas con caracteres especiales
                    from email.header import Header
                    nombre_archivo = Header(os.path.basename(archivo_normalizado), 'utf-8').encode()

                    # Agregar encabezado de Content-Disposition con el nombre del archivo codificado
                    mime_base.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{nombre_archivo}"'
                    )
                    try:
                        message.attach(mime_base)
                        print(f"Archivo {os.path.basename(archivo_normalizado)} adjuntado correctamente.")
                    except Exception as e:
                        raise ValueError(f"Error al adjuntar el archivo {os.path.basename(archivo_normalizado)}: {e}")


        # Construir y enviar el mensaje
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = {'raw': raw_message}

        send = service.users().messages().send(userId="me", body=send_message).execute()
        if send['labelIds'][0] == 'SENT':
            descripcion = "Correo enviado correctamente."
            print(descripcion)
            return { 'estado': True, 'descripcion': descripcion }
        else:
            descripcion = f"El correo no pudo ser enviado."
            print(descripcion)
            return { 'estado': False, 'descripcion': descripcion }

    except HttpError as error:
        descripcion = f"Un error ocurrió: {error}"
        print(descripcion)
        return { 'estado': False, 'descripcion': descripcion }
    except Exception as e:
        descripcion = f"Ocurrió un error inesperado: {e}"
        print(descripcion)
        return { 'estado': False, 'descripcion': descripcion }

def envio_correo_smtp(config_global, configuracion, destinatarios, asunto, cuerpo_html, archivos_adjuntos=None, cc=None, bcc=None):
    """
    Envía un correo usando Gmail.

    Args:
        destinatarios (list): Lista de correos electrónicos de los destinatarios principales.
        asunto (str): Asunto del correo.
        cuerpo_html (str): Contenido del correo en formato HTML.
        archivos_adjuntos (list): Lista de rutas de archivos a adjuntar (opcional).
        cc (list): Lista de correos electrónicos en copia (opcional).

    Returns:
        bool: True si el correo fue enviado correctamente, False en caso contrario.
    """
    #from settings import GMAIL_USER, GMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

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
        #msg['Bcc'] = ", ".join(bcc) if bcc else ""
        msg['Subject'] = asunto

        # Adjuntar contenido HTML
        msg.attach(MIMEText(cuerpo_html, 'html'))

        # Adjuntar archivos
        if archivos_adjuntos:
            for archivo in archivos_adjuntos:
                with open(archivo, 'rb') as f:
                    from email.mime.base import MIMEBase
                    from email import encoders

                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(archivo)}')
                    msg.attach(part)

        # Conectar al servidor y enviar el correo
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            #server.sendmail(GMAIL_USER, destinatarios , msg.as_string())
            server.sendmail(GMAIL_USER, destinatarios + (cc or []) + (bcc or []), msg.as_string())
            descripcion = "Correo enviado correctamente."
            print(descripcion)
            return { 'estado': True, 'descripcion': descripcion }

    except Exception as e:
        descripcion = f"Error al enviar el correo: {e}"
        print(descripcion)
        return { 'estado': False, 'descripcion': descripcion }

def enviar_correo(configuracion, archivo_informe, lista_ejecucion, tipo='api'):
    if tipo not in ['smtp', 'api']:
        raise ValueError("El tipo de envío debe ser 'smtp' o 'api'.")

    asuntos_exitosos = [ejecucion['carpeta'] for ejecucion in lista_ejecucion if ejecucion['estado_correo']['estado']]

    
    asuntos_exitosos = [f"<li>{orden.diccionario['asuntos_exitosos']}</li>" for orden in asuntos_exitosos]

    asunto = f'Informe de ejecucion Carga de Instructivos de Ordenes de Embarque - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

    with open(configuracion['template'], 'r') as file:
        cuerpo_html = file.read()

    cuerpo_html = str(cuerpo_html).replace('{asuntos_exitosos}', ''.join(asuntos_exitosos))

    destinatarios = [email.strip() for email in configuracion['envio']['destinatarios'].replace(';', ',').split(',')]
    copia = [email.strip() for email in configuracion['envio']['copia'].replace(';', ',').split(',')]
    oculto = [email.strip() for email in configuracion['envio']['oculta'].replace(';', ',').split(',')]

    if tipo == 'api':
        enviar_correo_api(destinatarios, asunto, cuerpo_html, [archivo_informe], copia, oculto)
    else:
        envio_correo_smtp(configuracion['configuracion'], destinatarios, asunto, cuerpo_html, [archivo_informe], copia, oculto)
