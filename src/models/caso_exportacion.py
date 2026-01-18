class CasoExportacion:
    def __init__(
        self,
        recibidor="",
        pais="",
        emails_para="",
        emails_copia="",
        adjuntos="",
        asunto="",
        cuerpo="",
    ):
        self.recibidor = recibidor
        self.pais = pais
        self.emails_para = emails_para
        self.emails_copia = emails_copia
        self.adjuntos = adjuntos
        self.asunto = asunto
        self.cuerpo = cuerpo

    def __repr__(self):
        return (
            f"CasoExportacion(recibidor={self.recibidor}, pais={self.pais}, emails_para={self.emails_para}, "
            f"emails_copia={self.emails_copia}, adjuntos={self.adjuntos}, "
            f"asunto={self.asunto}, cuerpo={self.cuerpo})"
        )

    def to_dict(self):
        return {
            "recibidor": self.recibidor,
            "pais": self.pais,
            "emails_para": self.emails_para,
            "emails_copia": self.emails_copia,
            "adjuntos": self.adjuntos,
            "asunto": self.asunto,
            "cuerpo": self.cuerpo,
        }

    def set(
        self,
        recibidor=None,
        pais=None,
        emails_para=None,
        emails_copia=None,
        adjuntos=None,
        asunto=None,
        cuerpo=None,
    ):
        if recibidor is not None:
            self.recibidor = recibidor
        if pais is not None:
            self.pais = pais
        if emails_para is not None:
            self.emails_para = emails_para
        if emails_copia is not None:
            self.emails_copia = emails_copia
        if adjuntos is not None:
            self.adjuntos = adjuntos
        if asunto is not None:
            self.asunto = asunto
        if cuerpo is not None:
            self.cuerpo = cuerpo


"""
# Ejemplo de uso
caso = CasoExportacion(
    recibidor='Recibidor',
    pais='España',
    emails_para='example@example.com',
    emails_copia='cc@example.com',
    adjuntos='documento.pdf',
    asunto='Asunto del correo',
    cuerpo='Cuerpo del correo'
)

print(caso)
print(caso.to_dict())

# Usando el setter para cambiar todos los campos
caso.set(recibidor='Nuevo Recibidor', pais='Francia', emails_para='nuevo@example.com', emails_copia='nuevo_cc@example.com', adjuntos='nuevo_documento.pdf', asunto='Nuevo Asunto', cuerpo='Nuevo Cuerpo')
print(caso)
print(caso.to_dict())
"""
