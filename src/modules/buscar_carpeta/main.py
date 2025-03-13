import os
import logging
import argparse

# Configuración del logger
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(filename=os.path.join(log_dir, 'buscar_carpeta.log'),
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
def buscar_existencia(ruta):
    logging.info(f"Iniciando búsqueda de la carpeta en la ruta: {ruta}")
    if os.path.exists(ruta):
        logging.info(f"Carpeta encontrada en la ruta: {ruta}")
        existe = True
    else:
        logging.warning(f"Carpeta no encontrada en la ruta: {ruta}")
        existe = False
    return existe
def listar_carpetas(ruta):
    logging.info(f"Listando carpetas en la ruta: {ruta}")
    #carpetas = [os.path.join(ruta, nombre) for nombre in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, nombre))]
    carpetas = [nombre for nombre in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, nombre))]
    logging.info(f"Carpetas listadas en la ruta {ruta}: {carpetas}")
    carpetas = sorted(carpetas)
    return carpetas
def buscar_carpeta(ruta):
    logging.info(f"Ruta proporcionada: {ruta}")
    if buscar_existencia(ruta):
        carpetas = listar_carpetas(ruta)
        logging.info(f"Carpetas encontradas: {carpetas}")
    else:
        carpetas = []
        logging.warning(f"No se encontró la carpeta en la ruta: {ruta}")
    return carpetas
def main():
    # Parseo de argumentos
    logging.info("Iniciando el parseo de argumentos")
    parser = argparse.ArgumentParser(description='Buscar y listar carpetas en una ruta especificada.')
    parser.add_argument('ruta', type=str, help='Ruta de la carpeta a buscar y listar')
    args = parser.parse_args()

    # Lógica principal del programa
    ruta = args.ruta
    logging.info(f"Ruta proporcionada: {ruta}")
    if buscar_existencia(ruta):
        carpetas = listar_carpetas(ruta)
        print(f"Carpetas encontradas: {carpetas}")
        logging.info(f"Carpetas encontradas: {carpetas}")
    else:
        carpetas = []
        print(f"No se encontró la carpeta en la ruta: {ruta}")
        logging.warning(f"No se encontró la carpeta en la ruta: {ruta}")

if __name__ == "__main__":
    logging.info("Iniciando el programa")
    main()
    #print(f"Carpetas encontradas: {buscar('/Volumes/Resources/Development/SmartBots/Santa_Helena-Subida_Archivos_a_Agente_Aduana/test/resources')}")
    logging.info("Programa finalizado")
