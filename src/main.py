from modules.configuracion import Configuracion as Configuracion_Yaml
from modules.extraer_excel import Configuracion as Configuracion_Excel
from modules.buscar_carpeta import buscar_carpeta
from modules.mover_carpeta import eliminar_carpetas, mover, mover_todo
from modules.listar_archivos import listar_archivos
from modules.estructurar_registro import estructurar

from pprint import pp 

CONFIG_GLOBAL = Configuracion_Yaml('src/configuration/configuracion.yaml')
CONFIG_EXCEL  = Configuracion_Excel(CONFIG_GLOBAL.config.path.shared.config)

def mover_carpetas_enproceso(ruta):
    archivos = None
    lista_carpetas = buscar_carpeta(ruta)
    if 'Configuracion' in lista_carpetas:
        lista_carpetas.remove('Configuracion')
    if 'En Proceso' in lista_carpetas:
        lista_carpetas.remove('En Proceso')
    if 'Listo' in lista_carpetas:
        lista_carpetas.remove('Listo')
    print(f"Carpetas : {lista_carpetas}")
    if len(lista_carpetas) > 0:
        print("Se encontraron carpetas en la ruta.")
        eliminar_carpetas(ruta)
        mover_carpetas = mover(ruta, lista_carpetas)
        if mover_carpetas:
            print("Carpetas movidas correctamente.")
            carpetas = listar_archivos(f'{ruta}/En Proceso')
        else:
            print("Error al mover las carpetas.")
    if carpetas == None or len(carpetas) == 0:
        registros = None
    else:
        registros = {'ruta': {'raiz': ruta, 'en_proceso': f'{ruta}/En Proceso'}, 'carpetas': carpetas}
    return registros

def listar_carpetas(registros: dict):
    ruta = registros['ruta']['en_proceso']
    if registros != None:
        if registros['carpetas'] != None:
            carpetas = registros['carpetas']
            print(f"Carpetas : {carpetas}")
        else:
            print(f"No se encontró un archivo PDF Instructivo en la carpeta {ruta}")
    else:
        print(f"No se encontró un archivo PDF Instructivo en la carpeta.")

    if carpetas == []:
        carpetas = None

    return ruta, carpetas

def registros(carpetas: dict):
    lista_ejecucion = []
    for folder, files in carpetas['carpetas'].items():
        ruta = f"{carpetas['ruta']['En Progreso']}/{folder}"
        estructura = estructurar(folder, CONFIG_EXCEL)
    
    return lista_ejecucion

def ejecutar():
    carpetas = mover_carpetas_enproceso(CONFIG_GLOBAL.config.path.shared.main)
    if carpetas != None:
        if len(carpetas['carpetas']) > 0:
            ejecucion = registros(carpetas)

def main():
    ejecutar()

if __name__ == "__main__":
    main()