import os


def listar_archivos(ruta):
    archivos_dict = {}
    archivos_ignorados = ["desktop.ini", ".DS_Store"]

    for dir in os.listdir(ruta):
        dir_path = os.path.join(ruta, dir)
        if os.path.isdir(dir_path):
            archivos_dict[dir] = []
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    if file in archivos_ignorados:
                        os.remove(file_path)
                    else:
                        archivos_dict[dir].append(file)

    return archivos_dict


def main(ruta):
    resultado = listar_archivos(ruta)
    print(resultado)


if __name__ == "__main__":
    ruta = "/Volumes/Resources/Development/SmartBots/Santa_Helena-Subida_Archivos_a_Agente_Aduana/test/resources/En Proceso"
    main(ruta)
