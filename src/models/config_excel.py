from pprint import pp

import pandas as pd


class DistribucionCorreos:
    def __init__(
        self,
        casos_exportacion,
        pais,
        emails_para,
        emails_copia,
        adjuntos,
        asunto,
        cuerpo,
        ejemplos,
        notas,
    ):
        self.casos_exportacion = casos_exportacion
        self.pais = pais
        self.emails_para = emails_para
        self.emails_copia = emails_copia
        self.adjuntos = adjuntos
        self.asunto = asunto
        self.cuerpo = cuerpo
        self.ejemplos = ejemplos
        self.notas = notas

    def to_dict(self):
        return self.__dict__


class RecibidoresEmails:
    def __init__(self, recibidor, distribucion_correos, lista_emails):
        self.recibidor = recibidor
        self.distribucion_correos = distribucion_correos
        self.lista_emails = lista_emails

    def to_dict(self):
        return self.__dict__


class ResumenCC:
    def __init__(self, tipo, cc, lista_emails):
        self.tipo = tipo
        self.cc = cc
        self.lista_emails = lista_emails

    def to_dict(self):
        return self.__dict__


class EmailReporte:
    def __init__(self, tipo, lista_emails):
        self.tipo = tipo
        self.lista_emails = lista_emails

    def to_dict(self):
        return self.__dict__


class Modelo:
    def __init__(self, distribucion_correos, recibidores_emails, resumen_cc, email_reporte):
        self.distribucion_correos = [DistribucionCorreos(**self._convert_keys(dc)) for dc in distribucion_correos]
        self.recibidores_emails = [RecibidoresEmails(**self._convert_keys(re)) for re in recibidores_emails]
        self.resumen_cc = [ResumenCC(**self._convert_keys(rc)) for rc in resumen_cc]
        self.email_reporte = [EmailReporte(**self._convert_keys(er)) for er in email_reporte]

    def _convert_keys(self, data):
        return {self._convert_key(k): v for k, v in data.items()}

    def _convert_key(self, key):
        return key.lower().replace(" ", "_")

    def to_dict(self):
        return {
            "distribucion_correos": [dc.to_dict() for dc in self.distribucion_correos],
            "recibidores_emails": [re.to_dict() for re in self.recibidores_emails],
            "resumen_cc": [rc.to_dict() for rc in self.resumen_cc],
            "email_reporte": [er.to_dict() for er in self.email_reporte],
        }


def cargar_modelo(data):
    return Modelo(
        distribucion_correos=data["DISTRIBUCION CORREOS"],
        recibidores_emails=data["RECIBIDORES EMAILS"],
        resumen_cc=data["RESUMEN CC"],
        email_reporte=data["EMAIL REPORTE"],
    )


def load_config(archivo_excel):
    xls = pd.ExcelFile(archivo_excel)
    datos = {}
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        datos[sheet_name] = df.to_dict(orient="records")
    modelo = cargar_modelo(datos)
    return modelo


def main(archivo_excel):
    datos = load_config(archivo_excel)
    pp(datos.to_dict())


if __name__ == "__main__":
    archivo_excel = "/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/test/Configuracion/Plantilla_de_Configuracion.xlsx"
    main(archivo_excel)
