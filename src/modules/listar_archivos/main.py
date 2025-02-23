import os

def listar_archivos(ruta):
    archivos_dict = {}
    
    for dir in os.listdir(ruta):
        dir_path = os.path.join(ruta, dir)
        if os.path.isdir(dir_path):
            archivos_dict[dir] = {'instructivo': None, 'booking': None}
            for file in os.listdir(dir_path):
                if file.upper().startswith('INSTRUCTIVO'):
                    archivos_dict[dir]['instructivo'] = file
                elif file.upper().startswith('BOOKING'):
                    archivos_dict[dir]['booking'] = file
    
    return archivos_dict

def main(ruta):
    resultado = listar_archivos(ruta)
    print(resultado)

if __name__ == "__main__":
    ruta = '/Volumes/Resources/Development/SmartBots/Santa_Helena-Subida_Archivos_a_Agente_Aduana/test/resources/En Proceso'
    main(ruta)