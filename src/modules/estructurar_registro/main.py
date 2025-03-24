#from models import CasoExportacion
from src.models import CasoExportacion

def obtener_recibidor(carpeta):
    try:
        recibidor = carpeta[::-1].split('(')[-1].split('-')[0].strip()[::-1]
    except:
        recibidor = None
    return recibidor

def obtener_destinatarios(recibidor, excel):
    destinatarios = []
    for item in excel.config.recibidores_emails:
        if item.recibidor == recibidor:
            destinatarios = item
            break
    if not destinatarios:
        print(f"recibidor {recibidor} no encontrado en la configuración.")
    return destinatarios

def obtener_distribucion(distribucion, excel):
    distribucion_correos = []
    for item in excel.config.distribucion_correos:
        if item.emails_para == distribucion:
            distribucion_correo = item
            break
    if not distribucion_correo:
        print(f"recibidor {distribucion_correo} no encontrado en la configuración.")
    try:
        return distribucion_correo
    except Exception as e:
        print(f"Error al obtener la distribución: {e}")
        return []

def obtener_copia(cc, excel):
    copia = []
    for item in excel.config.resumen_cc:
        if item.cc.strip() == cc:
            copia = item
            break
    if not copia:
        print(f"recibidor {copia} no encontrado en la configuración.")
    return copia

def obtener_reporte(excel):
    email_reporte = []
    for item in excel.config.email_reporte:
            email_reporte = item
            break
    if not email_reporte:
        print(f"recibidor {email_reporte} no encontrado en la configuración.")
    return email_reporte

def estructurar(carpeta, archivos,excel):
    distribucion_correo = ''
    pais = ''
    lista_mail_recibidor = ''
    cuerpo_distribucion_correo = ''
    asunto = carpeta
    recibidor = obtener_recibidor(carpeta)
    mail_recibidor = obtener_destinatarios(recibidor, excel)
    try:
        distribucion_correo = obtener_distribucion(mail_recibidor.distribucion_correos, excel)
        pais = distribucion_correo.pais
        lista_mail_recibidor = mail_recibidor.lista_emails
        cuerpo_distribucion_correo = distribucion_correo.cuerpo
    except:
        distribucion_correo = ''
        pais = ''
        lista_mail_recibidor = ''
        cuerpo_distribucion_correo = ''
    resumen_cc = obtener_copia('SANTA ELENA',excel)

    caso_exportacion = CasoExportacion()
    caso_exportacion.set(
        recibidor=recibidor,
        pais=pais,
        emails_para=lista_mail_recibidor,
        emails_copia=resumen_cc.lista_emails,
        adjuntos=archivos,
        asunto=asunto,
        cuerpo=cuerpo_distribucion_correo
    )

    return caso_exportacion

def main(ruta):
    print(f"Procesando carpeta: {ruta}")

if __name__ == "__main__":
    carpeta = 'FULL SET OF DOCS OE232400007- MSC CASSANDRE- DIVINE (ETA 03-02-2024)'
    main(carpeta)