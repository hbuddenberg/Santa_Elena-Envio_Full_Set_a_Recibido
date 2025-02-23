from modules.configuracion import Configuracion
from modules.buscar_carpeta import buscar as buscar_carpeta
from modules.mover_carpeta import mover, mover_todo
from modules.listar_archivos import listar_archivos
from modules.email_sender import enviar_correo
from modules.informe import genera_informe
from datetime import datetime

CONFIGURACION_PATH = 'src/configuration/configuracion.yaml'

def mover_carpetas_enproceso(ruta):
    archivos = None
    # Lógica principal del programa
    lista_carpetas = buscar_carpeta(ruta)
    if 'En Proceso' in lista_carpetas:
        lista_carpetas.remove('En Proceso')
    if 'Listo' in lista_carpetas:
        lista_carpetas.remove('Listo')
    print(f"Carpetas : {lista_carpetas}")
    if len(lista_carpetas) > 0:
        print("Se encontraron carpetas en la ruta.")
        mover_carpetas = mover(ruta, lista_carpetas)
        if mover_carpetas:
            print("Carpetas movidas correctamente.")
            archivos = listar_archivos(f'{ruta}/En Proceso')
        else:
            print("Error al mover las carpetas.")
    if archivos == None:
        registros = None
    else:
        registros = {'ruta': {'raiz': ruta, 'en_proceso': f'{ruta}/En Proceso'}, 'carpetas': archivos}
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

def proceso_extraer_pdf(ruta, instructivo, archivo, mapeo):
    archivo_pdf = f'{ruta}/{instructivo}/{archivo}'
    result = extraer_pdf(archivo_pdf, mapeo)
    print(result.get_dict())
    if result.get_dict() == None:
        result == None
        print(f"No se encontró un archivo PDF Instructivo en la carpeta {instructivo}")
    else:
        result = result

    return result

def proceso_extraer_pdfs(registros, archivo_json):
    list = []

    if registros != None:
        ruta = registros['ruta']['en_proceso']
        if registros['carpetas'] != None:
            carpetas = registros['carpetas']

            for key, dict in carpetas.items():
                if dict['instructivo'] != None:
                    archivo_pdf = f'{ruta}/{key}/{dict["instructivo"]}'
                    result = extraer_pdf(archivo_pdf, archivo_json)
                    print(result.get_dict())
                    if result.get_dict() != None:
                        list.append(result)
                else:
                    print(f"No se encontró un archivo PDF Instructivo en la carpeta {key}")

    return list if list != [] else None

def llama_api(registro, api):

    response = llamada_api(registro, api)
    print(response)
    registro.set_Api(response)

    return registro

def llamadas_api(registros, api):
    regs = []
    if registros is not None:
        if len(registros) > 0:
            for registro in registros:
                response =  llamada_api(registro, api)
                print(response)
                registro.set_Api(response)

                regs.append(registro)

    return regs if regs!= [] else None

def generacion_informe(registros, ruta):
    # Generar nombre del archivo con la fecha y hora actual
    nombre_archivo = f"Informe_Carga_Intructivo_{datetime.now().strftime('%Y-%m-%d_%H.%M.%S')}.xlsx"
    for registro in registros:
        archivo_informe = genera_informe(registro, ruta, nombre_archivo)
    return archivo_informe

def envio_correo(configuracion, archivo_informe, registros):
    ordenes_embarque = []
    for registro in registros:
        api_response = registro.diccionario['Api']['response']
        if api_response['code'] == 200 and api_response['message']['success'] == True:
            ordenes_embarque.append(registro.diccionario['Orden_Embarque'])

    print(f"Ordenes de embarque exitosas: {ordenes_embarque}")

    if ordenes_embarque:
        enviar_correo(configuracion, archivo_informe, ordenes_embarque)
    else:
        print("No se encontraron órdenes de embarque exitosas para enviar por correo.")

def ejecucion(configuracion):

    carpetas = mover_carpetas_enproceso(configuracion.ruta)

    if carpetas != None:
        ruta, carpetas = listar_carpetas(carpetas)
        lista_ejecucion = []
        for key, dict in carpetas.items():
            if dict['instructivo'] != None: # and len(dict['instructivo']) > 0:
                registro = proceso_extraer_pdf(ruta, key, dict['instructivo'], configuracion.mapeo)
                if registro != None:
                    registro = llama_api(registro, configuracion.get_dict()['api'])
                    lista_ejecucion.append(registro)

        if len(lista_ejecucion) > 0:
            archivo_informe = generacion_informe(lista_ejecucion, configuracion.get_dict()['ruta'])
            enviar_correo(configuracion.correo, archivo_informe, lista_ejecucion, 'api')
            mover_todo(configuracion.ruta)


def main():
    configuracion = Configuracion(CONFIGURACION_PATH)
    ejecucion(configuracion)
    #registros = mover_carpetas_enproceso(configuracion.ruta)
    #registros = proceso_extraer_pdf(registros, configuracion.mapeo)
    #registros = llama_api(registros, configuracion.get_dict()['api'])
    #archivo_informe = generacion_informe(registros, configuracion.get_dict()['ruta'])
    #envio_correo(configuracion.correo,archivo_informe, registros, 'smtp')
    #enviar_correo(configuracion.correo,archivo_informe, registros, 'api')
    #mover_todo(configuracion.ruta)


if __name__ == "__main__":
    main()