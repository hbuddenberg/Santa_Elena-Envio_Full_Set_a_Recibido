import os
import sys

# Añadir la ruta del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from caso_exportacion import CasoExportacion
    from modules.extraer_excel import Configuracion as Configuracion_Excel
except ImportError as e:
    print(f"Error al importar el módulo: {e}")
    sys.exit(1)

CONFIG_EXCEL  = Configuracion_Excel('test/Configuracion/Plantilla_de_Configuracion.xlsx')


def estruturar(carpeta, excel):
    archivos_dict = {}
    

    
    return archivos_dict

def main(ruta):
    resultado = estruturar(ruta, CONFIG_EXCEL)
    print(resultado)

if __name__ == "__main__":
    carpeta = 'FULL SET OF DOCS OE232400007- MSC CASSANDRE- DIVINE (ETA 03-02-2024)'
    main(carpeta)