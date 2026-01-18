from datetime import datetime

from .email_sender_vacio import enviar_correo_api, envio_correo_smtp


def enviar_vacio(configuracion, excel, tipo="api"):
    if tipo not in ["smtp", "api"]:
        raise ValueError("El tipo de envío debe ser 'smtp' o 'api'.")

    asunto = f"Informe de ejecucion Envio Correo a Recibidores - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    with open(configuracion.config.mail.template.empty, "r") as file:
        cuerpo_html = file.read()

    cuerpo_html = str(cuerpo_html)

    destinatarios = [email.strip() for email in excel.config.email_reporte[0].lista_emails.replace(";", ",").split(",")]
    copia = [email.strip() for email in configuracion.config.mail.sender.report.cc.replace(";", ",").split(",")]
    oculto = [email.strip() for email in configuracion.config.mail.sender.report.cco.replace(";", ",").split(",")]

    if tipo == "api":
        status = enviar_correo_api(configuracion, destinatarios, asunto, cuerpo_html, [], copia, oculto)
    else:
        status = envio_correo_smtp(
            configuracion,
            configuracion.config.mail.config.smtp,
            destinatarios,
            asunto,
            cuerpo_html,
            [],
            copia,
            oculto,
        )

    return status
