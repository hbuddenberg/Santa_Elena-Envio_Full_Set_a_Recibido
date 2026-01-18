import logging
import os
from datetime import datetime
from time import sleep

from modules.compresor import validar_archivos
from modules.configuracion import Configuracion as Configuracion_Yaml
from modules.email_sender import enviar_informe, enviar_reciver, enviar_vacio
from modules.estructurar_registro import estructurar
from modules.extraer_excel import Configuracion as Configuracion_Excel
from modules.informe import genera_informe
from modules.listar_archivos import listar_archivos

# Configuración del registro de log
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = os.path.join(log_dir, f"execution_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
logging.basicConfig(
    filename=log_filename,
    level=print,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

CONFIG_GLOBAL = Configuracion_Yaml("src/configuration/configuracion.yaml")
CONFIG_EXCEL = Configuracion_Excel(CONFIG_GLOBAL.config.path.local.config + "/Plantilla_de_Configuracion.xlsx")


def generacion_informe(registros, ruta):
    print("Generando informe.")
    nombre_archivo = f"Informe_Envio_Recibidor_{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}.xlsx"
    for registro in registros:
        archivo_informe = genera_informe(registro, ruta, nombre_archivo)
    return archivo_informe


def registros(carpetas: dict):
    lista_ejecucion = []
    print("Iniciando el proceso de registros.")
    for folder, files in carpetas["carpetas"].items():
        print(f"Ejecutando: {folder}")
        print(f"Archivos: {files}")
        ruta = f"{carpetas['ruta']['en_proceso']}/{folder}"
        files, tamaño_total = validar_archivos(files, ruta, folder)
        print(f"Tamaño total de los archivos: {tamaño_total} MB")
        estructura = estructurar(folder, files, CONFIG_EXCEL)
        print(f"Estructura: {estructura.to_dict()}")
        if estructura.emails_para not in (None, ""):
            if tamaño_total <= 25:
                status = enviar_reciver(CONFIG_GLOBAL, ruta, files, estructura, "api")
            else:
                status = {"estado": False, "descripcion": f"Archivos mayores a 25MB, tamaño total {tamaño_total} MB"}
            print(f"Estado Correo: {status}")
        else:
            print(f"Correo para: {estructura.emails_para}")
            status = {"estado": False, "descripcion": "Correos de Recibidor o Recibidor no encontrado."}

        lista_ejecucion.append(
            {
                "carpeta": folder,
                "ruta": ruta,
                "archivos": files,
                "estructura": estructura.to_dict(),
                "estado_correo": status,
            }
        )

    if len(lista_ejecucion) > 0:
        sleep(1)
        archivo_informe = generacion_informe(lista_ejecucion, carpetas["ruta"]["en_proceso"])
        enviar_informe(CONFIG_GLOBAL, CONFIG_EXCEL, archivo_informe, lista_ejecucion, "api")
        # mover_todo(CONFIG_GLOBAL.config.path.shared.main) # Comentado porque ahora movemos via API en el nivel superior

    return lista_ejecucion


from modules.google_api.client import DriveClient
from modules.google_api.service import DriveService


def get_drive_service():
    scopes = CONFIG_GLOBAL.config.mail.config.api.scopes + ["https://www.googleapis.com/auth/drive"]
    client = DriveClient(
        credentials_path=CONFIG_GLOBAL.config.mail.config.api.credentials,
        token_path=CONFIG_GLOBAL.config.mail.config.api.token,
        scopes=scopes,
    )
    return DriveService(client)


def procesar_nuevas_carpetas(drive_service: DriveService):
    print("Buscando carpetas en Google Drive...")

    # Resolver ID de carpeta raíz
    root_path_name = CONFIG_GLOBAL.config.path.drive.root_path
    try:
        root_id = drive_service.find_folder_id_by_path(root_path_name)
    except FileNotFoundError:
        logging.error(f"No se encontró la carpeta raíz en Drive: {root_path_name}")
        return

    # Buscar carpetas que NO sean 'En Proceso' o 'Finalizados' (o config)
    carpetas_drive = drive_service.list_folders_in_folder(root_id)
    folder_ignore = [
        CONFIG_GLOBAL.config.path.drive.in_progress,
        CONFIG_GLOBAL.config.path.drive.done,
        "Configuracion",
    ]

    # Crear carpeta 'En Proceso' local temporal si no existe
    local_temp_process = os.path.join(CONFIG_GLOBAL.config.path.local.main, "temp_process")
    if not os.path.exists(local_temp_process):
        os.makedirs(local_temp_process)

    # Identificar carpetas especiales en Drive para mover luego
    id_finalizados = None
    try:
        id_finalizados = drive_service.find_folder_id_by_path(CONFIG_GLOBAL.config.path.drive.done, root_id)
    except:
        logging.warning("Carpeta 'Finalizados' no encontrada en Drive.")

    lista_ejecucion_total = []

    for folder in carpetas_drive:
        if folder["name"] in folder_ignore:
            continue

        print(f"Procesando carpeta de Drive: {folder['name']}")

        # Descargar a temporal local
        local_folder_path = os.path.join(local_temp_process, folder["name"])
        drive_service.download_folder(folder["id"], local_folder_path)

        # Construir estructura similar a lo que espera 'registros'
        # Emulamos el diccionario que devolvía 'mover_carpetas_enproceso'
        carpeta_dict = {
            "ruta": {"en_proceso": local_temp_process},
            "carpetas": {folder["name"]: listar_archivos(local_folder_path)},
        }

        # Ejecutar lógica de negocio existente
        try:
            resultado = registros(carpeta_dict)
            lista_ejecucion_total.extend(resultado)

            # Si todo salió bien, mover en Drive a Finalizados
            if id_finalizados:
                print(f"Moviendo carpeta {folder['name']} a Finalizados en Drive...")
                drive_service.move_file(folder["id"], id_finalizados)

        except Exception as e:
            logging.error(f"Error procesando carpeta {folder['name']}: {e}")

        # Limpieza local (opcional, pero recomendada)
        # shutil.rmtree(local_folder_path)

    return lista_ejecucion_total


def ejecutar():
    print("Ejecutando el proceso principal (Modo Google Drive API).")
    try:
        service = get_drive_service()
        procesar_nuevas_carpetas(service)
    except Exception as e:
        logging.error(f"Error crítico en ejecución: {e}")
        # Fallback a enviar vacío si es necesario, o manejar error
        enviar_vacio(CONFIG_GLOBAL, CONFIG_EXCEL, "api")


def main():
    print("Iniciando el programa.")
    ejecutar()


if __name__ == "__main__":
    main()
