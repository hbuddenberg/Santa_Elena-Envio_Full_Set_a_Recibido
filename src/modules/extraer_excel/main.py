from models import load_config_excel as load_config


class Configuracion:
    def __init__(self, archivo_configuracion):
        self.path_file = archivo_configuracion
        self.config = load_config(archivo_configuracion)

    def get_dict(self):
        return {"config_fil": self.path_file, "config": self.config.to_dict()}

    def get_config(self):
        return self.config

    def get_path_file(self):
        return self.path_file


def main(archivo_excel):
    Configuracion(archivo_excel)


if __name__ == "__main__":
    archivo_excel = "/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/Configuracion/Plantilla_de_Configuracion.xlsx"
    main(archivo_excel)
